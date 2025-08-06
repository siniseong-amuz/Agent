from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Dict

class SummaryOutput(BaseModel):
    title: str
    summary: str

parser = PydanticOutputParser(pydantic_object=SummaryOutput)
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "{format_instructions}"
    ),
    ("human", "문장 요약: {original_text}")
])

def get_summary_node(llm) -> RunnableLambda:
    def _summary(input_state: Dict) -> Dict:
        original_text = input_state["input"]
        chain = prompt | llm
        response = chain.invoke({
            "original_text": original_text,
            "format_instructions": format_instructions
        })

        try:
            parsed = parser.parse(response.content)
        except Exception:
            summary_text = response.content.strip()
            parsed = SummaryOutput(
                title="요약 결과",
                summary=summary_text
            )

        return {
            "input": original_text,
            "title": parsed.title,
            "intent": "문장 요약",
            "result": {
                "summary": parsed.summary
            }
        }

    return RunnableLambda(_summary)