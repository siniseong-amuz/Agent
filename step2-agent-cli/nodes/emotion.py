from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_gemini_response, get_gemini_model

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 감정분석 요청을 기반으로 3~5 단어의 간단한 제목을 생성하세요. 응답과 중복되지 않게 하세요."),
    ("human", "{user_input}")
])

def get_emotion_node(llm=None) -> RunnableLambda:
    def _emotion(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        if llm is not None:
            try:
                title_msg = (title_prompt | llm).invoke({"user_input": user_input})
                title = getattr(title_msg, "content", str(title_msg)).strip() or "감정분석"
            except Exception:
                title = "감정분석"
        else:
            try:
                model = get_gemini_model()
                t = model.generate_content(
                    f"다음 텍스트 감정 분석 요청을 3~5 단어의 한국어 제목으로 요약: {user_input}"
                )
                title = (getattr(t, "text", "") or "").strip() or "감정분석"
            except Exception:
                title = "감정분석"

        emotion_prompt_text = (
            "텍스트의 감정을 간단하게 분석하세요. 주요 감정과 강도만 짧게 답변하세요.\n\n"
            f"감정 분석해주세요: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )

        full_response = stream_gemini_response(
            user_input=user_input,
            title=title,
            intent="emotion",
            prompt=emotion_prompt_text
        )

        return {
            "input": user_input,
            "title": title,
            "intent": "emotion",
            "result": {"response": full_response}
        }

    return RunnableLambda(_emotion)
