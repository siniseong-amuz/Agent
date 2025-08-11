from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_all_fields_response

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 항공편 질문을 기반으로 3-5단어의 간단한 제목을 생성하세요. 응답이랑 내용이 중복되지 않도록 하세요."),
    ("human", "{user_input}")
])

flight_prompt = ChatPromptTemplate.from_messages([
    ("system", "항공편 관련 질문에 답변해주세요. 항공편 조회, 예약, 체크인, 수하물 등에 대한 정보를 제공할 수 있습니다."),
    ("human", "항공편 질문: {user_input}")
])

def get_flight_node(llm) -> RunnableLambda:
    def _flight(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        
        title_chain = title_prompt | llm
        flight_chain = flight_prompt | llm
        
        def input_generator():
            for char in user_input:
                yield char
        
        def title_generator():
            for chunk in title_chain.stream({"user_input": user_input}):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
        
        def intent_generator():
            for char in "항공편":
                yield char
        
        def response_generator():
            for chunk in flight_chain.stream({"user_input": user_input}):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
        
        full_input, full_title, full_intent, full_response = stream_all_fields_response(
            input_iterator=input_generator(),
            title_iterator=title_generator(),
            intent_iterator=intent_generator(),
            response_iterator=response_generator()
        )
        
        return {
            "input": full_input,
            "title": full_title,
            "intent": full_intent,
            "result": {
                "response": full_response
            }
        }

    return RunnableLambda(_flight)