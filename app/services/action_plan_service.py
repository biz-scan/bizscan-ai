
import json
from typing import Dict, Any
from pydantic import HttpUrl

from app.core.logger import logger
from app.schemas.common_schema import CommonResponse
from app.schemas.action_plan_schema import CandidateResponse, EvaluationResponse, SelectionResponse, ActionPlanResponse
from app.schemas.analysis_schema import ActionPlanCallbackResponse
from app.core.chains import action_plan_chain, candidate_chain, evaluation_chain, selection_chain
from app.utils.http_utils import send_callback

async def create_action_plan(swot_data: Dict[str, Any], action_plan_callback_url: HttpUrl):
    """
    4단계 체인을 순차적으로 실행하여 최종 실행 계획을 도출합니다.
    """
    swot_json_str = json.dumps(swot_data, ensure_ascii=False)

    try:
        # 1단계: 전략 후보 생성
        logger.info("--- 1단계: 후보군 생성 시작 ---")
        candidates_res: CandidateResponse = await candidate_chain.ainvoke({
            "swot_json": swot_json_str
        })
        logger.debug(f"Candidate Chain 결과: {candidates_res.model_dump_json(indent=4, ensure_ascii=False)}")
        candidates = candidates_res.candidates # List[CandidateResult]

        # 2단계: 후보군 평가
        logger.info("--- 2단계: 후보군 평가 시작 ---")
        candidate_list_json = json.dumps(
            [c.model_dump() for c in candidates], 
            ensure_ascii=False
        )
        evaluation_res: EvaluationResponse = await evaluation_chain.ainvoke({
            "swot_json": swot_json_str,
            "candidate_list": candidate_list_json
        })
        logger.debug(f"Evaluation Chain 결과: {evaluation_res.model_dump_json(indent=4, ensure_ascii=False)}")
        evaluations = evaluation_res.evaluations # List[EvaluationResult]

        # 3단계: 최종 전략 선정
        logger.info("--- 3단계: 핵심 전략 선정 시작 ---")
        evaluated_candidates_json = json.dumps(
            [e.model_dump() for e in evaluations], 
            ensure_ascii=False
        )
        selection_res: SelectionResponse = await selection_chain.ainvoke({
            "swot_json": swot_json_str,
            "candidate_list": candidate_list_json,
            "evaluated_candidates": evaluated_candidates_json
        })
        logger.debug(f"Final Select Chain 결과: {selection_res.model_dump_json(indent=4, ensure_ascii=False)}")
        selections = selection_res.selections # List[SelectionResult]

        # 4단계: 실행 계획(To-Do) 수립
        logger.info("--- 4단계: 실행 계획 수립 시작 ---")
        final_selected_json = json.dumps(
            [s.model_dump() for s in selections], 
            ensure_ascii=False
        )
        final_action_plan: ActionPlanResponse = await action_plan_chain.ainvoke({
            "swot_json": swot_json_str,
            "final_selected_strategies": final_selected_json
        })
        logger.debug(f"ActionPlan Chain 결과:\n {final_action_plan.model_dump_json(indent=4, ensure_ascii=False)}")

        callback_data = ActionPlanCallbackResponse(
            status="success",
            action_plan=final_action_plan
        )

        # 성공 콜백 전송
        payload = CommonResponse(
            result=callback_data
        )
        # await send_callback(action_plan_callback_url, payload)
        logger.info("성공 콜백 전송 완료")
        print(callback_data)
    
    except Exception as e:
        # 에러 발생 시 로그를 남기고 SpringBoot에 알림
        logger.error(f"작업 중 에러 발생: {str(e)}", exc_info=True)
        
        payload = CommonResponse(
            isSuccess=False,
            code="AI_ERROR_500",
            message="AI 분석 중 오류가 발생했습니다.",
            result={"error_detail": str(e)}
        )
        # await send_callback(action_plan_callback_url, payload)
        logger.info("에러 콜백 전송 완료")        



