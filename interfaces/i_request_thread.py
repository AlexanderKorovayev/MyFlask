"""
модуль описывает базовый объект запроса клиента
"""


class IRequest:
    """
    класс объект запроса
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IRequest, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.method = None
        self.version = None
        self.headers = None
        self._target = None
        self._rfile = None

    def set_data(self, method, target, version, headers, rfile):
        self.method = method
        self._target = target
        self.version = version
        self.headers = headers
        self._rfile = rfile

    def body(self):
        """
        метод получения тела запроса
        """
        raise NotImplementedError

    def url(self):
        """
        метод для парсинга таргета
        """
        raise NotImplementedError

    def path(self):
        """
        метод получения пути из url
        """
        raise NotImplementedError

    def query(self):
        """
        метод получения параметров запроса
        """
        raise NotImplementedError
