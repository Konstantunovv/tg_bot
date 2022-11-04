import json
import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions
from constant import (
    CHECK_TOKENS_CRITICAL_LOG,
    GET_API_ANSWER_REQUEST_ERROR,
    GET_API_ANSWER_RESPONSE_ERROR,
    INTERVIEWING_API,
    KEY_ERROR,
    MAIN_EXCEPTION_ERROR,
    MAIN_EXCEPTION_MESSAGE,
    NO_NEW_STATUS_IN_API,
    PARSE_STATUS_RETURN,
    SEND_MESSAGE_INFO_LOG,
    SERVICE_DENIAL_ERROR,
    TYPE_ERROR_DICT,
    TYPE_ERROR_LIST,
)
from settings import ENDPOINT, HOMEWORK_VERDICTS, RETRY_TIME

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
ALL_TOKEN = ["PRACTICUM_TOKEN", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"]
HEADERS = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}


logger = logging.getLogger("bot_logger")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(stream=sys.stdout)
file_handler = logging.FileHandler(__file__ + ".log", mode="w")
formatter = logging.Formatter(
    "[%(asctime)s] "
    "[%(levelname)s "
    "%(name)s] [%(module)s:%(funcName)s >"
    " %(lineno)s] > %(message)s"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def send_message(bot, message):
    """Отправка сообщения в чат, определяемый в переменных окружения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(SEND_MESSAGE_INFO_LOG.format(message))
    except telegram.error.TelegramError as error:
        logger.exception(MAIN_EXCEPTION_ERROR.format(error))


def get_api_answer(current_timestamp):
    """Получение ответа API и проверка ответа."""
    params = {"from_date": current_timestamp}
    data = dict(url=ENDPOINT, headers=HEADERS, params=params)
    try:
        logger.debug(INTERVIEWING_API)
        response = requests.get(**data)
    except requests.exceptions.RequestException as request_error:
        raise ConnectionError(
            GET_API_ANSWER_REQUEST_ERROR.format(request_error, **data)
        )
    response_json = response.json()
    for error in ["code", "error"]:
        if error in response_json:
            raise json.JSONDecodeError(
                SERVICE_DENIAL_ERROR.format(
                    error, response_json[error], **data
                )
            )
    if response.status_code != HTTPStatus.OK:
        raise exceptions.RequestAPIYandexPracticumErrors(
            GET_API_ANSWER_RESPONSE_ERROR.format(response.status_code, **data)
        )
    return response_json


def check_response(response):
    """Проверка ответа API на корректность (наличие ключа 'homeworks')."""
    if not isinstance(response, dict):
        raise TypeError(TYPE_ERROR_DICT.format(type(response)))
    if "homeworks" not in response:
        raise KeyError(KEY_ERROR)
    homeworks = response["homeworks"]
    if not isinstance(homeworks, list):
        raise TypeError(TYPE_ERROR_LIST.format(type(homeworks)))
    return homeworks


def parse_status(homework):
    """Парсинг ответа API и проверка наличия нужных ключей и статусов."""
    name = homework["homework_name"]
    status = homework["status"]
    if status not in HOMEWORK_VERDICTS:
        raise ValueError(KEY_ERROR.format(status))
    return PARSE_STATUS_RETURN.format(name, HOMEWORK_VERDICTS[status])


def check_tokens():
    """Проверка доступности переменных окружения."""
    are_tokens_valid = True
    for name in ALL_TOKEN:
        if not globals()[name]:
            are_tokens_valid = False
            logging.critical(CHECK_TOKENS_CRITICAL_LOG.format(name))
    return are_tokens_valid


def main():
    """Логика работы tg bot."""
    if not check_tokens():
        return
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = 0
    last_message = ""
    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
                if send_message(bot, message):
                    timestamp = response.get("current_date", timestamp)
            else:
                logging.debug(NO_NEW_STATUS_IN_API)
        except Exception as error:
            message = MAIN_EXCEPTION_MESSAGE.format(error)
            logging.error(message)
            if message != last_message:
                if send_message(bot, message):
                    last_message = message
        finally:
            time.sleep(RETRY_TIME)


if __name__ == "__main__":
    main()
