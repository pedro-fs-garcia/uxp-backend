from pydantic_settings import BaseSettings
from typing import Optional # Importe Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"

    # Variáveis do Banco de Dados
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    # Variáveis JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        # Para compatibilidade com Pydantic V1, caso necessário no futuro
        # env_file_encoding = 'utf-8'

settings = Settings()