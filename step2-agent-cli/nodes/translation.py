from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from streaming_utils import stream_gemini_response, get_gemini_model

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 번역 요청을 기반으로 3~5 단어의 간단한 제목을 생성하세요. 응답과 중복되지 않게 하세요."),
    ("human", "{user_input}")
])

def get_translation_node(llm=None) -> RunnableLambda:
    def _translate(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        if llm is not None:
            try:
                title_msg = (title_prompt | llm).invoke({"user_input": user_input})
                title = getattr(title_msg, "content", str(title_msg)).strip() or "번역"
            except Exception:
                title = "번역"
        else:
            try:
                model = get_gemini_model()
                t = model.generate_content(
                    f"다음 번역 요청을 3~5 단어의 한국어 제목으로 요약: {user_input}"
                )
                title = (getattr(t, "text", "") or "").strip() or "번역"
            except Exception:
                title = "번역"

        translation_prompt_text = (
            "번역만 해주세요. 설명이나 추가 정보 없이 번역 결과만 출력하세요.\n\n"
            f"번역해주세요: {user_input}"
        )

        full_response = stream_gemini_response(
            user_input=user_input,
            title=title,
            intent="번역",
            prompt=translation_prompt_text
        )

        return {
            "input": user_input,
            "title": title,
            "intent": "번역",
            "result": {"response": full_response}
        }

    return RunnableLambda(_translate)
