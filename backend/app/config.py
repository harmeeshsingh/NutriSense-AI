from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # GCP
    GCP_PROJECT_ID: str
    
    # Auth
    GOOGLE_CLIENT_ID: str
    
    # AI APIs
    GEMINI_API_KEY: str
    ANTHROPIC_API_KEY: str
    
    # Cache
    REDIS_URL: str = "redis://localhost:6379"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
