# Standard python library imports
import logging

# Local imports
from models.classifier import Classifier
from shemas.service_input import ServiceInput
from shemas.service_output import ServiceOutput, ServiceOutputList
from shemas.service_config import config


# Логирование
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

NUMBER_OF_FIRST_CHAR: int = 13


class Handler:

    def __init__(self, data):
        self.data: ServiceInput = data

        logger = logging.getLogger(__name__)

        logger.info("Загрузка моделeй")
        self.models = Classifier()
        logger.info("Модели загружены")

    # Функция обработки запроса
    def get_class(
        self, text: str, clf: str = "naive_bayes", weights: str = "common"
    ) -> int:

        logger.info(
            "Вызвана функция определения класса текста с параметрами: "
            + f"text = {text[:5]}..., clf = {clf}, weights = {weights}"
        )

        # TODO
        # Здесь будет передаваться либо текст, либо список текстов в модель
        # и дополнительно категория для выбора весов.
        # Это все планируется реализовать в классе модели

        if clf == "logreg":
            logger.info("Использование логистической регрессии")
            return self.models.use_model_lr(text)
        elif clf == "naive_bayes":
            logger.info("Использование наивного байеса")
            return self.models.use_model_nb(text)
        else:
            logger.error(f"Неизвестный классификатор: {clf}")
            return -1

    # Получение имени класса по его индексу
    def get_class_name(self, value: int) -> str:
        if value == 0:
            return "negative"
        elif value == 1:
            return "positive"
        else:
            return "Unknown class"

    # Создвние выходных данных на основании текста отзыва
    def create_output_from_text(
        self, text: str, count: int = 0, category: str = "common"
    ) -> ServiceOutput:

        logger.info(f"Получен текст {count}: {text[:NUMBER_OF_FIRST_CHAR]}...")

        logger.info(f"Передача текста {count} к модели")
        class_number = self.get_class(text, weights=category)
        logger.info(f"Результат обработки текста {count}: {class_number}")

        logger.info(f"Создание ServiceOutput номер {count}")
        service_output = ServiceOutput(
            class_name=self.get_class_name(class_number),
            class_number=class_number,
            text_beginning=(text[:NUMBER_OF_FIRST_CHAR] + "..."),
            text_number=count,
        )

        return service_output

    def create_outputs(self, texts: list[str]) -> ServiceOutputList:
        logger.info(f"Получен список текстов: {texts[:NUMBER_OF_FIRST_CHAR]}...")
        new_output_list = ServiceOutputList(
            output_list=[
                self.create_output_from_text(text, count)
                for count, text in enumerate(texts, 1)
            ]
        )
        return new_output_list

    def get_outputs(self) -> ServiceOutputList:
        logger.info("Вызвана функция получения выходных данных")
        return self.create_outputs(self.data.reviews)
