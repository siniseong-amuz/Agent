from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class Response(BaseModel):
    title: str
    summary: str
    keywords: list[str]

parser = PydanticOutputParser(pydantic_object=Response)
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([ # ChatPromptTemplate - 역할 분리가 가능
    ("system", 
     "당신은 전문적인 정보 요약가입니다. "
     "사용자의 질문에 대해 반드시 JSON 형식으로 응답하세요. "
     "필드는 'title', 'summary', 'keywords'만 포함해야 하며, JSON 외 텍스트는 절대 포함하지 마세요.\n"
     "{format_instructions}"
    ),
    ("human", "{ques}")
])

llm = ChatOllama(model="llama3.1:8b", temperature=0)

ques = input("질문을 입력하세요: ")
formatted_prompt = prompt.format_messages(ques=ques, format_instructions=format_instructions)

output = llm.invoke(formatted_prompt)

answer = parser.parse(output.content)
print(answer.model_dump_json(indent=2))
