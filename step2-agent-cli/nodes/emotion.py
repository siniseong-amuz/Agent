from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streaming_utils import stream_json_response

prompt = ChatPromptTemplate.from_messages([
    ("system", "텍스트의 감정을 분석해주세요. 감정의 종류, 강도, 이유를 분석하여 상세하게 설명해주세요."),
    ("human", "감정 분석해주세요: {user_input}")
])

def get_emotion_node(llm) -> RunnableLambda:
    def _emotion(input_state: Dict) -> Dict:
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
            title="감정분석",
            intent="감정분석",
            response_iterator=response_generator()
        )
        
        return {
            "input": user_input,
            "title": "감정분석",
            "intent": "감정분석",
            "result": {
                "response": full_response
            }
        }

    return RunnableLambda(_emotion)