from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream

def get_summary_node(llm=None) -> RunnableLambda:
    def _summary(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"다음을 3~5단어로 간단히 제목만 출력: {user_input}"
        
        summary_prompt_text = (
            "텍스트를 요약해주세요. 핵심 내용을 간결하고 명확하게 정리하세요.\n\n"
            f"요약해주세요: {user_input}\n\n"
            f"(참고 맥락)\n{history_context}"
        )

        title, full_response = stream(
            user_input=user_input,
            intent="summary",
            title_prompt=title_prompt_text,
            response_prompt=summary_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "요약",
            "intent": "summary",
            "result": {"response": full_response}
        }

    return RunnableLambda(_summary)