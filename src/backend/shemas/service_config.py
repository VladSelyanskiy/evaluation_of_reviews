"""
Модуль настроек приложения.
"""

from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки для модели машинного обучения и API."""

    # Настройки модели машинного обучения
    MODEL_PATH: str = Field(
        default=r"src\backend\models_weights\logistic_regression_classifier.pickle",
        description="Путь к обученной модели",
    )
    CLASS_NAMES: List[str] = Field(
        default=["negative", "positive"],
        description="Названия классов",
    )
    MODEL_VERSION: str = Field(
        default="1.0.0",
        description="Версия модели (для мониторинга)",
    )

    # Настройки API
    API_HOST: str = Field(
        default="0.0.0.0",
        description="Хост API",
    )
    API_PORT: int = Field(
        default=8000,
        description="Порт API",
    )

    # Логирование и мониторинг
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Уровень логирования (DEBUG/INFO/WARNING/ERROR)",
    )
    LOG_FILE: Optional[str] = Field(
        default=None,
        description="Путь к файлу логов (None = вывод в консоль)",
    )


# Создаем конфиг
config = Settings()
