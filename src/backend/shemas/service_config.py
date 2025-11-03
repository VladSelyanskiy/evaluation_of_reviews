"""
Модуль настроек приложения.
"""

import os
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки для моделей машинного обучения и API."""

    # Веса моделей
    LOGISTIC_REGRESSION_CLASSIFIER_PATH: str = Field(
        default=os.path.join(
            "src", "backend", "models_weights", "logistic_regression_classifier.pickle"
        ),
        description="Путь к весам модели логистической регрессии",
    )
    NAIVE_BAYES_CLASSIFIER_PATH: str = Field(
        default=os.path.join(
            "src", "backend", "models_weights", "naive_bayes_classifier.pickle"
        ),
        description="Путь к весам модели наивного байесовского классификатора",
    )

    # Параметры модели
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
        default="127.0.0.1",
        description="Хост API",
    )
    API_PORT: int = Field(
        default=8000,
        description="Порт API",
    )

    # Логирование и мониторинг
    SERVICE_CONFIG_PATH: str = Field(
        default=os.path.join("src", "backend", "shemas", "service_config.py"),
        description="Путь к конфигурации сервиса",
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Уровень логирования (DEBUG/INFO/WARNING/ERROR)",
    )
    LOG_FILE: Optional[str] = Field(
        default=None,
        description="Путь к файлу логов (None = вывод в консоль)",
    )
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Формат логов",
    )

    # База данных
    DATABASE_PATH: str = Field(
        default=os.path.join("src", "backend", "databases", "reviews.db"),
        description="Путь к основной базе данных",
    )


# Создаем конфиг
config = Settings()
