import socket
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse
import json


class MyHTTPServer:

    MAX_LINE = 64*1024  # http протокол не обязывает ограничивать длинну строк реквест лайна,
    # но обычно сервера ограничивают
    MAX_HEADERS = 100  # в целом http протокол не обязывает ограничивать длинну хидера, но обычно сервера ограничивают

    def __init__(self, host_name, port_id, server_name):
        self._host = host_name
        self._port = port_id
        self._server_name = server_name
        self._users = {}

    def serve_forever(self):
        """
        главная функция по обслуживанию клиента
        TODO сделать обслуживание асинхронным или многопроцессорным
        """
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, address = serv_sock.accept()
                try:
                    print('Connected ' + str(address))
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        """
        обслуживание запроса(обработка запроса, выполнение запроса, ответ клиенту)
        :param conn: соединение с клиентом
        """
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()

    def parse_request(self, conn):
        """
        разбор запроса от клиента
        :param conn: сокет
        :return: объект запроса
        """
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')
        if host not in (self._server_name, f'{self._server_name}:{self._port}'):
            raise HTTPError(404, 'Not found')
        return Request(method, target, ver, headers, rfile)

    def parse_request_line(self, rfile):
        """
        разбор реквест лайна
        :param rfile: объект сокета, обёрнутый оболочкой файла
        :return: метод запроса, путь запроса, версия протокола
        """
        raw = rfile.readline(MyHTTPServer.MAX_LINE + 1)

        if len(raw) > MyHTTPServer.MAX_LINE:
            raise Exception('Request line is too long')

        req_line = str(raw, 'iso-8859-1')
        req_line = req_line.rstrip('\r\n')
        words = req_line.split()

        if len(words) != 3:
            raise Exception('Incorrect request line')

        method, target, ver = words
        # реализована поддержка толкьо версии 1.1
        if ver != 'HTTP/1.1':
            raise Exception('Unexpected HTTP version')

        return method, target, ver

    def parse_headers(self, rfile):
        """
        разбор заголовков
        :param rfile: объект сокета, обёрнутый оболочкой файла
        :return: объект, содержащий заголовки
        """
        headers = []
        while True:
            line = rfile.readline(MyHTTPServer.MAX_LINE + 1)
            if len(line) > MyHTTPServer.MAX_LINE:
                raise Exception('Header line is too long')

            # проверка на окончание блока с заголовками
            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)
            if len(headers) > MyHTTPServer.MAX_HEADERS:
                raise Exception('Too many headers')

        str_headers = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(str_headers)

    def handle_request(self, req):
        """
        обработка запроса от клиента
        :param req: объект запроса
        :return: данные для клиента
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


class Request:
    """
    класс объект запроса
    """
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

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


class Response:
    """
        класс объект ответа
    """
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class HTTPError(Exception):
    """
    ксласс обработчик запросов
    """
    def __init__(self, status, reason, body=None):
        super()
        self.status = status
        self.reason = reason
        self.body = body


if __name__ == '__main__':
    # import sys
    # my_host = sys.argv[1]
    # my_port = int(sys.argv[2])
    # my_name = sys.argv[3]

    serv = MyHTTPServer('127.0.0.1', 2006, 'example.local')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
