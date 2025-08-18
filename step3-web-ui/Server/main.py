import os
from fastapi import FastAPI
from config.cors import setup_cors, setup_cors_production
from api.newchat import router as newchat_router
from api.chatrooms import router as chatrooms_router
from api.chat import router as chat_router
from api.history import router as history_router
from database.database import init_db


app = FastAPI(
    title="langlanglang-ai API",
    description="amuz project - Agent API (siniseong)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
async def root():
    return {
        "message": "langlanglang-ai API is running",
        "status": "healthy",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.on_event("startup")
async def startup_event():
    await init_db()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

if ENVIRONMENT == "production":
    allowed_origins = [FRONTEND_URL] if FRONTEND_URL else []
    app = setup_cors_production(app, allowed_origins)
else:
    app = setup_cors(app)
app.include_router(newchat_router)
app.include_router(chatrooms_router)
app.include_router(chat_router)
app.include_router(history_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)