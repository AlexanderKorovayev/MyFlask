"""
модуль, реализующий http сервер
"""

from interfaces.i_server import IServer
from interfaces.i_response import Response
from base_errors.http_errors import HTTPError
from implementations.my_flask.request import Request
from email.parser import Parser


class HTTPServer(IServer):

    MAX_LINE = 64 * 1024  # http протокол не обязывает ограничивать длинну строк реквест лайна,
    # но обычно сервера ограничивают
    MAX_HEADERS = 100  # в целом http протокол не обязывает ограничивать длинну хидера, но обычно сервера ограничивают

    def __init__(self, host_name, port_id, server_name):
        super().__init__(host_name, port_id, server_name)

    def parse_request(self, conn):
        """
        разбор запроса от клиента
        :param conn: сокет
        :return: объект запроса
        """
        self._rfile = conn.makefile('rb')
        method, target, ver = self._parse_request_line()
        headers = self._parse_headers()
        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')
        if host not in (self._server_name, f'{self._server_name}:{self._port}'):
            raise HTTPError(404, 'Not found')
        print("PARSE REQUEST IS")
        print("method is " + method)
        print("target is " + target)
        print("version is " + ver)
        print("host is " + str(host))
        Request.set_data(method, target, ver, headers, self._rfile)
        print("url is " + str(Request.url()))
        print(str(type(Request.url())))
        print("path is " + str(Request.path()))
        print(str(type(Request.path())))
        print("query is " + str(Request.query()))
        print(str(type(Request.query())))

    def _parse_request_line(self):
        """
        разбор реквест лайна
        :return: метод запроса, путь запроса, версия протокола
        """
        raw = self._rfile.readline(HTTPServer.MAX_LINE + 1)

        if len(raw) > HTTPServer.MAX_LINE:
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

    def _parse_headers(self):
        """
        разбор заголовков
        :return: объект, содержащий заголовки
        """
        headers = []
        while True:
            line = self._rfile.readline(HTTPServer.MAX_LINE + 1)
            if len(line) > HTTPServer.MAX_LINE:
                raise Exception('Header line is too long')

            # проверка на окончание блока с заголовками
            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)
            if len(headers) > HTTPServer.MAX_HEADERS:
                raise Exception('Too many headers')

        str_headers = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(str_headers)

    def handle_request(self):
        """
        обработка запроса от клиента
        метод имеет поведение по умолчанию, которое необходимо переопределить бизнес логикой
        :return: данные для клиента
        """
        return Response(200, 'OK')

    def send_response(self, conn, resp):
        """
        Отправка ответа клиенту
        :param conn: сокет
        :param resp: объект ответа
        """

        print('IN RESPONSE')


        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'

        print('STATUS LINE IS \n' + str(status_line))

        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            print('HEADERS IS \n' + str(resp.headers))
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

        print('FINISH SEND RESPONSE')

    def send_error(self, conn, err):
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
        resp = Response(status, reason,
                        [('Content-Length', len(body))],
                        body)
        self.send_response(conn, resp)
