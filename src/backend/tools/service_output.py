from pydantic import BaseModel, Field


# Датакласс выхода сервиса
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
    # Начало текста отзыва
    text_beginning: str = Field(default="class_text_beginning")
    # Номер отзыва
    text_number: int = Field(default=0)
    # Вероятность класса
    class_confidence: float = Field(default=-1.0)


# Датакласс списка с выходами сервиса
class ServiceOutputList(BaseModel):
    """
    Модель для нескольких выходных данных сервиса.
    Атрибуты:
        output_list: list[ServiceOutput] Лист c ServiceOutput для нескольких текстов
    """

    # Лист содержащий ServiceOutput для нескольких текстов
    output_list: list[ServiceOutput] = Field(default_factory=list[ServiceOutput])

    class_names: list[str] = Field(default_factory=list[str])
    class_numbers: str = Field(default=list[int])
    model_type: str = Field(default="model_type")
    category: str = Field(default="category")
