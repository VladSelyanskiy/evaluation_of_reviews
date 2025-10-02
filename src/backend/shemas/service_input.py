from pydantic import BaseModel, Field


# Датакласс входа сервиса
class ServiceInput(BaseModel):
    """
    Модель входных данных сервиса.
    Атрибуты:
        reviews: list[str] Список с отзывами
    """

    reviews: list[str] = Field(default_factory=list)
