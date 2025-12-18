import asyncio

from agent import get_agent
from mcp_client import client


def main():
    return asyncio.run(get_agent(client))


agent = main()
