# Standard python library imports
import logging

# Related third party imports
import pydantic
import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Local imports
from models.classifier import Classifier
from shemas.service_output import ServiceOutput
from shemas.service_config import config

# Создание FastAPI приложения
app = FastAPI()

# Логирование
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


logger = logging.getLogger(__name__)

service_config_path = r"src\backend\shemas\service_config.py"


# Датакласс входа сервиса
class ServiceInput(pydantic.BaseModel):
    review: str = pydantic.Field("text")


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

    logger.info("Получен запрос на обработку текста")
    logger.info("Получение текста")
    text = data.review
    logger.info(f"Получен текст: {text if len(text) <= 10 else text[:10]+"..."}")

    logger.info("Передача текста к модели")
    result = get_class(text)
    logger.info(f"Результат обработки текста: {result}")

    logger.info("Создание ServiceOutput")
    service_output = ServiceOutput(
        class_name=get_class_name(result), class_number=result, text=text
    )

    logger.info("Создание JSON представления ServiceOutput")
    service_output_json = service_output.model_dump(mode="json")

    logger.info("Отправка результата обработки в формате JSON")
    return JSONResponse(content=jsonable_encoder(service_output_json))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
