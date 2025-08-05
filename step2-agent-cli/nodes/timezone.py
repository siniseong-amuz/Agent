from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Dict

class TimezoneOutput(BaseModel):
    title: str
    td: str

parser = PydanticOutputParser(pydantic_object=TimezoneOutput)
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     """     
     {format_instructions}"""),
    ("human", "시차 질문: {original_text}")
])

def get_timezone_node(llm) -> RunnableLambda:
    def _timezone(input_state: Dict) -> Dict:
        original_text = input_state["input"]
        chain = prompt | llm
        response = chain.invoke({
            "original_text": original_text,
            "format_instructions": format_instructions
        })

        try:
            parsed = parser.parse(response.content)
        except Exception:
            parsed = TimezoneOutput(
                title="시차 계산 결과",
                td=response.content.strip()
            )

        return {
            "input": original_text,
            "title": parsed.title,
            "intent": "시차 계산",
            "result": {
            "td": parsed.td
            }
        }

    return RunnableLambda(_timezone)