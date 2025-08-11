from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_json_response

prompt = ChatPromptTemplate.from_messages([
    ("system", "텍스트를 요약해주세요. 핵심 내용을 간결하고 명확하게 정리해서 제공해주세요."),
    ("human", "요약해주세요: {user_input}")
])

def get_summary_node(llm) -> RunnableLambda:
    def _summary(input_state: Dict) -> Dict:
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
            title="요약",
            intent="요약",
            response_iterator=response_generator()
        )
        
        return {
            "input": user_input,
            "title": "요약",
            "intent": "요약",
            "result": {
                "response": full_response
            }
        }

    return RunnableLambda(_summary)