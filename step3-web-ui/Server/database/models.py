from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    chat_history = relationship("ChatHistory", back_populates="room", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("chat_rooms.id"), nullable=False, index=True)
    input = Column(Text, nullable=False)
    result = Column(JSON, nullable=True)
    intent = Column(String(50), nullable=False)
    title = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    room = relationship("ChatRoom", back_populates="chat_history")
    
    def to_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "input": self.input,
            "intent": self.intent,
            "title": self.title,
            "result": self.result,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }