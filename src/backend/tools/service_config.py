# Standard python library imports
import os
from typing import Optional, List

# Related third party imports
from pydantic import Field
from pydantic_settings import BaseSettings


# Модуль настроек приложения
class Settings(BaseSettings):
    """Настройки для моделей машинного обучения и API."""

    # Пути к весам моделей
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
    LSTM_FOR_2_ClASSES_CLASSIFIER_PATH: str = Field(
        default=os.path.join(
            "src", "backend", "models_weights", "LSTM_model_2nd_class.h5"
        ),
        description="Путь к весам LSTM модели для двух классов",
    )
    TOKENIZER_FOR_LSTM2CLASSES_PATH: str = Field(
        default=os.path.join(
            "src", "backend", "models_weights", "2nd_class_tokenizer.pickle"
        ),
        description="Путь к токенизатору для LSTM модели 2 классов",
    )
    WEIGHTS_FOR_RT2_3CLASSES_PATH: str = Field(
        default=os.path.join("src", "backend", "models_weights", "model_RT2_3_classes"),
        description="Путь к папке с весами и токенизатором модели для трех классов",
    )

    # Параметры модели двух классов
    MODELS_FOR_2_CLASSES: list[str] = Field(
        default=["naive_bayes", "log_reg", "lstm"],
        description="Названия моделей для классификации двух классов",
    )
    MODELS_FOR_3_CLASSES: list[str] = Field(
        default=["rt_2"],
        description="Названия моделей для классификации трех классов",
    )
    CLASS_NAMES: List[str] = Field(
        default=["negative", "positive"],
        description="Названия классов двух типов",
    )
    CLASS_THRESHOLD: float = Field(
        default=0.5,
        description="Порог для классификации",
    )
    CLASS_3_NAMES: List[str] = Field(
        default=["negative", "neutral", "positive"],
        description="Названия классов трех типов",
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

    # Параметр размера выходного текста
    NUMBER_OF_FIRST_CHAR: int = Field(
        default=13,
        description="Количество первых символов в выходном тексте",
    )

    # База данных
    DATABASE_PATH: str = Field(
        default=os.path.join("src", "backend", "databases", "reviews.db"),
        description="Путь к основной базе данных",
    )


# Создаем конфиг
config = Settings()
