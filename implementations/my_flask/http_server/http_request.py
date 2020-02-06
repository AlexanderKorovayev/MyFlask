from interfaces.i_request import IRequest
from functools import lru_cache
from urllib.parse import parse_qs, urlparse


class Request(IRequest):
    """
    класс объект запроса
    """

    @staticmethod
    def body():
        size = Request.headers.get('Content-Length')
        if not size:
            return None
        return Request.rfile.read(size)

    @staticmethod
    @property
    @lru_cache(maxsize=None)
    def url():
        return urlparse(Request.target)

    @staticmethod
    @property
    def path():
        return Request.url.path

    @staticmethod
    @property
    @lru_cache(maxsize=None)
    def query():
        return parse_qs(Request.url.query)

