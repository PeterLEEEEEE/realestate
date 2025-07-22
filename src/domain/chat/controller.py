from fastapi.responses import StreamingResponse
from logger import logger
from fastapi import APIRouter, Depends, HTTPException, status,Body
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from src.core.config import get_config
from src.core.agent.langgraph.agent import RealEstateAgent
from .service import ChatService
from .container import ChatContainer

chat_router = APIRouter(tags=["Chat"], prefix="/chat")


class ChatInput(BaseModel):
    message: str

@chat_router.post("/{chatroom_id}/invoke")
@inject
async def invoke(
    chatroom_id: str,
    user_input: ChatInput, 
    chat_service: ChatService = Depends(Provide["chat_container.chat_service"])
):
    """
    Invoke the agent with the given user input and chatroom ID.
    """
    
    try:
        response = await chat_service.invoke_agent(user_input.message, chatroom_id)
        # async def event_stream():
        #     try:
        #         async for response in agent.graph.astream({"messages": inputs}, config=memory_config, stream_mode=["custom"]):
        #             # Yield the response as a server-sent event
        #             yield f"data: {response}\n\n"                    
        #             # for value in response.values():
        #             #     value["messages"][-1].pretty_print()
        #     except Exception as e:
        #         yield f"data: Error occurred: {str(e)}\n\n"
        
        return response["messages"][-1].content
        
        # return StreamingResponse(
        #     event_stream(),
        #     media_type="text/event-stream",
        # )
        # Call the invoke_agent method from the repository
        # yield await chat_service.invoke_agent(user_input, chatroom_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@chat_router.delete("/{chatroom_id}")
@inject
async def delete_chatroom(
    chatroom_id: str,
    chat_service: ChatService = Depends(Provide["chat_container.chat_service"])
):
    """
    Delete the chatroom with the given ID.
    """
    try:
        # Call the delete_chatroom method from the repository
        await chat_service.delete_chatroom(chatroom_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@chat_router.post("/new")
@inject
async def create_chatroom(
    user_id: str,
    chat_service: ChatService = Depends(Provide["chat_container.chat_service"])
):
    """
    Create a new chatroom for the user.
    """
    logger.info(f"Creating chatroom for user {user_id}")
    try:
        # Call the add_chatroom method from the repository
        return await chat_service.add_chatroom(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@chat_router.get("/{chatroom_id}")
@inject
async def get_chat_history(
    chatroom_id: str,
    chat_service: ChatService = Depends(Provide["chat_container.chat_service"])
):
    """
    Get the chat history for the given chatroom ID.
    """
    try:
        # Call the get_chat_history method from the repository
        chat_history = await chat_service.get_chat_history(chatroom_id)
        return chat_history
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )