import socket
import sys
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse
import json

class MyHTTPServer:

    MAX_LINE = 64*1024
    MAX_HEADERS = 100

    def __init__(self, host_name, port_id, server_name):
        self._host = host_name
        self._port = port_id
        self._server_name = server_name
        self._users = {}

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
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
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')
        if host not in (self._server_name,
                        f'{self._server_name}:{self._port}'):
            raise Exception('Not found')
        return Request(method, target, ver, headers, rfile)

    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MyHTTPServer.MAX_LINE + 1)
            if len(line) > MyHTTPServer.MAX_LINE:
                raise Exception('Header line is too long')

            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)
            if len(headers) > MyHTTPServer.MAX_HEADERS:
                raise Exception('Too many headers')
            str_headers = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(str_headers)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MyHTTPServer.MAX_LINE + 1)  # эффективно читаем строку целиком
        if len(raw) > MyHTTPServer.MAX_LINE:
            raise Exception('Request line is too long')

        req_line = str(raw, 'iso-8859-1')
        req_line = req_line.rstrip('\r\n')
        words = req_line.split()
        if len(words) != 3:
            raise Exception('Malformed request line')

        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise Exception('Unexpected HTTP version')

        return method, target, ver

    def handle_request(self, req):
        if req.path == '/users' and req.method == 'POST':
            return self.handle_post_users(req)

        if req.path == '/users' and req.method == 'GET':
            return self.handle_get_users(req)

        if req.path.startswith('/users/'):
            user_id = req.path[len('/users/'):]
            if user_id.isdigit():
                return self.handle_get_user(req, user_id)

        raise Exception('Not found')

    def handle_post_users(self, req):
        user_id = len(self._users) + 1
        self._users[user_id] = {'id': user_id,
                                'name': req.query['name'][0],
                                'age': req.query['age'][0]}
        return Response(204, 'Created')

    def handle_get_users(self, req):
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
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', content_type),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)

    def handle_get_user(self, req, user_id):
        pass

    def send_response(self, conn, resp):
        pass  # TODO: implement me

    def send_error(self, conn, err):
        pass  # TODO: implement me


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


if __name__ == '__main__':
    my_host = sys.argv[1]
    my_port = int(sys.argv[2])
    my_name = sys.argv[3]

    serv = MyHTTPServer(my_host, my_port, my_name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
