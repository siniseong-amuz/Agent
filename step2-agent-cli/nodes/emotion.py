from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream_emotion

def get_emotion_node(llm=None) -> RunnableLambda:
    def _emotion(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"Output only a simple title in 3-5 words for the following: {user_input}"
        
        emotion_prompt_text = (
            f"Output only the main emotion of the text in one word: {user_input}\n\n"
            f"(Reference context)\n{history_context}"
        )
        
        message_prompt_text = (
            f"Please write an empathetic and comforting message about the following text: {user_input}\n\n"
            f"(Reference context)\n{history_context}"
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
            "title": title or "Emotion Analysis",
            "intent": "emotion",
            "result": {
                "response": emotion_response,
                "message": message_response
            }
        }

    return RunnableLambda(_emotion)
