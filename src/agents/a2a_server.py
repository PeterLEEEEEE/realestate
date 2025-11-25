"""A2A Server for multi-agent real estate service."""

from typing import Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from a2a.types import (
    AgentCard,
    SendMessageRequest,
    SendMessageResponse,
    Message,
    TextPart,
    Part,
)

from src.agents.orchestrator import OrchestratorAgent
from src.agents.property import PropertyAgent
from src.agents.market import MarketAgent
from src.agents.comparison import ComparisonAgent


class AgentServer:
    """A2A compliant agent server."""

    def __init__(self, llm: Any, session_factory: Any):
        self.llm = llm
        self.session_factory = session_factory

        # Initialize agents
        self.orchestrator = OrchestratorAgent(llm, session_factory)
        self.property_agent = PropertyAgent(llm, session_factory)
        self.market_agent = MarketAgent(llm, session_factory)
        self.comparison_agent = ComparisonAgent(llm, session_factory)

        self.agents = {
            "orchestrator": self.orchestrator,
            "property": self.property_agent,
            "market": self.market_agent,
            "comparison": self.comparison_agent,
        }

    def get_router(self) -> APIRouter:
        """Create FastAPI router with A2A endpoints."""
        router = APIRouter(prefix="/a2a", tags=["A2A"])

        @router.get("/agents")
        async def list_agents() -> list[dict]:
            """List all available agents."""
            return [
                {
                    "id": agent_id,
                    "name": agent.config.name,
                    "description": agent.config.description,
                }
                for agent_id, agent in self.agents.items()
            ]

        @router.get("/agents/{agent_id}")
        async def get_agent_card(agent_id: str) -> AgentCard:
            """Get agent card for discovery."""
            agent = self.agents.get(agent_id)
            if not agent:
                return {"error": f"Agent '{agent_id}' not found"}
            return agent.get_agent_card()

        @router.post("/agents/{agent_id}/messages")
        async def send_message(
            agent_id: str,
            request: SendMessageRequest,
        ) -> SendMessageResponse:
            """Send a message to an agent."""
            agent = self.agents.get(agent_id)
            if not agent:
                return SendMessageResponse(
                    message=Message(
                        role="agent",
                        parts=[TextPart(text=f"Agent '{agent_id}' not found")],
                    )
                )

            # Extract text from request
            user_text = ""
            for part in request.message.parts:
                if hasattr(part, "text"):
                    user_text += part.text

            # Get context_id from metadata or generate one
            context_id = request.message.metadata.get("context_id", "default") if request.message.metadata else "default"

            # Invoke agent
            result = await agent.invoke(user_text, context_id)

            # Extract response
            messages = result.get("messages", [])
            response_text = ""
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, "content"):
                    response_text = last_message.content

            return SendMessageResponse(
                message=Message(
                    role="agent",
                    parts=[TextPart(text=response_text)],
                )
            )

        class ChatRequest(BaseModel):
            query: str
            context_id: str = "default"

        @router.post("/chat")
        async def chat(request: ChatRequest) -> dict:
            """Simple chat endpoint using orchestrator."""
            result = await self.orchestrator.invoke(request.query, request.context_id)
            messages = result.get("messages", [])

            response_text = ""
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, "content"):
                    response_text = last_message.content

            return {
                "query": request.query,
                "response": response_text,
                "context_id": request.context_id,
            }

        return router


def create_a2a_router(llm: Any, session_factory: Any) -> APIRouter:
    """Factory function to create A2A router."""
    server = AgentServer(llm, session_factory)
    return server.get_router()
