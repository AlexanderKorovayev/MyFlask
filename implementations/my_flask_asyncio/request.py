from interfaces.asynced.i_request_async import IRequest
from urllib.parse import parse_qs, urlparse


class Request(IRequest):
    """
    класс объект запроса
    """

    def body(self):
        size = self.headers.get('Content-Length')
        if not size:
            return None
        return self._rfile.read(size)

    def url(self):
        return urlparse(self._target)

    def path(self):
        return self.url().path

    def query(self):
        return parse_qs(self.url().query)

