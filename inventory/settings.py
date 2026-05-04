from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    service_host: str = "0.0.0.0"
    service_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
