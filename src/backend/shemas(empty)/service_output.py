from pydantic import BaseModel
from enum import Enum


class SentimentClass(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class ServiceOutput(BaseModel):
    class_name: str = "class"
    text: str = "text"
    sentiment: str = SentimentClass
