from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    POSTGRES_URL: str

    JWT_ACCESS_SECRET: str
    JWT_ACCESS_EXPIRATION_SECONDS: int
    JWT_ACCESS_ALGORITHM: str

    JWT_REFRESH_SECRET: str
    JWT_REFRESH_EXPIRATION_SECONDS: int
    JWT_REFRESH_ALGORITHM: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int


settings = Config()
