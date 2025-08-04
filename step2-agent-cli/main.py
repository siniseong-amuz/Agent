from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
import json, os
from dotenv import load_dotenv
from nodes.translation import get_translation_node

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0)

class GraphState(TypedDict):
    input: str
    title: str
    intent: str
    result: dict

builder = StateGraph(GraphState)
builder.add_node("translation", get_translation_node(llm))
builder.set_entry_point("translation")
builder.set_finish_point("translation")
graph = builder.compile()

while True:
    ques = input("질문을 입력하세요 (종료 q 또는 exit): ").strip()
    if ques.lower() in {"q", "exit"}:
        print("대화를 종료합니다.")
        break

    result = graph.invoke({"input": ques})
    print(json.dumps(result, indent=2, ensure_ascii=False))
