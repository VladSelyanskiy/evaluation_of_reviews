# Standard python library imports
import logging
import sqlite3

# Related third party imports
import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Local imports
from tools.handler import MainHandler
from tools.service_input import ServiceInput
from tools.service_output import ServiceOutputList
from tools.service_config import config

# Создание FastAPI приложения
app = FastAPI()

# Логирование
logging.basicConfig(
    level=config.LOG_LEVEL, format=config.LOG_FORMAT, filename=config.LOG_FILE
)

logger = logging.getLogger(__name__)

logger.info(f"Загружена конфигурация сервиса по пути: {config.SERVICE_CONFIG_PATH}")

try:
    with sqlite3.connect(config.DATABASE_PATH) as connection:
        cursor = connection.cursor()

        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS reviews \
                (id INTEGER PRIMARY KEY, text TEXT, \
                class_name TEXT, class_number INTEGER)"
        )
        connection.commit()
except sqlite3.Error as e:
    logger.error(f"An error occurred: {e}")


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
async def inference(new_data: ServiceInput) -> JSONResponse:

    logger.info(
        f"Получен запрос на обработку текстов с параметрами: категория - <{new_data.category}>, модель - <{new_data.model_type}>"
    )

    logger.info("Создание обработчика Handler")
    handler: MainHandler = MainHandler(data=new_data)

    logger.info("Начало получения ServiceOutputList")
    outputs: ServiceOutputList = handler.get_outputs()
    logger.info("Получение ServiceOutputList завершено")

    try:
        with sqlite3.connect(config.DATABASE_PATH) as connection:

            cursor = connection.cursor()
            logger.info("Добавление текстов в базу данных")
            for output in outputs.output_list:
                # Insert data
                cursor.execute(
                    "INSERT INTO reviews \
                        (text, class_name, class_number) \
                        VALUES (?, ?, ?)",
                    (output.text_beginning, output.class_name, output.class_number),
                )

            logger.info("Добавлены тексты в базу данных")
    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")

    logger.info("Создание JSON представления ServiceOutputList")
    service_output_json = outputs.model_dump(mode="json")

    logger.info("Отправка результата обработки в формате JSON")
    return JSONResponse(content=jsonable_encoder(service_output_json))


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.API_HOST, port=config.API_PORT, reload=True)
