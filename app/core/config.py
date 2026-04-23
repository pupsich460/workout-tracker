from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "Workout_tracker"
    database_url: str = "sqlite+aiosqlite:///./workout_tracker.db"
    secret: str = "SECRET"
    groq_api_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
