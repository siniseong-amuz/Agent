from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    room_id: str
    message: str

class ChatResponse(BaseModel):
    room_id: str
    input: str
    title: str
    intent: str
    result: dict

@router.post(
    "/chat",
    tags=["채팅 (Chat)"],
    summary="대화 입력",
    description="특정 채팅방에서 에이전트와의 대화를 처리합니다.",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):
    try:
        result = await chat_service.process_message(request.message, request.room_id)
        
        response_data = result.get("response", {})
        if isinstance(response_data, str):
            response_data = {"response": response_data}
        
        return ChatResponse(
            room_id=result.get("room_id"),
            input=request.message,
            title=result.get("title", ""),
            intent=result.get("intent", ""),
            result=response_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"처리 중 오류가 발생했습니다: {str(e)}")
