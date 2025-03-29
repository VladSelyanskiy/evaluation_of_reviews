# Standard python library imports
import logging

# Related third party importsi
import pydantic
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# local imports
from backend.models.usage_of_models import Classifier

# Создание FastAPI приложения
app = FastAPI()

# логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

service_config_path = "src//main.py"


# датакласс выхода сервиса
class ServiceOutput(pydantic.BaseModel):
    class_name: str = pydantic.Field("class")


# датакласс входа сервиса
class ServiceInput(pydantic.BaseModel):
    review: str = pydantic.Field("text")


logger.info(f"\tЗагружена конфигурация сервиса по пути: {service_config_path}")

logger.info("\tЗагрузка моделeй")
models = Classifier()
logger.info("\tМодели загружены")


# функция обработки запроса
def get_class(text: str, clf: str = "logreg") -> str:

    logger.info(
        f"\tВызвана функция определения класса текста с параметрами: text={text[:5]}..., clf={clf}"
    )

    if clf == "logreg":
        logger.info("\tИспользование логистической регрессии")
        return models.use_model_lr(text)
    elif clf == "nb":
        logger.info("\tИспользование наивного байеса")
        return models.use_model_nb(text)
    else:
        logger.error(f"Неизвестный классификатор: {clf}")
        return "Unknown classifier"


# точка доступа для проверки жизни сервиса
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


# точка доступа для обработки текстового запроса
@app.post("/string/")
async def inference(data: ServiceInput) -> JSONResponse:

    logger.info("\tПолучен запрос на обработку текста")
    logger.info("\tПолучение текста")
    text = data.review.strip()
    logger.info(f"\tПолучен текст: {text if len(text) <= 10 else text[:10]+"..."}")
    logger.info("\tПередача текста к модели")

    result = get_class(text)
    logger.info(f"\tРезультат обработки текста: {result}")

    service_output = ServiceOutput(class_name=result)
    service_output_json = service_output.model_dump(mode="json")

    logger.info("\tОтправка результата обработки в формате JSON")
    return JSONResponse(content=jsonable_encoder(service_output_json))


"""
uvicorn main:app
"""
