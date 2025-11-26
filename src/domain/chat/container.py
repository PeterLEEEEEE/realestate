from dependency_injector import containers, providers
from pymongo.asynchronous.database import AsyncDatabase

from src.agents import OrchestratorAgent
from .service import ChatService
from .repository import ChatRepository


class ChatContainer(containers.DeclarativeContainer):
    """Container for chat domain dependencies."""

    session_factory = providers.Dependency()
    mongo_db = providers.Dependency(instance_of=AsyncDatabase)

    # Orchestrator는 AgentContainer에서 주입받음 (Singleton)
    orchestrator = providers.Dependency(instance_of=OrchestratorAgent)

    chat_repository = providers.Factory(
        ChatRepository,
        session_factory=session_factory,
        mongo=mongo_db
    )

    chat_service = providers.Factory(
        ChatService,
        repository=chat_repository,
        orchestrator=orchestrator,
    )