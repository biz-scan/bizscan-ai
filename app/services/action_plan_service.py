import json
import httpx
from typing import Dict, Any
from pydantic import HttpUrl

from app.schemas.common_schema import CommonResponse
from app.schemas.action_plan_schema import ActionPlanResponse, CandidateResponse, EvaluationResponse, SelectionResponse
from app.core.chains import action_plan_chain, candidate_chain, evaluation_chain, selection_chain

async def create_action_plan(swot_data: Dict[str, Any], action_plan_callback_url: HttpUrl) -> ActionPlanResponse:
    """
    4단계 체인을 순차적으로 실행하여 최종 실행 계획을 도출합니다.
    """
    swot_json_str = json.dumps(swot_data, ensure_ascii=False)

    try:
        # 1단계: 전략 후보 생성
        print("--- 1단계: 후보군 생성 중 ---")
        candidates_res: CandidateResponse = await candidate_chain.ainvoke({
            "swot_json": swot_json_str
        })
        candidates = candidates_res.candidates # List[CandidateResult]

        # 2단계: 후보군 평가
        print("--- 2단계: 후보군 평가 중 ---")
        evaluation_res: EvaluationResponse = await evaluation_chain.ainvoke({
            "swot_json": swot_json_str,
            "candidate_list": json.dumps(candidates, ensure_ascii=False)
        })
        evaluations = evaluation_res.evaluations # List[EvaluationResult]

        # 3단계: 최종 전략 선정
        print("--- 3단계: 핵심 전략 선정 중 ---")
        selection_res: SelectionResponse = await selection_chain.ainvoke({
            "swot_json": swot_json_str,
            "candidate_list": json.dumps(candidates, ensure_ascii=False),
            "evaluated_candidates": json.dumps(evaluations, ensure_ascii=False)
        })
        selections = selection_res.selections # List[SelectionResult]

        # 4단계: 실행 계획(To-Do) 수립
        print("--- 4단계: 실행 계획 수립 중 ---")
        final_action_plan: ActionPlanResponse = await action_plan_chain.ainvoke({
            "swot_json": swot_json_str,
            "final_selected_strategies": json.dumps(selections, ensure_ascii=False)
        })

        # 성공 콜백 전송
        payload = CommonResponse(
            isSuccess=True,
            code="COMMON200",
            message="AI 분석이 완료되었습니다.",
            result=final_action_plan.model_dump()
        )
        await send_callback(action_plan_callback_url, payload)
    
    except Exception as e:
        # 에러 발생 시 로그를 남기고 SpringBoot에 알림
        print(f"!!! 작업 중 에러 발생: {str(e)} !!!")
        
        payload = CommonResponse(
            isSuccess=False,
            code="AI_ERROR_500",
            message="AI 분석 중 오류가 발생했습니다.",
            result={"error_detail": str(e)}
        )
        await send_callback(action_plan_callback_url, payload)


async def send_callback(url: HttpUrl, payload: Dict[str, Any]):
    """콜백 전송 로직 공통화"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                str(url),
                json=payload,
                timeout=10.0
            )
            response.raise_for_status()
        except Exception as e:
            print(f"--- 콜백 전송 최종 실패: {str(e)} ---")