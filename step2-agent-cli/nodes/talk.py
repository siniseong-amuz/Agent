from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from streaming_utils import stream_gemini_response, get_gemini_model

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 질문을 기반으로 3~5 단어의 간단한 제목을 생성하세요. 응답 내용과 중복되지 않게 하세요."),
    ("human", "{user_input}")
])

def get_talk_node(llm=None) -> RunnableLambda:
    def _talk(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        if llm is not None:
            try:
                title_msg = (title_prompt | llm).invoke({"user_input": user_input})
                title = getattr(title_msg, "content", str(title_msg)).strip() or "대화"
            except Exception:
                title = "대화"
        else:
            try:
                model = get_gemini_model()
                title_resp = model.generate_content(
                    f"다음 사용자 질문을 3~5 단어의 한국어 제목으로 요약: {user_input}"
                )
                title = (getattr(title_resp, "text", "") or "").strip() or "대화"
            except Exception:
                title = "대화"

        talk_prompt_text = f"""자연스럽게 대화하세요. 간단하고 직접적으로 답변해주세요.

        이전 대화 맥락:
        {history_context}

        사용자 질문: {user_input}"""

        full_response = stream_gemini_response(
            user_input=user_input,
            title=title,
            intent="일상대화",
            prompt=talk_prompt_text
        )

        return {
            "input": user_input,
            "title": title,
            "intent": "일상대화",
            "result": {"response": full_response}
        }

    return RunnableLambda(_talk)
