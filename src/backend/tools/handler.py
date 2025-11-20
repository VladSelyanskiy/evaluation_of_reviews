# Standard python library imports
import logging

# Local imports
from models.classic_methods_2cls import Classifier
from models.LSTM_2cls import LSTM2Classes
from models.classifier_for_3_classes import Classifier3cls
from models.classifier_for_5_classes import Classifier5cls
from tools.service_input import ServiceInput
from tools.service_output import ServiceOutput, ServiceOutputList
from tools.service_config import config


NUMBER_OF_FIRST_CHAR: int = config.NUMBER_OF_FIRST_CHAR
logger = logging.getLogger(__name__)


class MainHandler:

    def __init__(
        self,
        data: ServiceInput,
    ):
        self.data: ServiceInput = data
        self.info: dict[str, str] = {
            "model_type": data.model_type,
            "category": data.category,
        }

    def get_outputs(self) -> ServiceOutputList:
        if self.info["model_type"] in config.MODELS_FOR_2_CLASSES:
            self.handler2cls = Handler2Cls(self.data)
            return self.handler2cls.get_outputs()
        elif self.info["model_type"] in config.MODELS_FOR_3_CLASSES:
            self.handler3cls = Handler3Cls(self.data)
            return self.handler3cls.get_outputs()
        elif self.info["model_type"] in config.MODELS_FOR_5_CLASSES:
            self.handler5cls = Handler5Cls(self.data)
            return self.handler5cls.get_outputs()
        else:
            return ServiceOutputList()


class Handler2Cls:

    def __init__(self, data: ServiceInput):
        self.data: ServiceInput = data
        self.model_type: str = data.model_type
        match self.model_type:
            case "naive_bayes":
                self.models = Classifier()
            case "log_reg":
                self.models = Classifier()
            case "lstm":
                self.models = LSTM2Classes()
        self.category: str = data.category

    # Функция обработки запроса
    def get_class(self, text: str) -> tuple[int, float]:

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
                return self.models.use_model_lstm(text)
            case _:
                logger.error(f"Неизвестный классификатор: {self.model_type}")
                return (-1, -1.0)

    def get_class_name(self, class_number: int) -> str:
        return config.CLASS_NAMES[class_number]

    # Создание выходных данных на основании текста отзыва
    def create_output_from_text(self, text: str, count: int = 0) -> ServiceOutput:

        logger.info(f"Получен текст {count}: {text[:NUMBER_OF_FIRST_CHAR]}...")

        logger.info(f"Передача текста {count} к модели")
        class_number, class_confidence = self.get_class(text)
        logger.info(
            f"Результат обработки текста {count}: {class_number}, {class_confidence}"
        )

        logger.info(f"Создание ServiceOutput номер {count}")
        service_output = ServiceOutput(
            class_name=self.get_class_name(class_number),
            class_number=class_number,
            text_beginning=(text[:NUMBER_OF_FIRST_CHAR] + "..."),
            text_number=count,
            class_confidence=class_confidence,
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


class Handler3Cls:

    def __init__(self, data: ServiceInput):
        self.data: ServiceInput = data
        self.model_type: str = data.model_type
        match self.model_type:
            case "rt2_3cls":
                self.models = Classifier3cls()
        self.category: str = data.category

    # Функция обработки запроса
    def get_class(self, text: str) -> tuple[float, float]:

        logger.info(
            "Вызвана функция определения класса текста с параметрами: "
            + f"text = {text[:NUMBER_OF_FIRST_CHAR]}..., clf = {self.model_type}, category = {self.category}"
        )

        match self.model_type:
            case "rt2_3cls":
                logger.info("Использование модели RT2 3 classes")
                return self.models.use_model_RT2(text)
            case _:
                logger.error(f"Неизвестный классификатор: {self.model_type}")
                return -1

    def get_class_name(self, class_number: int) -> str:
        return config.CLASS_3_NAMES[class_number]

    # Создание выходных данных на основании текста отзыва
    def create_output_from_text(self, text: str, count: int = 0) -> ServiceOutput:

        logger.info(f"Получен текст {count}: {text[:NUMBER_OF_FIRST_CHAR]}...")

        logger.info(f"Передача текста {count} к модели")
        class_number, class_confidence = self.get_class(text)
        logger.info(
            f"Результат обработки текста {count}: {class_number}, {class_confidence}"
        )

        logger.info(f"Создание ServiceOutput номер {count}")
        service_output = ServiceOutput(
            class_name=self.get_class_name(class_number),
            class_number=class_number,
            text_beginning=(text[:NUMBER_OF_FIRST_CHAR] + "..."),
            text_number=count,
            class_confidence=class_confidence,
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


class Handler5Cls:

    def __init__(self, data: ServiceInput):
        self.data: ServiceInput = data
        self.model_type: str = data.model_type
        match self.model_type:
            case "rt2_5cls":
                self.models = Classifier5cls()
        self.category: str = data.category

    # Функция обработки запроса
    def get_class(self, text: str) -> tuple[float, float]:

        logger.info(
            "Вызвана функция определения класса текста с параметрами: "
            + f"text = {text[:NUMBER_OF_FIRST_CHAR]}..., clf = {self.model_type}, category = {self.category}"
        )

        match self.model_type:
            case "rt2_5cls":
                logger.info("Использование модели RT2 5 clsses")
                return self.models.use_model_RT2_for_5_classes(text)
            case _:
                logger.error(f"Неизвестный классификатор: {self.model_type}")
                return -1

    def get_class_name(self, class_number: int) -> str:
        return config.CLASS_5_NAMES[class_number]

    # Создание выходных данных на основании текста отзыва
    def create_output_from_text(self, text: str, count: int = 0) -> ServiceOutput:

        logger.info(f"Получен текст {count}: {text[:NUMBER_OF_FIRST_CHAR]}...")

        logger.info(f"Передача текста {count} к модели")
        class_number, class_confidence = self.get_class(text)
        logger.info(
            f"Результат обработки текста {count}: {class_number}, {class_confidence}"
        )

        logger.info(f"Создание ServiceOutput номер {count}")
        service_output = ServiceOutput(
            class_name=self.get_class_name(class_number),
            class_number=class_number,
            text_beginning=(text[:NUMBER_OF_FIRST_CHAR] + "..."),
            text_number=count,
            class_confidence=class_confidence,
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
