from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database.database import AsyncSessionLocal
from database.models import ChatRoom
from sqlalchemy.future import select

router = APIRouter()

class ChatRoomResponse(BaseModel):
    id: str
    title: str

@router.get(
    "/chatrooms",
    tags=["채팅방 관리 (Chatroom Management)"],
    summary="채팅방 목록 조회",
    description="모든 채팅방 목록을 조회합니다.",
    response_model=List[ChatRoomResponse]
)
async def get_chatrooms():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ChatRoom).order_by(ChatRoom.created_at.desc())
            )
            chatrooms = result.scalars().all()
            
            return [
                ChatRoomResponse(
                    id=room.id,
                    title=room.title
                )
                for room in chatrooms
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"채팅방 목록 조회 중 오류가 발생했습니다: {str(e)}")

@router.delete(
    "/chatrooms/{id}",
    tags=["채팅방 관리 (Chatroom Management)"],
    summary="채팅방 삭제",
    description="특정 채팅방과 관련된 모든 메시지를 삭제합니다.",
)
async def delete_chatroom(id: str):
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ChatRoom).where(ChatRoom.id == id)
            )
            chatroom = result.scalar_one_or_none()
            
            if not chatroom:
                raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다.")
            
            await session.delete(chatroom)
            await session.commit()
            
            return {"message": "채팅이 삭제되었습니다."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"채팅방 삭제 중 오류가 발생했습니다: {str(e)}")
