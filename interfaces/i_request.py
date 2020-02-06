"""
модуль описывает базовый объект запроса клиента
"""


from functools import lru_cache


class IRequest:
    """
    класс объект запроса
    """

    _method = None
    _target = None
    _version = None
    _headers = None
    _rfile = None

    @staticmethod
    def set_data(method, target, version, headers, rfile):
        _method = method
        _target = target
        _version = version
        _headers = headers
        _rfile = rfile

    @staticmethod
    def body():
        """
        метод получения тела запроса
        """
        raise NotImplementedError

    @staticmethod
    @property
    @lru_cache(maxsize=None)
    def url():
        """
        метод для парсинга таргета
        """
        raise NotImplementedError
