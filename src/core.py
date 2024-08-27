from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore",        
    )

    TOKEN: str
    CHAT_ID: str
    MESSAGE_THREAD_ID: Optional[str]
    REDIS_HOST: str

settings = Settings()