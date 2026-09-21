from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "AI Interview Assessment Platform"

    debug: bool = True

    database_url: str

    jwt_secret_key: str

    qdrant_url: str

    qdrant_api_key: str

    qdrant_collection_name: str

    groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()