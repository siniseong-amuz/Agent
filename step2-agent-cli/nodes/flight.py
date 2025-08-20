from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream

def get_flight_node(llm=None) -> RunnableLambda:
    def _flight(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"다음을 3~5단어로 간단히 제목만 출력: {user_input}"
        
        flight_prompt_text = (
            "항공편 관련 질문에 답변해주세요. 항공편 조회, 예약, 체크인, 수하물 등에 대한 정보를 제공하세요.\n\n"
            f"항공편 질문: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )

        title, full_response = stream(
            user_input=user_input,
            intent="flight",
            title_prompt=title_prompt_text,
            response_prompt=flight_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "비행 시간",
            "intent": "비행 시간",
            "result": {"response": full_response}
        }

    return RunnableLambda(_flight)