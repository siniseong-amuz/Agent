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
     """{format_instructions}

    이전 대화 맥락:
    {history}"""
    ),
    ("human", "문장 요약: {original_text}")
])

def get_summary_node(llm) -> RunnableLambda:
    def _summary(input_state: Dict) -> Dict:
        original_text = input_state["input"]
        history_context = input_state.get("history", "")
        chain = prompt | llm
        response = chain.invoke({
            "original_text": original_text,
            "history": history_context,
            "format_instructions": format_instructions
        })

        try:
            parsed = parser.parse(response.content)
        except Exception:
            parsed = SummaryOutput(
                title="요약 결과",
                summary=response.content.strip()
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