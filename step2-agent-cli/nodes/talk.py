from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_json_response

prompt = ChatPromptTemplate.from_messages([
    ("system",
     """자연스럽게 대화하세요. 간단하고 직접적으로 답변해주세요.

    이전 대화 맥락:
    {history}"""
    ),
    ("human", "{user_input}")
])

def get_talk_node(llm) -> RunnableLambda:
    def _talk(input_state: Dict) -> Dict:
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
            title="일상대화", 
            intent="일상대화",
            response_iterator=response_generator()
        )
        
        return {
            "input": user_input,
            "title": "일상대화",
            "intent": "일상대화",
            "result": {
                "response": full_response
            }
        }

    return RunnableLambda(_talk)