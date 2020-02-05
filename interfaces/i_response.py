"""
модуль описывает базовый объект ответа сервера
"""


class Response:
    """
        класс объект ответа
    """
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body