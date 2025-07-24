from sqlalchemy import Integer, String, Boolean, VARCHAR
from sqlalchemy.sql import expression
from sqlalchemy.orm import Mapped, mapped_column
from src.db.postgres.conn import Base
from src.db.mixins.timestamp_mixin import TimestampMixin
from pydantic import BaseModel


# 실제 메세지는 MongoDB에 저장하고, 상태 정보는 PostgreSQL에 저장

class ChatMessage(BaseModel):
    id: str
    thread_id: str # chatroom_id
    message: str
    sender_type: str  # "human" or "ai"
    sender_id: str # user_id or agent_id
    
class Chat(Base, TimestampMixin):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chatroom_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)  # User ID
    agent_id: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)  # Agent ID (optional)
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        server_default=expression.true()  # default=True
    )
    

class ChatRoom(Base, TimestampMixin):
    __tablename__ = "chat_rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)  # User ID
    agent_id: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)  # Agent ID (optional)
    title: Mapped[str] = mapped_column(String(100), nullable=False, default="Chat Room")
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        server_default=expression.true()  # default=True
    )
    