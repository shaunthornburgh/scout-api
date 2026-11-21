from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://scout:scout@localhost:5432/scout"
    api_key: str = "change-me"
    env: str = "development"


settings = Settings()
