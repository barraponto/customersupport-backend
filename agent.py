from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

system_prompt = """
You are a customer support agent.
You are given a customer query and you need to help the customer with their query.
"""


async def get_agent(client: MultiServerMCPClient):
    tools = await client.get_tools()
    agent = create_agent(
        model="groq:llama-3.1-8b-instant",
        tools=tools,
        system_prompt=system_prompt,
    )
    return agent
