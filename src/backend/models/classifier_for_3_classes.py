import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from tools.service_config import config


class Classifier3cls:

    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.WEIGHTS_FOR_RT2_3CLASSES_PATH
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            config.WEIGHTS_FOR_RT2_3CLASSES_PATH
        )

    def use_model_RT2(
        self, text: str
    ) -> tuple[int, float]:  # класс 0, 1, 2 и уверенность от 0 до 1
        # Токенизируем текст и подготавливаем для модели
        inputs = self.tokenizer(
            text, max_length=512, padding=True, truncation=True, return_tensors="pt"
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
