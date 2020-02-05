"""
модуль, реализующий http сервер
"""

from interfaces.i_server import IServer
from interfaces.i_response import Response
from base_errors.http_errors import HTTPError
from implementations.http_server.http_request import Request
from email.parser import Parser
import json


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
        return Request(method, target, ver, headers, self._rfile)

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

    def handle_request(self, req):
        """
        обработка запроса от клиента
        :param req: объект запроса
        :return: данные для клиента
        #TODO вот эта часть должна быть декоратором, т.е. сервер запускается обрабатывает запрос а эта штука реализует уже бл. Т.е. это по сути меняющаяся часть
        """
        if req.path == '/users' and req.method == 'POST':
            return self.handle_post_users(req)

        if req.path == '/users' and req.method == 'GET':
            return self.handle_get_users(req)

        if req.path.startswith('/users/'):
            user_id = req.path[len('/users/'):]
            if user_id.isdigit():
                return self.handle_get_user(req, user_id)

        raise HTTPError(404, 'Not found')

    def handle_post_users(self, req):
        """
        обработка запроса на создание пользователя
        :param req: объект запроса
        :return: объект ответа
        """
        user_id = len(self._users) + 1
        self._users[user_id] = {'id': user_id,
                                'name': req.query['name'][0],
                                'age': req.query['age'][0]}
        return Response(204, 'Created')

    def handle_get_users(self, req):
        """
        обработка запроса на получение всех пользователей
        :param req: объект запроса
        :return: объект ответа
        """
        accept = req.headers.get('Accept')
        if 'text/html' in accept:
            content_type = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'<div>Пользователи ({len(self._users)})</div>'
            body += '<ul>'
            for u in self._users.values():
                body += f'<li>#{u["id"]} {u["name"]}, {u["age"]}</li>'
            body += '</ul>'
            body += '</body></html>'

        elif 'application/json' in accept:
            content_type = 'application/json; charset=utf-8'
            body = json.dumps(self._users)

        else:
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', content_type),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)

    def handle_get_user(self, req, user_id):
        """
        бработка запроса на получение пользоватедя по id
        :param req: объект запроса
        :param user_id: id пользователя
        :return: объект запроса
        """
        user = self._users.get(int(user_id))
        if not user:
            raise HTTPError(404, 'Not found')

        accept = req.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'#{user["id"]} {user["name"]}, {user["age"]}'
            body += '</body></html>'

        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(user)

        else:
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)

    def send_response(self, conn, resp):
        """
        Отправка ответа клиенту
        :param conn: сокет
        :param resp: объект ответа
        """
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

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
