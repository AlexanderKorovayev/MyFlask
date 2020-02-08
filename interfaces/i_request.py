"""
модуль описывает базовый объект запроса клиента
"""


from functools import lru_cache


class IRequest:
    """
    класс объект запроса
    """

    method = None
    _target = None
    version = None
    headers = None
    _rfile = None

    @staticmethod
    def set_data(method, target, version, headers, rfile):
        IRequest.method = method
        IRequest._target = target
        IRequest.version = version
        IRequest.headers = headers
        IRequest._rfile = rfile

    @staticmethod
    def body():
        """
        метод получения тела запроса
        """
        raise NotImplementedError

    @staticmethod
    @lru_cache(maxsize=None)
    def url():
        """
        метод для парсинга таргета
        """
        raise NotImplementedError
