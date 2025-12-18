from typing import Any

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import (
    ModelRetryMiddleware,
    SummarizationMiddleware,
    ToolRetryMiddleware,
)
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph.state import CompiledStateGraph

system_prompt = """
You are a customer support agent.
You are given a customer query and you need to help the customer with their query.
Always try to remember the product categories.

If you ever need the user UUID, ask the user to authenticate with email and pin.
Then use that information (email and pin) to get the user UUID.
"""


async def get_agent(client: MultiServerMCPClient):
    tools = await client.get_tools()
    agent = create_agent(
        model="groq:llama-3.1-8b-instant",
        tools=tools,
        system_prompt=system_prompt,
        middleware=[
            ToolRetryMiddleware(max_retries=3),
            ModelRetryMiddleware(max_retries=3),
            SummarizationMiddleware(
                model="groq:llama-3.1-8b-instant",
                trigger=("messages", 12),
                keep=("messages", 4),
            ),
        ],
    )
    return agent


class CustomerSupportAgent:
    def __init__(
        self, agent: CompiledStateGraph[AgentState[Any]], configuration: dict[str, Any]
    ):
        self.agent = agent
        self.configuration = configuration

    async def query(self, prompt: str):
        try:
            response = await self.agent.ainvoke(
                {"messages": [{"role": "user", "content": prompt}]}, self.configuration
            )
        except Exception:
            return (
                "Sorry, I'm having trouble processing your request. Please try again."
            )

        return response["messages"][-1].content
