from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET_KEY: str
    ENCRYPTION_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()