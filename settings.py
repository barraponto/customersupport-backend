from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    groq_api_key: str = Field(default="")
    shop_mcp_server_url: str = Field(default="")


settings = Settings()
