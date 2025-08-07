from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Dict

class TalkOutput(BaseModel):
    title: str
    response: str

parser = PydanticOutputParser(pydantic_object=TalkOutput)
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     """자연스럽게 대화하세요.

    {format_instructions}

    이전 대화 맥락:
    {history}"""
    ),
    ("human", "{user_input}")
])

def get_talk_node(llm) -> RunnableLambda:
    def _talk(input_state: Dict) -> Dict:
        user_input = input_state["input"]
        history_context = input_state.get("history", "")
        chain = prompt | llm
        response = chain.invoke({
            "user_input": user_input,
            "history": history_context,
            "format_instructions": format_instructions
        })

        try:
            parsed = parser.parse(response.content)
        except Exception:
            parsed = TalkOutput(
                title="일상대화",
                response=response.content
            )

        return {
            "input": user_input,
            "title": parsed.title,
            "intent": "일상대화",
            "result": {
                "response": parsed.response
            }
        }

    return RunnableLambda(_talk)