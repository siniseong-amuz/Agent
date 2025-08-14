from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatResult(BaseModel):
    response: str

class ChatHistoryResponse(BaseModel):
    input: str
    intent: str
    result: ChatResult

@router.get(
    "/history/{id}",
    tags=["채팅 히스토리 (Chat History)"],
    summary="특정 채팅방의 채팅 히스토리 조회",
    description="특정 채팅방에 저장된 채팅 히스토리를 조회합니다.",
    response_model=List[ChatHistoryResponse]
)
async def get_chat_history(id: str, limit: int = Query(50, description="조회할 히스토리 개수", ge=1, le=100)):
    try:
        history = await chat_service.get_chat_history_by_room(room_id=id, limit=limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"히스토리 조회 중 오류가 발생했습니다: {str(e)}")
