import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'step2-agent-cli'))

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from nodes.translation import get_translation_node
from nodes.emotion import get_emotion_node
from nodes.intent import get_intent_node
from nodes.timezone import get_timezone_node
from nodes.flight import get_flight_node
from nodes.summary import get_summary_node
from nodes.search import get_search_node
from nodes.talk import get_talk_node
from database.database import AsyncSessionLocal
from database.models import ChatRoom
from sqlalchemy.future import select
from services.history_service import HistoryService

load_dotenv()

class GraphState(dict):
    input: str
    title: str
    intent: str
    result: dict
    intent_result: str
    confidence: float
    history: str

class ChatService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )
        self.history_service = HistoryService()
        
        self.ROUTING_MAP = {
            "translation": "translation",
            "emotion": "emotion",
            "timezone": "timezone",
            "flight": "flight",
            "summary": "summary",
            "search": "search",
            "talk": "talk"
        }
        
        self.graph = self._build_graph()
    
    def _route(self, state: GraphState) -> str:
        return self.ROUTING_MAP.get(state.get("intent_result", "unknown"), "talk")
    
    def _build_graph(self):
        builder = StateGraph(GraphState)
        builder.add_node("intent", get_intent_node(self.llm))
        builder.add_node("translation", get_translation_node(None))
        builder.add_node("emotion", get_emotion_node(None))
        builder.add_node("timezone", get_timezone_node(None))
        builder.add_node("flight", get_flight_node(None))
        builder.add_node("summary", get_summary_node(None))
        builder.add_node("search", get_search_node(None))
        builder.add_node("talk", get_talk_node(None))
        builder.set_entry_point("intent")
        builder.add_conditional_edges("intent", self._route, self.ROUTING_MAP)
        for node in self.ROUTING_MAP.values():
            builder.set_finish_point(node)
        
        return builder.compile()
    
    async def process_message(self, message: str, room_id: str):
        await self.verify_chatroom_exists(room_id)
        
        history_context = await self.history_service.get_recent_context(room_id, 5)
        final_result = None
        
        for update in self.graph.stream({"input": message, "history": history_context}):
            for node_name, node_output in update.items():
                if node_name != "intent":
                    if isinstance(node_output, dict) and "result" in node_output:
                        final_result = node_output
        
        if final_result:
            intent = final_result.get("intent", "")
            result_data = final_result["result"]
            
            if isinstance(result_data, dict) and ("original" in result_data and "translation" in result_data):
                response_data = {
                    "type": "translation",
                    "original": result_data.get("original", ""),
                    "translation": result_data.get("translation", "")
                }
                response_text = f"원문: {result_data.get('original', '')}\n번역문: {result_data.get('translation', '')}"
            elif isinstance(result_data, dict) and ("message" in result_data or "confidence" in result_data or intent in {"emotion", "감정 분석"}):
                response_data = {
                    "emotion": result_data.get("response", ""),
                    "message": result_data.get("message", ""),
                    "confidence": result_data.get("confidence", "")
                }
                response_text = f"{result_data.get('response', '')} - {result_data.get('message', '')} ({result_data.get('confidence', '')})"
            else:
                response_data = result_data.get("response", result_data)
                response_text = result_data.get("response", "") if isinstance(result_data, dict) else str(result_data)
            
            chat_record = await self.history_service.save_to_database(
                room_id=room_id,
                input=message,
                intent=intent,
                title=final_result.get("title", ""),
                result=response_data
            )
            
            return {
                "id": chat_record.id,
                "room_id": room_id,
                "title": final_result.get("title", ""),
                "intent": intent,
                "response": response_data,
                "created_at": chat_record.created_at.isoformat()
            }
        
        return {
            "id": None,
            "room_id": room_id,
            "title": "",
            "intent": "error",
            "response": "error...",
            "created_at": ""
        }
    
    async def verify_chatroom_exists(self, room_id: str):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ChatRoom).where(ChatRoom.id == room_id)
            )
            chatroom = result.scalar_one_or_none()
            if not chatroom:
                raise ValueError(f"채팅방 {room_id}를 찾을 수 없습니다.")
    
    async def get_chat_history_by_room(self, room_id: str, limit: int = 50):
        return await self.history_service.get_chat_history_by_room(room_id, limit)