from fastapi import FastAPI
from config.cors import setup_cors
from api.chat import router as chat_router
from api.chat_history import router as chat_history_router
from database.database import init_db


app = FastAPI(
    title="langlanglang-ai API",
    description="amuz project - Agent API (siniseong)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app = setup_cors(app)
app.include_router(chat_router)
app.include_router(chat_history_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)