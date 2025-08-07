from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Dict

class TranslationOutput(BaseModel):
    title: str
    original: str
    translated: str

parser = PydanticOutputParser(pydantic_object=TranslationOutput)
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system", 
    """    
    이전 대화 맥락: {history}
    {format_instructions}"""
    ),
    ("human", "사용자 요청: {original_text}")
])

def get_translation_node(llm) -> RunnableLambda:
    def _translate(input_state: Dict) -> Dict:
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
            parsed = TranslationOutput(
                title="번역 결과",
                original=original_text,
                translated=response.content.strip()
            )

        return {
            "input": original_text,
            "title": parsed.title,
            "intent": "번역",
            "result": {
                "original": parsed.original,
                "translated": parsed.translated
            }
        }

    return RunnableLambda(_translate)