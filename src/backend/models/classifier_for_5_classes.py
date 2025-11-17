# Standard python library imports
import re
import json

# Related third party imports
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Local imports
from tools.service_config import config


class Classifier5cls:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.WEIGHTS_FOR_RT2_5CLASSES_PATH
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            config.WEIGHTS_FOR_RT2_5CLASSES_PATH
        )
        self.re_pattern = re.compile(r"[^А-яЁё]+")

        with open(config.STOPWORDS_FOR_RT2_PATH, "r", encoding="utf-8") as file:
            self.stopwords = set(json.load(file))

    def preprocess_text(self, text):
        # Очистка текста
        text = self.re_pattern.sub(" ", text).lower()
        words = [word for word in text.split() if word not in self.stopwords]
        return " ".join(words)

    def use_model_RT2_for_5_classes(self, text: str) -> tuple[int, float]:
        """класс 0, 1, 2, 3, 4 и уверенность от 0 до 1"""

        text_clear = self.preprocess_text(text)
        # Токенизируем текст и подготавливаем для модели
        inputs = self.tokenizer(
            text_clear,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

        # Подаем на вход модели без вычисления градиентов (только инференс)
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Получаем предсказания
        predicted = torch.nn.functional.softmax(outputs.logits, dim=1)

        # Находим индекс класса с максимальной вероятностью
        predicted_class_idx = predicted.argmax().item()
        sentiment = predicted_class_idx
        confidence = predicted[0][predicted_class_idx].item()

        return sentiment, confidence
