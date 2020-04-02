"""
модуль, реализующий http сервер
"""

from interfaces.asynced.i_server import IServer
from base_errors.http_errors import HTTPError
from email.parser import Parser
from implementations.my_flask_asyncio.response import Response
from implementations.my_flask_asyncio.request import Request
from datetime import datetime


class HTTPServer(IServer):

    _MAX_LINE = 64 * 1024  # http протокол не обязывает ограничивать длинну строк реквест лайна,
    # но обычно сервера ограничивают
    _MAX_HEADERS = 100  # в целом http протокол не обязывает ограничивать длинну хидера, но обычно сервера ограничивают

    def __init__(self, host_name, port_id, server_name, request, response):
        super().__init__(host_name, port_id, server_name, request, response)

    async def _parse_request(self, reader):
        """
        разбор запроса от клиента
        :param conn: сокет
        :return: объект запроса
        """

        _rfile = reader
        method, target, ver = await self._parse_request_line(_rfile)
        headers = await self._parse_headers(_rfile)
        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')
        if host not in (self.server_name, f'{self.server_name}:{self.port}'):
            raise HTTPError(404, 'Not found')
        _request = Request()
        _request.set_data(method, target, ver, headers, _rfile)
        return _request

    async def _parse_request_line(self, conn):
        """
        разбор реквест лайна
        :conn: подключение к сокету
        :return: метод запроса, путь запроса, версия протокола
        """
        raw = await conn.readline()

        if len(raw) > HTTPServer._MAX_LINE:
            raise Exception('Request line is too long')

        req_line = str(raw, 'iso-8859-1')
        req_line = req_line.rstrip('\r\n')
        params = req_line.split()

        if len(params) != 3:
            raise Exception('Incorrect request line')

        method, target, ver = params

        # реализована поддержка толкьо версии 1.1
        if ver != 'HTTP/1.1':
            raise Exception('Unexpected HTTP version')

        return method, target, ver

    async def _parse_headers(self, conn):
        """
        разбор заголовков
        :conn: подключение к сокету
        :return: объект, содержащий заголовки
        """
        headers = []
        while True:
            line = await conn.readline()
            if len(line) > HTTPServer._MAX_LINE:
                raise Exception('Header line is too long')

            # проверка на окончание блока с заголовками
            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)
            if len(headers) > HTTPServer._MAX_HEADERS:
                raise Exception('Too many headers')

        str_headers = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(str_headers)

    async def _handle_request(self, request):
        """
        обработка запроса от клиента
        метод имеет поведение по умолчанию, которое необходимо переопределить бизнес логикой
        :request: объект запроса
        :return: данные для клиента
        """

        response = Response()
        response.set_data(200, 'OK')
        return response

    async def _send_response(self, conn, response):
        """
        Отправка ответа клиенту
        :param conn: сокет
        :param response: объект ответа
        """

        wfile = conn
        status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'

        wfile.write(status_line.encode('iso-8859-1'))

        if response.headers:
            for (key, value) in response.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if response.body:
            wfile.write(response.body)

        await wfile.drain()

    async def _send_error(self, conn, err):
        """
        конструирование объекта ошибки и его отправка
        :param conn: сокет
        :param err: ошибка
        """
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        response = Response()
        response.set_data(status, reason, [('Content-Length', len(body))], body)
        await self._send_response(conn, response)
