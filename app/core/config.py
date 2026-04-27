from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "Workout_tracker"
    database_url: str = "sqlite+aiosqlite:///./workout_tracker.db"
    secret: str = "SECRET"
    groq_api_key: str
    bot_token: str
    api_url: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
