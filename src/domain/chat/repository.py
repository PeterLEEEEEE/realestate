import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pymongo.asynchronous.database import AsyncDatabase

from .base import BaseAlchemyRepository
from .models import ChatMessage, Chat


class ChatRepository(BaseAlchemyRepository[Chat]):
    
    def __init__(self, session_factory: AsyncSession, mongo: AsyncDatabase):
        super().__init__(model=ChatMessage, session_factory=session_factory)
        self.chats = mongo['chats']
        
    async def invoke_agent(self, agent_id: str):
        ...
    
    async def save_checkpoint(self, checkpoint: str) -> None:
        async with self.session_factory() as session:
            session.add(checkpoint)
            await session.commit()
            await session.refresh(checkpoint)
    
    async def get_chat_history(self, user_id: str, chatroom_id: str) -> list:
        async with self.session_factory() as session:
            query = select(ChatMessage).where(
                ChatMessage.user_id == user_id,
                ChatMessage.chatroom_id == chatroom_id
            )
            result = await session.execute(query)
            return result.scalars().all()

    
    async def add_chatroom(self, user_id: str) -> str:
        """채팅방 생성 후 room_id 반환"""
        chatroom_id = str(uuid.uuid4())

        chatroom_model = {
            "chatroom_id": chatroom_id,
            "user_id": user_id,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "metadata": {
                "message_count": 0,
                "last_activity": datetime.now()
            }
        }

        try:
            await self.chats.insert_one(chatroom_model)
            return chatroom_id
        except Exception as e:
            raise Exception(f"Failed to create chatroom: {str(e)}")

    async def get_chatrooms(self, user_id: str) -> list:
        """사용자의 채팅방 목록 조회"""
        try:
            cursor = self.chats.find(
                {"user_id": user_id, "is_active": True},
                {"_id": 0, "chatroom_id": 1, "created_at": 1, "updated_at": 1, "metadata": 1}
            ).sort("updated_at", -1)
            return await cursor.to_list(length=100)
        except Exception as e:
            raise Exception(f"Failed to get chatrooms: {str(e)}")