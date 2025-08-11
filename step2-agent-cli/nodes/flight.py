from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_json_response

prompt = ChatPromptTemplate.from_messages([
    ("system", "항공편 관련 질문에 답변해주세요. 항공편 조회, 예약, 체크인, 수하물 등에 대한 정보를 제공할 수 있습니다."),
    ("human", "항공편 질문: {user_input}")
])

def get_flight_node(llm) -> RunnableLambda:
    def _flight(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        
        chain = prompt | llm
        
        def response_generator():
            for chunk in chain.stream({"user_input": user_input}):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
        
        full_response = stream_json_response(
            user_input=user_input,
            title="항공편",
            intent="항공편",
            response_iterator=response_generator()
        )
        
        return {
            "input": user_input,
            "title": "항공편",
            "intent": "항공편",
            "result": {
                "response": full_response
            }
        }

    return RunnableLambda(_flight)