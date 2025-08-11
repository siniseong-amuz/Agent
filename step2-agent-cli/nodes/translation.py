from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_json_response

prompt = ChatPromptTemplate.from_messages([
    ("system", "번역만 해주세요. 설명이나 추가 정보 없이 번역 결과만 출력하세요."),
    ("human", "번역해주세요: {user_input}")
])

def get_translation_node(llm) -> RunnableLambda:
    def _translate(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        history_context = input_state.get("history", "")
        
        chain = prompt | llm
        
        def response_generator():
            for chunk in chain.stream({
                "user_input": user_input,
                "history": history_context
            }):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
        
        full_response = stream_json_response(
            user_input=user_input,
            title="번역",
            intent="번역",
            response_iterator=response_generator()
        )
        
        return {
            "input": user_input,
            "title": "번역",
            "intent": "번역",
            "result": {
                "response": full_response
            }
        }

    return RunnableLambda(_translate)