from pydantic_settings import BaseSettings


class SharedSettings(BaseSettings):
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


shared_settings = SharedSettings()
