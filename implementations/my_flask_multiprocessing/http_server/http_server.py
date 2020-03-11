"""
модуль, реализующий http сервер
"""

from interfaces.multiprocessing.i_server import IServer
from base_errors.http_errors import HTTPError
from email.parser import Parser
from implementations.my_flask_multiprocessing.response import Response
from implementations.my_flask_multiprocessing.request import Request
from datetime import datetime
import multiprocessing
import socket


class HTTPServer(IServer):

    _MAX_LINE = 64 * 1024  # http протокол не обязывает ограничивать длинну строк реквест лайна,
    # но обычно сервера ограничивают
    _MAX_HEADERS = 100  # в целом http протокол не обязывает ограничивать длинну хидера, но обычно сервера ограничивают

    def __init__(self, host_name, port_id, server_name, request, response):
        super().__init__(host_name, port_id, server_name, request, response)

    def serve_forever(self):
        """
        главная функция по обслуживанию клиента
        """

        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serv_sock.bind((self._host, self.port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                HTTPServer._queue.put((HTTPServer._serve_client, conn))

        finally:
            serv_sock.close()

    @staticmethod
    def _serve_client(conn):
        """
        обслуживание запроса(обработка запроса, выполнение запроса, ответ клиенту)
        :param conn: соединение с клиентом
        """

        try:
            request = HTTPServer._parse_request(conn)
            response = HTTPServer._handle_request(request)
            HTTPServer._send_response(conn, response)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            HTTPServer._send_error(conn, e)

        if conn:
            conn.close()

    @staticmethod
    def _parse_request(conn):
        """
        разбор запроса от клиента
        :param conn: сокет
        :return: объект запроса
        """

        _rfile = conn.makefile('rb')
        method, target, ver = HTTPServer._parse_request_line(_rfile)
        headers = HTTPServer._parse_headers(_rfile)
        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')
        if host not in (HTTPServer.server_name, f'{HTTPServer.server_name}:{HTTPServer.port}'):
            raise HTTPError(404, 'Not found')
        _request = Request()
        _request.set_data(method, target, ver, headers, _rfile)
        return _request

    @staticmethod
    def _parse_request_line(conn):
        """
        разбор реквест лайна
        :conn: подключение к сокету
        :return: метод запроса, путь запроса, версия протокола
        """

        raw = conn.readline(HTTPServer._MAX_LINE + 1)
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

    @staticmethod
    def _parse_headers(conn):
        """
        разбор заголовков
        :conn: подключение к сокету
        :return: объект, содержащий заголовки
        """
        headers = []
        while True:
            line = conn.readline(HTTPServer._MAX_LINE + 1)
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

    @staticmethod
    def _handle_request(request):
        """
        обработка запроса от клиента
        метод имеет поведение по умолчанию, которое необходимо переопределить бизнес логикой
        :request: объект запроса
        :return: данные для клиента
        """
        response = Response()
        response.set_data(200, 'OK')
        return response

    @staticmethod
    def _send_response(conn, response):
        """
        Отправка ответа клиенту
        :param conn: сокет
        :param response: объект ответа
        """

        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'

        wfile.write(status_line.encode('iso-8859-1'))

        if response.headers:
            for (key, value) in response.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if response.body:
            wfile.write(response.body)

        wfile.flush()
        wfile.close()

    @staticmethod
    def _send_error(conn, err):
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
        HTTPServer._send_response(conn, response)
