from pydantic import BaseModel, Field


class ServiceOutput(BaseModel):
    # Название класса (например, "positive" или "negative")
    class_name: str = Field("class")
    # Номер класса (например, 0 или 1)
    class_number: int = Field(-1)
    # Текст отзыва
    text: str = Field("class_text")
