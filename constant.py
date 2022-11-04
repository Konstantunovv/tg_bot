CHECK_TOKENS_CRITICAL_LOG = (
    'Отсутствует обязательная переменная окружения: {}'
)
SEND_MESSAGE_INFO_LOG = ('Сообщение отправлено: {}')
SEND_MESSAGE_EXCEPTION_LOG = ('Сообщение {} в Telegram не отправлено: {}')
GET_API_ANSWER_REQUEST_ERROR = (
    'Некорректный запрос: {}. '
    'Передаваемые параметры:{url}, {headers}, {params}'
)
GET_API_ANSWER_RESPONSE_ERROR = (
    'Ответ сервера = {}. '
    'Входящие параметры: {url}, {headers}, {params}. '
)
SERVICE_DENIAL_ERROR = (
    'Отказ в обслуживании:{}: {}. '
    'Входящие параметры: {url}, {headers}, {params}.'
)
TYPE_ERROR_LIST = 'Неверный тип данных: {}. Ожидается список.'
TYPE_ERROR_DICT = 'Неверный тип данных: {}. Ожидается словарь.'
KEY_ERROR = 'Невозможно получить значение по ключу: homeworks.'
PARSE_STATUS_RETURN = (
    '{}\n'
    'Изменился статус проверки работы "{}". \n'
    '{}\n'
    'Коментарий к работе: {}'
)
INTERVIEWING_API = ('Опрашиваем Yandex Homework API')
MAIN_EXCEPTION_MESSAGE = 'Сбой в работе программы: {}'
NO_NEW_STATUS_IN_API = 'Отсутствие в ответе новых статусов'
MAIN_EXCEPTION_ERROR = 'Ошибка: {}'
