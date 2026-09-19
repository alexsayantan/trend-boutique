import os
from pydantic_settings import BaseSettings

from shared.config import shared_settings

class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/product_db"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    grpc_server_port: int = 50051

    # Inherting or utilizing shared settings could also be done here
    # For now, we mix them if needed or use them separately.

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

settings = Settings()
