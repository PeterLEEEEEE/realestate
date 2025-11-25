from abc import ABC, abstractmethod
from typing import Any, AsyncIterator
from dataclasses import dataclass

from a2a.types import AgentCard, AgentCapabilities, AgentSkill


@dataclass
class AgentConfig:
    name: str
    description: str
    version: str = "1.0.0"


class BaseAgent(ABC):
    """Base class for all A2A agents."""

    def __init__(self, config: AgentConfig, llm: Any):
        self.config = config
        self.llm = llm
        self._graph = None

    @abstractmethod
    def get_tools(self) -> list:
        """Return list of tools available to this agent."""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    def get_graph(self):
        """Lazy initialization of the agent graph."""
        if self._graph is None:
            from langgraph.prebuilt import create_react_agent
            self._graph = create_react_agent(
                self.llm,
                tools=self.get_tools(),
                prompt=self.get_system_prompt(),
            )
        return self._graph

    async def invoke(self, query: str, context_id: str) -> dict:
        """Invoke the agent with a query."""
        graph = self.get_graph()
        config = {"configurable": {"thread_id": context_id}}
        result = await graph.ainvoke({"messages": [("user", query)]}, config=config)
        return result

    async def stream(self, query: str, context_id: str) -> AsyncIterator[dict]:
        """Stream responses from the agent."""
        graph = self.get_graph()
        config = {"configurable": {"thread_id": context_id}}
        async for chunk in graph.astream(
            {"messages": [("user", query)]},
            config=config,
            stream_mode="updates"
        ):
            yield chunk

    def get_agent_card(self) -> AgentCard:
        """Return A2A agent card for discovery."""
        return AgentCard(
            name=self.config.name,
            description=self.config.description,
            version=self.config.version,
            capabilities=AgentCapabilities(streaming=True),
            skills=[
                AgentSkill(
                    id=self.config.name.lower().replace(" ", "_"),
                    name=self.config.name,
                    description=self.config.description,
                )
            ],
        )
