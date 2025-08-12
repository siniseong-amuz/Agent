from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from streaming_utils import stream_gemini_response, get_gemini_model

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 시간대 질문을 기반으로 3~5 단어의 간단한 제목을 생성하세요. 응답과 중복되지 않게 하세요."),
    ("human", "{user_input}")
])

def get_timezone_node(llm=None) -> RunnableLambda:
    def _timezone(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")

        if llm is not None:
            try:
                title_msg = (title_prompt | llm).invoke({"user_input": user_input})
                title = getattr(title_msg, "content", str(title_msg)).strip() or "시간대"
            except Exception:
                title = "시간대"
        else:
            try:
                model = get_gemini_model()
                t = model.generate_content(
                    f"다음 시간대 질문을 3~5 단어의 한국어 제목으로 요약: {user_input}"
                )
                title = (getattr(t, "text", "") or "").strip() or "시간대"
            except Exception:
                title = "시간대"

        timezone_prompt_text = (
            "시간대 관련 질문에 답변해주세요. 현재 시간, 다른 나라 시간, 시간대 변환 등을 도와주세요.\n\n"
            f"시간대 질문: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )

        full_response = stream_gemini_response(
            user_input=user_input,
            title=title,
            intent="시간대",
            prompt=timezone_prompt_text
        )

        return {
            "input": user_input,
            "title": title,
            "intent": "시간대",
            "result": {"response": full_response}
        }

    return RunnableLambda(_timezone)
