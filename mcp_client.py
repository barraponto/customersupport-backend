from langchain_mcp_adapters.client import MultiServerMCPClient

from settings import settings


def get_client(url: str | None = None):
    return MultiServerMCPClient(
        {
            "shop": {
                "transport": "http",
                "url": url or settings.shop_mcp_server_url,
            }
        }
    )
