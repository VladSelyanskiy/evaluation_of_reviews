# Standard python library imports
import logging
import sqlite3

# Related third party imports
import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Local imports
from shemas.service_handler import Handler
from shemas.service_input import ServiceInput
from shemas.service_output import ServiceOutputList
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
logger.info(f"Загружена конфигурация сервиса по пути: {service_config_path}")

try:
    with sqlite3.connect(r"src\backend\databases\reviews.db") as connection:
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

    logger.info("Получен запрос на обработку текстов")
    logger.info(f"Получены тексты с категорией <{new_data.category}>")

    logger.info("Создание обработчика Handler")
    handler: Handler = Handler(data=new_data)

    logger.info("Начало получения ServiceOutputList")
    outputs: ServiceOutputList = handler.get_outputs()
    logger.info("Получение ServiceOutputList завершено")

    try:
        with sqlite3.connect(r"src\backend\databases\reviews.db") as connection:

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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
