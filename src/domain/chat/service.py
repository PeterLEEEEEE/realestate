import uuid
from typing import Optional
from logger import logger
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
# from langmem.short_term import SummarizationNode, RunningSummary
from src.core.agent.langgraph.agent import RealEstateAgent
from .base import BaseService
from .repository import ChatRepository


class ChatService(BaseService):    
    def __init__(self, repository: ChatRepository, agent: RealEstateAgent):
        super().__init__(repository=repository, agent=agent)
        
    async def invoke_agent(self, user_input: str, chatroom_id: str):
        memory_config = RunnableConfig(
            recursion_limit=5, # 순환 방지, 최대 5개의 노드까지 방문
            configurable={"thread_id": chatroom_id} # 이게 유지되면 멀티턴 대화 가능
        )

        graph = self.agent.get_graph()

        messages = {"messages": [HumanMessage(content=user_input)]}
        # result = await graph.ainvoke(messages, config=memory_config)
        # return result
        try:
            result = await graph.ainvoke(messages, config=memory_config)
            return result
        except Exception as e:
            print(f"Invoke error: {e}")
            # 에러 시 현재 상태 반환
            final_state = await graph.aget_state(memory_config)
            return {"messages": final_state.values.get("messages", [])}
        
    
    async def add_chatroom(self, user_id: int):
        
        """
        Create a new chatroom for the user.
        """
        logger.info(f"[ChatService] Creating chatroom for user {user_id}")
        chatroom = await self.repository.add_chatroom(user_id)
        return {
            "user_id": chatroom.get("user_id"),
            "chatroom_id": chatroom.get("chatroom_id")
        }
    
    