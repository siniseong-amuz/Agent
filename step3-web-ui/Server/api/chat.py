from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    input: str
    title: str
    intent: str
    result: dict

@router.post(
    "/chat",
    tags=["프롬프트 입력 (Prompt input)"],
    summary="대화 입력",
    description="에이전트와의 대화를 처리합니다.",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):
    try:
        result = await chat_service.process_message(request.message)
        return ChatResponse(
            input=request.message,
            title=result.get("title", ""),
            intent=result.get("intent", ""),
            result={"response": result.get("response", "")}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"처리 중 오류가 발생했습니다: {str(e)}")