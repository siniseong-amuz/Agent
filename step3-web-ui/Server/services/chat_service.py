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
from database.models import ChatHistory, ChatRoom
from sqlalchemy.future import select

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
        
        final_result = None
        
        for update in self.graph.stream({"input": message, "history": ""}):
            for node_name, node_output in update.items():
                if node_name != "intent":
                    if isinstance(node_output, dict) and "result" in node_output:
                        final_result = node_output
        
        if final_result:
            intent = final_result.get("intent", "")
            result_data = final_result["result"]
            
            if intent == "번역":
                response_data = {
                    "original": result_data.get("original", ""),
                    "translation": result_data.get("translation", "")
                }
                response_text = result_data.get("translation", "")
            elif intent == "emotion":
                response_data = {
                    "emotion": result_data.get("response", ""),
                    "message": result_data.get("message", "")
                }
                response_text = f"{result_data.get('response', '')} - {result_data.get('message', '')}"
            else:
                response_data = result_data.get("response", "")
                response_text = result_data.get("response", "")
            
            chat_record = await self.save_to_database(
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
    
    async def save_to_database(self, room_id: str, input: str, intent: str, title: str = "", result: dict = None):
        async with AsyncSessionLocal() as session:
            chat_record = ChatHistory(
                room_id=room_id,
                input=input,
                intent=intent,
                title=title,
                result=result
            )
            session.add(chat_record)
            await session.commit()
            await session.refresh(chat_record)
            
            chatroom_result = await session.execute(
                select(ChatRoom).where(ChatRoom.id == room_id)
            )
            chatroom = chatroom_result.scalar_one()
            await session.commit()
            
            return chat_record
    
    async def get_chat_history_by_room(self, room_id: str, limit: int = 50):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ChatHistory)
                .where(ChatHistory.room_id == room_id)
                .order_by(ChatHistory.created_at.asc())
                .limit(limit)
            )
            return [record.to_dict() for record in result.scalars().all()]