from langchain_core.messages import HumanMessage
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

def get_translation_node(llm) -> RunnableLambda:
    def _translate(input_state: Dict) -> Dict:
        original_text = input_state["input"]

        prompt = f"""
        아래 문장을 자연스럽게 영어로 번역해줘
        {original_text}
        {format_instructions}
        """.strip()

        response = llm.invoke([HumanMessage(content=prompt)])

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
            "intent": "translation",
            "translation_result": {
                "original": parsed.original,
                "translated": parsed.translated
            }
        }

    return RunnableLambda(_translate)