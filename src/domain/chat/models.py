from sqlalchemy import Integer, String, Boolean, VARCHAR
from sqlalchemy.sql import expression
from sqlalchemy.orm import Mapped, mapped_column
from src.db.postgres.conn import Base
from src.db.mixins.timestamp_mixin import TimestampMixin
from pydantic import BaseModel




class ChatMessage(BaseModel):
    id: str
    thread_id: str # chatroom_id
    message: str
    sender_type: str  # "human" or "ai"
    sender_id: str # user_id or agent_id
    
class Chat(Base, TimestampMixin):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    thread_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)  # User ID
    agent_id: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)  # Agent ID (optional)
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        server_default=expression.true()  # default=True
    )
    
    def __repr__(self) -> str:
        return f"<Chat(id={self.id}, thread_id={self.thread_id}, user_id={self.user_id})>"