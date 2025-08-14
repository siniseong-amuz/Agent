from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.database import AsyncSessionLocal
from database.models import ChatRoom
import uuid

router = APIRouter()

class ChatRoomResponse(BaseModel):
    id: str
    title: str

@router.post(
    "/newchat",
    tags=["채팅 (Chat)"],
    summary="새 채팅방 생성",
    description="새로운 채팅방을 자동으로 생성합니다. 제목은 'new chat'으로 고정됩니다.",
    response_model=ChatRoomResponse
)
async def create_chatroom():
    try:
        async with AsyncSessionLocal() as session:
            title = "new chat"
            
            chatroom = ChatRoom(
                id=str(uuid.uuid4()),
                title=title
            )
            
            session.add(chatroom)
            await session.commit()
            await session.refresh(chatroom)
            
            return ChatRoomResponse(
                id=chatroom.id,
                title=chatroom.title
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"채팅방 생성 중 오류가 발생했습니다: {str(e)}")
