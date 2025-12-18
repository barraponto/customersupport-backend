from langchain_mcp_adapters.client import MultiServerMCPClient

from settings import settings

client = MultiServerMCPClient(
    {
        "shop": {
            "transport": "http",
            "url": settings.shop_mcp_server_url,
        }
    }
)
