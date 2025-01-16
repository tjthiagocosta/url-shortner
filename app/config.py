from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    database_url: str
    api_host: str
    allowed_origins: str

    model_config = ConfigDict(env_file=".env")


settings = Settings()
