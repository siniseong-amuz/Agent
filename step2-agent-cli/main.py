import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from history import HistoryManager
from nodes.translation import get_translation_node
from nodes.emotion import get_emotion_node
from nodes.intent import get_intent_node
from nodes.timezone import get_timezone_node
from nodes.flight import get_flight_node
from nodes.summary import get_summary_node
from nodes.search import get_search_node
from nodes.talk import get_talk_node

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

class GraphState(dict):
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
    "search": "search",
    "talk": "talk"
}

def route(state: GraphState) -> str:
    return ROUTING_MAP.get(state.get("intent_result", "unknown"), "talk")

history_manager = HistoryManager()

builder = StateGraph(GraphState)
builder.add_node("intent", get_intent_node(llm))
builder.add_node("translation", get_translation_node(None))
builder.add_node("emotion", get_emotion_node(None))
builder.add_node("timezone", get_timezone_node(None))
builder.add_node("flight", get_flight_node(None))
builder.add_node("summary", get_summary_node(None))
builder.add_node("search", get_search_node(None))
builder.add_node("talk", get_talk_node(None))
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
    final_result = None

    for update in graph.stream({"input": ques, "history": history_context}):
        for node_name, node_output in update.items():
            if node_name != "intent":
                if isinstance(node_output, dict) and "result" in node_output:
                    if "response" in node_output["result"]:
                        final_result = node_output

    if final_result:
        history_manager.add_history(
            input=ques,
            response=final_result["result"]["response"],
            intent=final_result.get("intent", "")
        )
