# Standard python library imports
import logging

# Local imports
from models.classic_methods_2cls import Classifier
from models.LSTM_2cls import LSTM2Classes
from shemas.service_input import ServiceInput
from shemas.service_output import ServiceOutput, ServiceOutputList
from shemas.service_config import config


NUMBER_OF_FIRST_CHAR: int = config.NUMBER_OF_FIRST_CHAR
logger = logging.getLogger(__name__)


class Handler2Cls:

    def __init__(
        self,
        data: ServiceInput,
        model_type: str = "naive_bayes",
        category: str = "common",
    ):
        self.data: ServiceInput = data
        self.model_type = model_type
        match model_type:
            case "naive_bayes":
                self.models = Classifier()
            case "log_reg":
                self.models = Classifier()
            case "lstm":
                self.models = LSTM2Classes()
        self.category = category

    # Функция обработки запроса
    def get_class(self, text: str) -> int:

        logger.info(
            "Вызвана функция определения класса текста с параметрами: "
            + f"text = {text[:NUMBER_OF_FIRST_CHAR]}..., clf = {self.model_type}, category = {self.category}"
        )

        match self.model_type:
            case "log_reg":
                logger.info("Использование логистической регрессии")
                return self.models.use_model_lr(text)
            case "naive_bayes":
                logger.info("Использование наивного байеса")
                return self.models.use_model_nb(text)
            case "lstm":
                logger.info("Использование LSTM")
                class_number: float = self.models.use_model_lstm(text)
                if class_number >= config.CLASS_THRESHOLD:
                    return 1
                else:
                    return 0
            case _:
                logger.error(f"Неизвестный классификатор: {self.model_type}")
                return -1

    def get_class_name(self, class_number: int) -> str:
        return config.CLASS_NAMES[class_number]

    # Создание выходных данных на основании текста отзыва
    def create_output_from_text(self, text: str, count: int = 0) -> ServiceOutput:

        logger.info(f"Получен текст {count}: {text[:NUMBER_OF_FIRST_CHAR]}...")

        logger.info(f"Передача текста {count} к модели")
        class_number = self.get_class(text)
        logger.info(f"Результат обработки текста {count}: {class_number}")

        logger.info(f"Создание ServiceOutput номер {count}")
        service_output = ServiceOutput(
            class_name=self.get_class_name(class_number),
            class_number=class_number,
            text_beginning=(text[:NUMBER_OF_FIRST_CHAR] + "..."),
            text_number=count,
        )

        return service_output

    def get_outputs(self) -> ServiceOutputList:
        logger.info("Вызвана функция получения выходных данных")
        new_output_list = ServiceOutputList(
            output_list=[
                self.create_output_from_text(text, count)
                for count, text in enumerate(self.data.reviews, 1)
            ]
        )
        return new_output_list
