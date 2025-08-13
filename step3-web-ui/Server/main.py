from fastapi import FastAPI
from config.cors import setup_cors

app = FastAPI(
    title="langlanglang-ai API",
    description="amuz project - Agnet API (siniseong)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app = setup_cors(app)

@app.post("/chat", tags=["프롬프트 입력 (Prompt input)"], summary="대화 입력", description="에이전트와의 대화를 처리합니다.")
async def chat():
    return {"message": "AI Agent API Server"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)