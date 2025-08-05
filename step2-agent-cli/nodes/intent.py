from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Dict, Literal

class IntentOutput(BaseModel):
    intent: Literal["translation", "emotion", "timezone", "unknown"]
    confidence: float

parser = PydanticOutputParser(pydantic_object=IntentOutput)
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "사용자의 요청을 자연스럽게 분석해서 가장 적절한 작업 유형을 판단해주세요:"
     "translation: 언어 번역이나 변환을 원하는 경우"
     "emotion: 감정 상태나 기분을 분석하길 원하는 경우"
     "timezone: 국가 간 시차를 계산하거나 묻는 경우"
     
     "{format_instructions}"
    ),
    ("human", "{user_input}")
])

def get_intent_node(llm) -> RunnableLambda:
    def _intent(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        chain = prompt | llm
        response = chain.invoke({
            "user_input": user_input,
            "format_instructions": format_instructions
        })

        try:
            parsed = parser.parse(response.content)
        except Exception:
            parsed = IntentOutput(
                intent="translation",
                confidence=0.5
            )

        return {
            "input": user_input,
            "intent_result": parsed.intent,
            "confidence": parsed.confidence
        }

    return RunnableLambda(_intent)