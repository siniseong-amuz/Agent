from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream

def get_timezone_node(llm=None) -> RunnableLambda:
    def _timezone(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"3~5단어로 간단히 제목만 출력: {user_input}"
        
        timezone_prompt_text = (
            "시간대 관련 질문에 답변해주세요. 현재 시간, 다른 나라 시간, 시간대 변환 등을 도와주세요.\n\n"
            f"시간대 질문: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )

        title, full_response = stream(
            user_input=user_input,
            intent="시간대",
            title_prompt=title_prompt_text,
            response_prompt=timezone_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "시간대",
            "intent": "시간대",
            "result": {"response": full_response}
        }

    return RunnableLambda(_timezone)
