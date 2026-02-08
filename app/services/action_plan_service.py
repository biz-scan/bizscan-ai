import asyncio
import json
from typing import Dict, Any
from pydantic import HttpUrl

from app.core.logger import logger
from app.schemas.common_schema import CallbackResponse
from app.schemas.swot_schema import SWOTResponse
from app.schemas.action_plan_schema import CandidateResponse, EvaluateResponse, FinalSelectResponse, ActionDetailResponse
from app.schemas.analysis_schema import ActionPlanCallbackResponse, FinalSelectCallbackResponse
from app.core.chains import action_detail_chain, candidate_chain, evaluate_chain, final_select_chain
from app.utils.http_utils import send_callback

async def create_action_plan(swot_data: SWOTResponse, action_plan_callback_url: HttpUrl, action_detail_callback_url: HttpUrl, fail_callback_url: HttpUrl,request_id: str):
    """
    4단계 체인을 순차적으로 실행하여 최종 실행 계획을 도출합니다.    

    1~3단계는 중복 방지를 위해 각 SWOT 조합 별(SO, ST, WO, WT)로 루프를 수행하여 총 4번의 루프를 수행합니다.
    4단계(실행 계획)는 성능 향상을 위해 병렬로 실행합니다.
    """
    swot_json_str = swot_data.model_dump_json(ensure_ascii=False)

    # 4가지 조합 정의
    quadrants = [
        {"type": "SO", "desc": "내부의 강점(S)을 활용하여 외부의 기회(O)를 적극적으로 포착하는 공격적 전략", "f1": swot_data.strengths, "f2": swot_data.opportunities},
        {"type": "ST", "desc": "내부의 강점(S)을 활용하여 외부의 위협(T)을 회피하거나 극복하는 방어적 전략", "f1": swot_data.strengths, "f2": swot_data.threats},
        {"type": "WO", "desc": "내부의 약점(W)을 보완하여 외부의 기회(O)를 활용하는 방향 전환 전략", "f1": swot_data.weaknesses, "f2": swot_data.opportunities},
        {"type": "WT", "desc": "내부의 약점(W)을 보완하고 외부의 위협(T)으로부터 생존하기 위한 철수 또는 방어 전략", "f1": swot_data.weaknesses, "f2": swot_data.threats}
    ]

    accumulated_titles = []  # 중복 방지를 위한 전략 제목 저장소
    all_action_details = []    # 최종 8개(2*4) 저장용
    all_final_selections = [] # 최종 선정된 모든 전략 (총 8개 예정)
    current_start_id = 1 # 전략 구분 용 ID

    try:
        for quad in quadrants:
            q_type = quad["type"]
            # --- 1단계: 전략 후보 생성 ---
            logger.info(f"--- [{q_type}] 1단계: 후보군 생성 시작 ---")
            f1_json = json.dumps(quad["f1"].model_dump(), ensure_ascii=False)
            f2_json = json.dumps(quad["f2"].model_dump(), ensure_ascii=False)
            candidates_res = await candidate_chain.ainvoke({
                "quadrant_type": q_type,
                "current_guide": quad["desc"],
                "factor_1": f1_json,
                "factor_2": f2_json,
                "previous_strategies": accumulated_titles,
                "start_id": current_start_id
            })
            logger.debug(f"Candidate Chain 결과: {candidates_res.model_dump_json(indent=4, ensure_ascii=False)}")
            candidates = candidates_res.candidates # List[CandidateResult]

            # --- 2단계: 후보군 평가 ---
            logger.info(f"--- [{q_type}] 2단계: 후보군 평가 시작 ---")
            candidate_list_json = json.dumps(
                [c.model_dump() for c in candidates], 
                ensure_ascii=False
            )
            evaluate_res: EvaluateResponse = await evaluate_chain.ainvoke({
                "swot_json": swot_json_str,
                "candidate_list": candidate_list_json
            })
            logger.debug(f"Evaluation Chain 결과: {evaluate_res.model_dump_json(indent=4, ensure_ascii=False)}")
            evaluations = evaluate_res.evaluations # List[EvaluateResponse]

            # --- 3단계: 최종 전략 선정 ---
            logger.info(f"--- [{q_type}] 3단계: 핵심 전략 선정 시작 ---")
            evaluated_candidates_json = json.dumps(
                [e.model_dump() for e in evaluations], 
                ensure_ascii=False
            )
            final_select_res: FinalSelectResponse = await final_select_chain.ainvoke({
                "swot_json": swot_json_str,
                "candidate_list": candidate_list_json,
                "evaluated_candidates": evaluated_candidates_json
            })
            logger.debug(f"Final Select Chain 결과: {final_select_res.model_dump_json(indent=4, ensure_ascii=False)}")
            selections = final_select_res.selections # List[FinalSelectResponse]

            for selection in final_select_res.selections:
                all_final_selections.append(selection)
                accumulated_titles.append(selection.title)
            current_start_id += 4

        
        # --- 중간 콜백 전송 (선정 결과 알림) ---
        logger.info("--- 모든 전략 선정 완료: ACTION_DETAIL_PROCESSING 콜백 전송 ---")
        payload = CallbackResponse(
            request_id=request_id,
            status="ACTION_DETAIL_PROCESSING",
            result=FinalSelectCallbackResponse(final_select=FinalSelectResponse(selections=all_final_selections))
        )
        await send_callback(action_plan_callback_url, payload)
        logger.info("ACTION_DETAIL_PROCESSING 콜백 전송 완료")
        

        # --- [마지막 단계] 실행 계획 수립 (병렬 처리) ---
        logger.info("--- 마지막 단계: 실행 계획 병렬 수립 시작 ---")

        tasks = []
        for selection in all_final_selections:
            final_selected_json = json.dumps([selection.model_dump()], ensure_ascii=False)
            # ainvoke 태스크를 리스트에 담음
            tasks.append(action_detail_chain.ainvoke({
                "swot_json": swot_json_str,
                "final_selected_strategies": final_selected_json
            }))
        
        action_detail_responses = await asyncio.gather(*tasks)

        all_action_details = []
        for res in action_detail_responses:
            all_action_details.extend(res.plans)
        
        log_data = [plan.model_dump() for plan in all_action_details]
        logger.debug(
            f"ActionDetail 최종 결과물:\n"
            f"{json.dumps(log_data, indent=4, ensure_ascii=False)}"
        )

        

        # --- 모든 루프 종료 후 최종 COMPLETED 콜백 전송 ---
        payload = CallbackResponse(
            request_id=request_id,
            status="COMPLETED",
            result = ActionPlanCallbackResponse(
                action_plan=ActionDetailResponse(plans=all_action_details) # 필드명을 plans로 변경
            )
        )
        await send_callback(action_detail_callback_url, payload)
        logger.info("전체 프로세스 완료 및 최종 콜백 전송 완료")
        
    
    except Exception as e:
        # 에러 발생 시 로그를 남기고 SpringBoot에 알림
        logger.error(f"작업 중 에러 발생: {str(e)}", exc_info=True)
        
        payload = CallbackResponse(
            isSuccess=False,
            code="AI_ERROR_500",
            message="실행 전략 생성 중 오류가 발생했습니다.",
            request_id=request_id,
            status="FAILED"
        )
        await send_callback(fail_callback_url, payload)
        logger.info("에러 콜백 전송 완료")        



