from interfaces.i_request import IRequest
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
        return Request._rfile.read(size)

    @staticmethod
    def url():
        return urlparse(Request._target)

    @staticmethod
    def path():
        return Request.url().path

    @staticmethod
    def query():
        return parse_qs(Request.url().query)

