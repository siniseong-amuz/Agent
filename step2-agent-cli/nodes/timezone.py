from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_all_fields_response

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 시간대 질문을 기반으로 3-5단어의 간단한 제목을 생성하세요. 응답이랑 내용이 중복되지 않도록 하세요."),
    ("human", "{user_input}")
])

timezone_prompt = ChatPromptTemplate.from_messages([
    ("system", "시간대 관련 질문에 답변해주세요. 현재 시간, 다른 나라 시간, 시간대 변환 등을 도움을 드릴 수 있습니다."),
    ("human", "시간대 질문: {user_input}")
])

def get_timezone_node(llm) -> RunnableLambda:
    def _timezone(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        
        title_chain = title_prompt | llm
        timezone_chain = timezone_prompt | llm
        
        def input_generator():
            for char in user_input:
                yield char
        
        def title_generator():
            for chunk in title_chain.stream({"user_input": user_input}):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
        
        def intent_generator():
            for char in "시간대":
                yield char
        
        def response_generator():
            for chunk in timezone_chain.stream({"user_input": user_input}):
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

    return RunnableLambda(_timezone)