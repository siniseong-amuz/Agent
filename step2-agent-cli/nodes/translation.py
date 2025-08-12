from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream_title_and_response

def get_translation_node(llm=None) -> RunnableLambda:
    def _translate(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"다음 번역 요청을 3~5 단어의 한국어 제목으로 요약: {user_input}"
        
        translation_prompt_text = (
            "번역만 해주세요. 설명이나 추가 정보 없이 번역 결과만 출력하세요.\n\n"
            f"번역해주세요: {user_input}"
            f"(참고 맥락)\n{history_context}"
        )

        title, full_response = stream_title_and_response(
            user_input=user_input,
            intent="번역",
            title_prompt=title_prompt_text,
            response_prompt=translation_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "번역",
            "intent": "번역",
            "result": {"response": full_response}
        }

    return RunnableLambda(_translate)
