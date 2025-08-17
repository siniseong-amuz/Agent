from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream_translation

def get_translation_node(llm=None) -> RunnableLambda:
    def _translate(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"3~5단어로 간단히 제목만 출력: {user_input}"
        
        translation_prompt_text = (
            "번역만 해주세요. 설명이나 추가 정보 없이 번역 결과만 출력하세요.\n\n"
            f"번역해주세요: {user_input}"
            f"(참고 맥락)\n{history_context}"
        )

        title, original, translation = stream_translation(
            user_input=user_input,
            intent="translation",
            title_prompt=title_prompt_text,
            response_prompt=translation_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "Translation",
            "intent": "translation",
            "result": {
                "original": original,
                "translation": translation
            }
        }

    return RunnableLambda(_translate)
