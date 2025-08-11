from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_all_fields_response

title_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 요약 요청을 기반으로 3-5단어의 간단한 제목을 생성하세요. 응답이랑 내용이 중복되지 않도록 하세요."),
    ("human", "{user_input}")
])

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "텍스트를 요약해주세요. 핵심 내용을 간결하고 명확하게 정리해서 제공해주세요."),
    ("human", "요약해주세요: {user_input}")
])

def get_summary_node(llm) -> RunnableLambda:
    def _summary(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        history_context = input_state.get("history", "")
        
        title_chain = title_prompt | llm
        summary_chain = summary_prompt | llm
        
        def input_generator():
            for char in user_input:
                yield char
        
        def title_generator():
            for chunk in title_chain.stream({"user_input": user_input}):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
        
        def intent_generator():
            for char in "요약":
                yield char
        
        def response_generator():
            for chunk in summary_chain.stream({
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

    return RunnableLambda(_summary)