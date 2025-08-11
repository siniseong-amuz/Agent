from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_all_fields_response

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 번역 요청을 기반으로 간단한 3-5단어의 제목을 생성하세요. 응답이랑 내용이 중복되지 않도록 하세요."),
    ("human", "{user_input}")
])

translation_prompt = ChatPromptTemplate.from_messages([
    ("system", "번역만 해주세요. 설명이나 추가 정보 없이 번역 결과만 출력하세요."),
    ("human", "번역해주세요: {user_input}") 
])

def get_translation_node(llm) -> RunnableLambda:
    def _translate(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        history_context = input_state.get("history", "")
        
        title_chain = title_prompt | llm
        translation_chain = translation_prompt | llm
        
        def input_generator():
            for char in user_input:
                yield char
        
        def title_generator():
            for chunk in title_chain.stream({"user_input": user_input}):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
        
        def intent_generator():
            for char in "번역":
                yield char
        
        def response_generator():
            for chunk in translation_chain.stream({
                "user_input": user_input,
                "history": history_context
            }):
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

    return RunnableLambda(_translate)