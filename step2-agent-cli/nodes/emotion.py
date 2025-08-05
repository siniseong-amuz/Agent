from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Dict

class EmotionOutput(BaseModel):
    title: str
    emotion: str
    confidence: float

parser = PydanticOutputParser(pydantic_object=EmotionOutput)
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "{format_instructions}"
    ),
    ("human", "다음 문장의 감정을 분석해주세요: {original_text}")
])

def get_emotion_node(llm) -> RunnableLambda:
    def _emotion(input_state: Dict) -> Dict:
        original_text = input_state["input"]
        chain = prompt | llm
        response = chain.invoke({
            "original_text": original_text,
            "format_instructions": format_instructions
        })

        try:
            parsed = parser.parse(response.content)
        except Exception:
            parsed = EmotionOutput(
                title="감정 분석 결과",
                emotion="감정 분석 실패",
                confidence=0.0
            )

        return {
            "input": original_text,
            "title": parsed.title,
            "intent": "감정 분석",
            "result": {
                "emotion": parsed.emotion,
                "confidence": parsed.confidence
            }
        }

    return RunnableLambda(_emotion)