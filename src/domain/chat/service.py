from typing import Optional
from logger import logger

from src.agents import OrchestratorAgent
from .base import BaseService
from .repository import ChatRepository


class ChatService(BaseService):
    """Chat service using multi-agent orchestrator."""

    def __init__(self, repository: ChatRepository, orchestrator: OrchestratorAgent):
        super().__init__(repository=repository, agent=orchestrator)
        self.orchestrator = orchestrator

    async def invoke_agent(
        self,
        user_input: str,
        chatroom_id: str,
        user_id: Optional[str] = None,
    ):
        """
        Invoke the orchestrator agent with user input.

        Args:
            user_input: User's message
            chatroom_id: Conversation context ID
            user_id: Optional user identifier for tracing

        Returns:
            Agent response with messages
        """
        try:
            # OrchestratorAgent.invoke()가 Langfuse 로깅 자동 처리
            result = await self.orchestrator.invoke(
                query=user_input,
                context_id=chatroom_id,
                user_id=user_id,
            )
            return result
        except Exception as e:
            logger.error(f"Invoke error: {e}")
            return {"messages": [], "error": str(e)}
        
    
    async def add_chatroom(self, user_id: str) -> str:
        """채팅방 생성"""
        logger.info(f"[ChatService] Creating chatroom for user {user_id}")
        return await self.repository.add_chatroom(user_id)

    async def get_chatrooms(self, user_id: str) -> list:
        """사용자의 채팅방 목록 조회"""
        return await self.repository.get_chatrooms(user_id)
