from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream_title_and_response

def get_emotion_node(llm=None) -> RunnableLambda:
    def _emotion(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"다음을 3~5단어로 간단히 제목만 출력: {user_input}"
        
        emotion_prompt_text = (
            "텍스트의 감정을 간단하게 분석하세요. 주요 감정과 강도만 짧게 답변하세요.\n\n"
            f"감정 분석해주세요: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )

        title, full_response = stream_title_and_response(
            user_input=user_input,
            intent="emotion",
            title_prompt=title_prompt_text,
            response_prompt=emotion_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "감정분석",
            "intent": "emotion",
            "result": {"response": full_response}
        }

    return RunnableLambda(_emotion)
