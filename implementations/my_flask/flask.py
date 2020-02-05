"""
модуль реализующий непосредственно сам фреймворм
"""

from interfaces.i_server import IServer
from utils import check_type
from implementations.http_server import http_server


class Flask(http_server.HTTPServer):
    # мы наследуем сервер и расширяем его добавляя обработку данных сервером, в сервере обработка данных не должна быть реализована
    #TODO пока храним в поле класса, но надо будет это поменять потому что каждый экземпляр будет переписывать данные, например хранить в базе
    route_map = {}

    def __init__(self, port, host_name='localhost', server_name='localhost'):
        super().__init__(host_name, port, server_name)

    def route(self, path):
        def inner_route(f):
            Flask.route_map[path] = f.__name__
            def inner_inner_route(*args, **kwargs):
                rez = f(*args, **kwargs)
                return rez
            return inner_inner_route
        return inner_route

    def run(self):
            self.serve_forever()
            # func = Flask.route_map.get(path)
            # print(globals().get(func)())
