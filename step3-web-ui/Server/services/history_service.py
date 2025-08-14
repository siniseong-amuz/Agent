from database.database import AsyncSessionLocal
from database.models import ChatHistory, ChatRoom
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Dict, Any


class HistoryService:
    def __init__(self):
        pass
    
    def _format_response_text(self, record: ChatHistory) -> str:
        result_data = record.result
        
        if not isinstance(result_data, dict):
            return str(result_data) if result_data else ""
        
        if record.intent == "번역":
            return result_data.get("translation", "")
        elif record.intent == "emotion":
            emotion = result_data.get("emotion", "")
            message = result_data.get("message", "")
            return f"{emotion} - {message}" if emotion and message else emotion or message
        else:
            return result_data.get("response", "")
    
    async def get_recent_context(self, room_id: str, count: int = 5) -> str:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ChatHistory)
                .where(ChatHistory.room_id == room_id)
                .order_by(ChatHistory.created_at.desc())
                .limit(count)
            )
            records = result.scalars().all()
            
            if not records:
                return ""
            
            context_parts = []
            for record in reversed(records):
                context_parts.append(f"사용자: {record.input}")
                response_text = self._format_response_text(record)
                context_parts.append(f"AI: {response_text}")
            
            return "\n".join(context_parts)
    
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
            await session.flush()
            
            if title and title.strip():
                await self._update_chatroom_title_if_first_message(session, room_id, title)
            
            await session.commit()
            await session.refresh(chat_record)
            return chat_record
    
    async def _update_chatroom_title_if_first_message(self, session, room_id: str, title: str):
        count_result = await session.execute(
            select(func.count(ChatHistory.id)).where(ChatHistory.room_id == room_id)
        )
        message_count = count_result.scalar()
        
        if message_count == 1:
            chatroom_result = await session.execute(
                select(ChatRoom).where(ChatRoom.id == room_id)
            )
            chatroom = chatroom_result.scalar_one_or_none()
            if chatroom and chatroom.title == "new chat":
                chatroom.title = title
    
    async def get_chat_history_by_room(self, room_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ChatHistory)
                .where(ChatHistory.room_id == room_id)
                .order_by(ChatHistory.created_at.asc())
                .limit(limit)
            )
            
            records = []
            for record in result.scalars().all():
                result_data = record.result
                if isinstance(result_data, str):
                    result_data = {"response": result_data}
                
                records.append({
                    "input": record.input,
                    "intent": record.intent,
                    "result": result_data
                })
            
            return records