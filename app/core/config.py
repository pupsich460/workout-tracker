from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    # Общие настройки приложения
    app_title: str = "Workout_tracker"
    version: str = "0.1.0"
    description: str = "API для отслеживания тренировок и прогресса"

    # Настройки базы данных
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Секретные ключи и токены
    secret: str
    groq_api_key: str
    bot_token: str
    api_url: str = "http://127.0.0.1:8000"
    SQL_ECHO: bool = False
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @property
    def database_url(self) -> str:
        """Сформировать URL для подключения к базе данных."""
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
