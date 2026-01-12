import os
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings) :
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_SERVER : str
    POSTGRES_PORT : int
    POSTGRES_DB : str
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    GROQ_API_KEY: str
    GEMINI_API_KEY: str
    
    LOG_LEVEL: str = "INFO"
    API_V1_STR: str = "/api/v1"
    
    @property
    def SQLALCHEMY_DATABASE_URL(self) :
        return(f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()