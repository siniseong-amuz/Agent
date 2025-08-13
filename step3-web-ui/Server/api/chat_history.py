from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any
from services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatHistoryResponse(BaseModel):
    id: int
    input: str
    intent: str
    title: str
    result: Dict[str, Any]
    created_at: str

@router.get(
    "/chat/history",
    tags=["채팅 히스토리 (Chat History)"],
    summary="채팅 히스토리 조회",
    description="데이터베이스에 저장된 채팅 히스토리를 조회합니다.",
    response_model=List[ChatHistoryResponse]
)
async def get_chat_history(limit: int = Query(10, description="조회할 히스토리 개수", ge=1, le=100)):
    try:
        history = await chat_service.get_chat_history(limit=limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"히스토리 조회 중 오류가 발생했습니다: {str(e)}")
