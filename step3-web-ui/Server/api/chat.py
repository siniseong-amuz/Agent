from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    id: str
    message: str

class ChatResult(BaseModel):
    response: str

class ChatResponse(BaseModel):
    id: str
    input: str
    intent: str
    result: ChatResult

@router.post(
    "/chat",
    tags=["채팅 (Chat)"],
    summary="대화 입력",
    description="특정 채팅방에서 에이전트와의 대화를 처리합니다.",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):
    try:
        result = await chat_service.process_message(request.message, request.id)
        
        response_data = result.get("response", {})
        if isinstance(response_data, str):
            response_text = response_data
        else:
            response_text = response_data.get("response", "")
        
        return ChatResponse(
            id=result.get("room_id"),
            input=request.message,
            intent=result.get("intent", ""),
            result=ChatResult(response=response_text)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"처리 중 오류가 발생했습니다: {str(e)}")
