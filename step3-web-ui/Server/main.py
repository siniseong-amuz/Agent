from fastapi import FastAPI
from config.cors import setup_cors
from api.chat import router as chat_router


app = FastAPI(
    title="langlanglang-ai API",
    description="amuz project - Agent API (siniseong)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app = setup_cors(app)
app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)