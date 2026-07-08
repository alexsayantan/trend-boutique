from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "cart-service"
    app_version: str = "0.1.0"
    debug: bool = True
    environment: str = "development"

    postgres_user: str = "trend"
    postgres_password: str = "trend"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "trend_bouttique"

    database_url: str | None = None

    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    @property
    def db_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_url_sync(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
