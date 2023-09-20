"""Модуль, содержащий основные настройки сервиса."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Основные настройки сервиса."""
    MODEL_PATH: str = "model"
    PORT: int = 8000
    HOST: str = '127.0.0.1'


current_settings = Settings()
