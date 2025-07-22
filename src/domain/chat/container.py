from dependency_injector import containers, providers
from pymongo.asynchronous.database import AsyncDatabase
from src.core.agent.langgraph.agent import RealEstateAgent
from src.db.mongo.checkpointer import CustomMongoDBSaver
from .service import ChatService
from .repository import ChatRepository



class ChatContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    mongo_db = providers.Dependency(instance_of=AsyncDatabase)
    llm = providers.Dependency()
    
    mongo_checkpointer = providers.Factory(
        CustomMongoDBSaver,
        conn=mongo_db,
        collection_name="chat_checkpoints"
    )
    
    real_estate_agent = providers.Factory(
        RealEstateAgent,
        llm=llm,
        checkpointer=mongo_checkpointer
        # checkpointer=None
    )
    
    chat_repository = providers.Factory(
        ChatRepository,
        session_factory=session_factory,
        mongo=mongo_db
    )
    
    chat_service = providers.Factory(
        ChatService,
        repository=chat_repository,
        agent=real_estate_agent,
    )