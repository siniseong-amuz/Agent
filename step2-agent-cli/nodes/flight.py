from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_gemini_response, get_gemini_model

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 항공편 질문을 기반으로 3~5 단어의 간단한 제목을 생성하세요. 응답과 중복되지 않게 하세요."),
    ("human", "{user_input}")
])

def get_flight_node(llm=None) -> RunnableLambda:
    def _flight(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        if llm is not None:
            try:
                title_msg = (title_prompt | llm).invoke({"user_input": user_input})
                title = getattr(title_msg, "content", str(title_msg)).strip() or "flight"
            except Exception:
                title = "flight"
        else:
            try:
                model = get_gemini_model()
                t = model.generate_content(
                    f"다음 항공편 질문을 3~5 단어의 한국어 제목으로 요약: {user_input}"
                )
                title = (getattr(t, "text", "") or "").strip() or "flight"
            except Exception:
                title = "flight"

        flight_prompt_text = (
            "항공편 관련 질문에 답변해주세요. 항공편 조회, 예약, 체크인, 수하물 등에 대한 정보를 제공하세요.\n\n"
            f"항공편 질문: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )

        full_response = stream_gemini_response(
            user_input=user_input,
            title=title,
            intent="flight",
            prompt=flight_prompt_text
        )

        return {
            "input": user_input,
            "title": title,
            "intent": "flight",
            "result": {"response": full_response}
        }

    return RunnableLambda(_flight)