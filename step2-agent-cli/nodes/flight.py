from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Dict

class FlightOutput(BaseModel):
    title: str
    time: str

parser = PydanticOutputParser(pydantic_object=FlightOutput)
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
     {format_instructions}"""),
    ("human", "비행시간 질문: {original_text}")
])

def get_flight_node(llm) -> RunnableLambda:
    def _flight(input_state: Dict) -> Dict:
        original_text = input_state["input"]
        chain = prompt | llm
        response = chain.invoke({
            "original_text": original_text,
            "format_instructions": format_instructions
        })

        try:
            parsed = parser.parse(response.content)
        except Exception:
            parsed = FlightOutput(
                title="비행시간 계산 결과",
                time=response.content.strip()
            )

        return {
            "input": original_text,
            "title": parsed.title,
            "intent": "비행시간 계산",
            "result": {
                "time": parsed.time
            }
        }

    return RunnableLambda(_flight)