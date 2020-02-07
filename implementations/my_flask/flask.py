"""
модуль реализующий непосредственно сам фреймворм
"""


from implementations.my_flask.http_server import http_server
from base_errors.http_errors import HTTPError
from implementations.my_flask.request import Request


class Flask(http_server.HTTPServer):
    # мы наследуем сервер и расширяем его добавляя обработку данных сервером, в сервере обработка данных не должна быть реализована
    #TODO пока храним в поле класса, но надо будет это поменять потому что каждый экземпляр будет переписывать данные, например хранить в базе
    route_map = {}

    def __init__(self, port, host_name='localhost', server_name='localhost'):
        super().__init__(host_name, port, server_name)

    def route(self, path, method='GET'):
        def inner_route(f):
            Flask.route_map[(path, method)] = f.__name__

            def inner_inner_route(*args, **kwargs):
                rez = f(*args, **kwargs)
                return rez
            return inner_inner_route
        return inner_route
    
    def handle_request(self):
        """
        обработка запроса от клиента
        :return: данные для клиента
        """
        print('IN HANDLE')
        print(Request.path)
        path = Request.path
        print("PATH IS " + path)
        method = Request.method
        print("METHOD IS " + method)
        func_name = Flask.route_map.get((path, method))
        if not func_name:
            raise HTTPError(404, 'Not found')
        print("FUNC NAME IS " + func_name)
        result = globals().get(func_name)()
        print("RESULT IS \n" + result)
        return result

    def run(self):
        self.serve_forever()
