# Standard python library imports
import logging

# Related third party imports
import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Local imports
from models.classifier import Classifier
from shemas.service_input import ServiceInput
from shemas.service_output import ServiceOutput, ServiceOutputList
from shemas.service_config import config

# Создание FastAPI приложения
app = FastAPI()

# Логирование
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

NUMBER_OF_FIRST_CHAR: int = 13

service_config_path = r"src\backend\shemas\service_config.py"
logger.info(f"Загружена конфигурация сервиса по пути: {service_config_path}")

logger.info("Загрузка моделeй")
models = Classifier()
logger.info("Модели загружены")


# Функция обработки запроса
def get_class(text: str, clf: str = "naive_bayes") -> int:

    logger.info(
        f"Вызвана функция определения класса текста с параметрами: text={text[:5]}..., clf={clf}"
    )

    if clf == "logreg":
        logger.info("Использование логистической регрессии")
        return models.use_model_lr(text)
    elif clf == "naive_bayes":
        logger.info("Использование наивного байеса")
        return models.use_model_nb(text)
    else:
        logger.error(f"Неизвестный классификатор: {clf}")
        return -1


# Получение имени класса по его индексу
def get_class_name(value: int) -> str:
    if value == 0:
        return "negative"
    elif value == 1:
        return "positive"
    else:
        return "Unknown class"


# Создвние выходных данных на основании текста отзыва
def create_output_from_text(text: str, count: int = 0) -> ServiceOutput:

    logger.info(f"Получен текст {count}: {text[:NUMBER_OF_FIRST_CHAR] + "..."}")

    logger.info(f"Передача текста {count} к модели")
    class_number = get_class(text)
    logger.info(f"Результат обработки текста {count}: {class_number}")

    logger.info("Создание ServiceOutput")
    service_output = ServiceOutput(
        class_name=get_class_name(class_number),
        class_number=class_number,
        text_beginning=(text[:NUMBER_OF_FIRST_CHAR] + "..."),
        text_number=count,
    )

    return service_output


# Точка доступа для проверки жизни сервиса
@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def health_check() -> str:
    """
    Точка доступа для проверки жизни сервиса

    Возвращает:
        HTTP Статус код (ОК)
    """
    return '{"Status" : "OK"}'


# Точка доступа для обработки текстового запроса
@app.post("/string/")
async def inference(data: ServiceInput) -> JSONResponse:

    logger.info("Получен запрос на обработку текстов")
    logger.info("Получение текстов")

    logger.info("Создание ServiceOutputList")
    outputs = ServiceOutputList(
        output_list=[
            create_output_from_text(text=text, count=count)
            for count, text in enumerate(data.reviews, 1)
        ]
    )

    logger.info("Создание JSON представления ServiceOutputList")
    service_output_json = outputs.model_dump(mode="json")

    logger.info("Отправка результата обработки в формате JSON")
    return JSONResponse(content=jsonable_encoder(service_output_json))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
