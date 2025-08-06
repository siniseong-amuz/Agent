from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
import json, os
from dotenv import load_dotenv
from nodes.translation import get_translation_node
from nodes.emotion import get_emotion_node
from nodes.intent import get_intent_node
from nodes.timezone import get_timezone_node
from nodes.flight import get_flight_node
from nodes.summary import get_summary_node

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0)

class GraphState(TypedDict):
    input: str
    title: str
    intent: str
    result: dict
    intent_result: str
    confidence: float

def route(state: GraphState) -> str:
    intent = state.get("intent_result", "unknown")
    routing_map = {
        "translation": "translation",
        "emotion": "emotion",
        "timezone": "timezone",
        "flight": "flight",
        "summary": "summary"
    }
    return routing_map.get(intent, "translation")

builder = StateGraph(GraphState)
builder.add_node("intent", get_intent_node(llm))
builder.add_node("translation", get_translation_node(llm))
builder.add_node("emotion", get_emotion_node(llm))
builder.add_node("timezone", get_timezone_node(llm))
builder.add_node("flight", get_flight_node(llm))
builder.add_node("summary", get_summary_node(llm))
builder.set_entry_point("intent")
builder.add_conditional_edges(
    "intent",
    route,
    {
        "translation": "translation",
        "emotion": "emotion",
        "timezone": "timezone",
        "flight": "flight",
        "summary": "summary"
    }
)

builder.set_finish_point("translation")
builder.set_finish_point("emotion")
builder.set_finish_point("timezone")
builder.set_finish_point("flight")
builder.set_finish_point("summary")

graph = builder.compile()

while True:
    ques = input("질문을 입력하세요 (종료 q 또는 exit): ").strip()
    if ques.lower() in {"q", "exit"}:
        print("대화를 종료합니다.")
        break

    result = graph.invoke({"input": ques})
    output_result = {k: v for k, v in result.items() if k not in ["intent_result", "confidence"]} # 파이썬 딕셔너리 컴프리헨션 문법 k = 키, v = 값
    print(json.dumps(output_result, indent=2, ensure_ascii=False))