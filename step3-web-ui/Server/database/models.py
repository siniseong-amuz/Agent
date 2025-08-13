from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    input = Column(Text, nullable=False)
    result = Column(JSON, nullable=True)
    intent = Column(String(50), nullable=False)
    title = Column(String(200))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "input": self.input,
            "intent": self.intent,
            "title": self.title,
            "result": self.result,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }