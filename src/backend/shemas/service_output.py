from pydantic import BaseModel, Field


class ServiceOutput(BaseModel):
    """
    Модель выходных данных сервиса.
    Атрибуты:
        class_name (str): Название класса (например, "positive" или "negative").
        class_number (int): Номер класса (например, 0 или 1).
        text (str): Текст отзыва.
    """

    # Название класса (например, "positive" или "negative")
    class_name: str = Field(default="class")
    # Номер класса (например, 0 или 1)
    class_number: int = Field(default=-1)
    # Текст отзыва
    text: str = Field(default="class_text")
