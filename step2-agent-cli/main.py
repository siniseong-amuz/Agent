import os
import json
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from history import HistoryManager
from nodes.translation import get_translation_node
from nodes.emotion import get_emotion_node
from nodes.intent import get_intent_node
from nodes.timezone import get_timezone_node
from nodes.flight import get_flight_node
from nodes.summary import get_summary_node
from nodes.talk import get_talk_node

load_dotenv()

class GraphState(TypedDict):
    input: str
    title: str
    intent: str
    result: dict
    intent_result: str
    confidence: float
    history: str

ROUTING_MAP = {
    "translation": "translation",
    "emotion": "emotion",
    "timezone": "timezone",
    "flight": "flight",
    "summary": "summary",
    "talk": "talk"
}

def route(state: GraphState) -> str:
    return ROUTING_MAP.get(state.get("intent_result", "unknown"), "talk")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)
history_manager = HistoryManager()

builder = StateGraph(GraphState)
builder.add_node("intent", get_intent_node(llm))
builder.add_node("translation", get_translation_node(llm))
builder.add_node("emotion", get_emotion_node(llm))
builder.add_node("timezone", get_timezone_node(llm))
builder.add_node("flight", get_flight_node(llm))
builder.add_node("summary", get_summary_node(llm))
builder.add_node("talk", get_talk_node(llm))
builder.set_entry_point("intent")
builder.add_conditional_edges("intent", route, ROUTING_MAP)

for node in ROUTING_MAP.values():
    builder.set_finish_point(node)

graph = builder.compile()
history_manager.start_new_session()

while True:
    ques = input("질문을 입력하세요 (종료 q 또는 exit): ").strip()
    if ques.lower() in {"q", "exit"}:
        print("대화를 종료합니다.")
        break

    history_context = history_manager.get_recent_context(3)
    
    result = graph.invoke({
        "input": ques,
        "history": history_context
    })
    
    history_manager.add_history(
        input=ques,
        response=result.get("result", {}).get("response", ""),
        intent=result.get("intent", "")
    )
