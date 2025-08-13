from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream_emotion

def get_emotion_node(llm=None) -> RunnableLambda:
    def _emotion(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"다음을 3~5단어로 간단히 제목만 출력: {user_input}"
        
        emotion_prompt_text = (
            f"텍스트의 주요 감정만 한 단어로 출력하세요: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )
        
        message_prompt_text = (
            f"다음 텍스트에 대해 공감하고 위로하는 메시지를 작성해주세요: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )

        title, emotion_response, message_response = stream_emotion(
            user_input=user_input,
            intent="emotion",
            title_prompt=title_prompt_text,
            emotion_prompt=emotion_prompt_text,
            message_prompt=message_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "감정분석",
            "intent": "emotion",
            "result": {
                "response": emotion_response,
                "message": message_response
            }
        }

    return RunnableLambda(_emotion)
