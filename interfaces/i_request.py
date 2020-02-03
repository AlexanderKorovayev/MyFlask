"""
модуль описывает базовый объект запроса клиента
"""


from functools import lru_cache


class IRequest:
    """
    класс объект запроса
    """
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    def body(self):
        """
        метод получения тела запроса
        """
        raise NotImplementedError

    @property
    @lru_cache(maxsize=None)
    def url(self):
        """
        метод для парсинга таргета
        """
        raise NotImplementedError
