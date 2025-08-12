from langchain_core.runnables import RunnableLambda
from typing import Dict
from streaming_utils import stream_title_and_response

def get_talk_node(llm=None) -> RunnableLambda:
    def _talk(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"다음을 3~5단어로 간단히 제목만 출력: {user_input}"
        
        talk_prompt_text = (
            "자연스럽게 대화하세요. 간단하고 직접적으로 답변해주세요.\n\n"
            f"이전 대화 맥락:\n{history_context}\n\n"
            f"사용자 질문: {user_input}"
        )

        title, full_response = stream_title_and_response(
            user_input=user_input,
            intent="일상대화",
            title_prompt=title_prompt_text,
            response_prompt=talk_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "대화",
            "intent": "일상대화",
            "result": {"response": full_response}
        }

    return RunnableLambda(_talk)
