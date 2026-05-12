from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://verifypk:verifypk123@db:5432/verifypk"
    REDIS_URL: str = "redis://:redis123@redis:6379/0"
    CELERY_BROKER_URL: str = "amqp://verifypk:rabbit123@rabbitmq:5672/"

    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_USER: str = "verifypk"
    MINIO_PASS: str = "minio123456"
    MINIO_BUCKET: str = "verifypk-media"

    MODELS_PATH: str = "/models"
    INSIGHTFACE_MODEL: str = "buffalo_l"
    LIVENESS_THRESHOLD: float = 0.6
    FACE_MATCH_THRESHOLD: float = 0.4
    LIVENESS_SCORE_THRESHOLD: float = 0.7

    API_KEY_PREFIX_LIVE: str = "live_pk_"
    API_KEY_PREFIX_TEST: str = "test_pk_"

    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
