class RequestAPIYandexPracticumErrors(Exception):
    """Статус ответа при запросе к API Яндекс Практикум отличается от 200"""
    pass


class ServiceDenial(Exception):
    "Отказ в обслуживании!"
    pass