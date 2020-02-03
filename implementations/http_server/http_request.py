from interfaces.i_request import IRequest
from functools import lru_cache
from urllib.parse import parse_qs, urlparse


class Request(IRequest):
    """
    класс объект запроса
    """

    def body(self):
        size = self.headers.get('Content-Length')
        if not size:
            return None
        return self.rfile.read(size)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)
