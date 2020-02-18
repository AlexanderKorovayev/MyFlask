"""
модуль описывает базовый объект ответа сервера
"""


class IResponse:
    """
        класс объект ответа
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IResponse, cls).__new__(cls)
        return cls.instance

    def __init__(self, status=200, reason='OK', headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body

    def set_data(self, status=200, reason='OK', headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body
