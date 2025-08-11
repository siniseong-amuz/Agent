from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_json_response

prompt = ChatPromptTemplate.from_messages([
    ("system", "시간대 관련 질문에 답변해주세요. 현재 시간, 다른 나라 시간, 시간대 변환 등을 도움을 드릴 수 있습니다."),
    ("human", "시간대 질문: {user_input}")
])

def get_timezone_node(llm) -> RunnableLambda:
    def _timezone(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        
        chain = prompt | llm
        
        def response_generator():
            for chunk in chain.stream({"user_input": user_input}):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
        
        full_response = stream_json_response(
            user_input=user_input,
            title="시간대",
            intent="시간대",
            response_iterator=response_generator()
        )
        
        return {
            "input": user_input,
            "title": "시간대",
            "intent": "시간대",
            "result": {
                "response": full_response
            }
        }

    return RunnableLambda(_timezone)