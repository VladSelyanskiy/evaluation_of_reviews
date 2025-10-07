from pydantic import BaseModel, Field


# Датакласс входа сервиса
class ServiceInput(BaseModel):
    """
    Модель входных данных сервиса.
    Атрибуты:
        reviews: list[str] Список с отзывами
        category: str Категория отзывов, по которой определяется
            какие веса использовать
    """

    # Список содержащий полученные отзывы
    reviews: list[str] = Field(default_factory=list[str])
    # Категория отзывов
    # По умолчанию используются общие веса для модели
    category: str = Field(default="common")
