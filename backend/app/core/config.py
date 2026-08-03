from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "btc_sentiment"
    COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"
    GROQ_API_KEY: str
    HUGGINGFACE_API_KEY: str 
    FRONTEND_URL: str="http://localhost:5173"
    SENTIMENT_TTL_DAYS:int=45
    SIGNAL_TTL_BUFFER_HOURS:int=12

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()