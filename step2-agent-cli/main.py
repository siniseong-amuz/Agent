from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
# from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
load_dotenv()

class Response(BaseModel):
    title: str
    content: str

# parser = PydanticOutputParser(pydantic_object=Response)
# format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "당신은 전문적인 정보 요약가입니다. "
     "필드는 'title', 'content'만 포함해주세요."
    ),
    ("human", "{ques}")
])

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0)

structured_llm = llm.with_structured_output(Response)

ques = input("질문을 입력하세요: ")
formatted_prompt = prompt.format_messages(ques=ques)

# output = llm.invoke(formatted_prompt)

answer = structured_llm.invoke(formatted_prompt)
print(answer.model_dump_json(indent=2))