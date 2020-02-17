"""
модуль реализующий непосредственно сам фреймворм
"""


from implementations.my_flask_synchro.http_server import http_server
from base_errors.http_errors import HTTPError
from implementations.my_flask_synchro.request import request
from implementations.my_flask_synchro.response import response
from implementations.my_flask_synchro.session import session
from interfaces.i_data_worker import IDataWorker
import inspect
import importlib
import platform
import utils


class Flask(http_server.HTTPServer):
    # TODO пока храним в поле класса, но надо будет это поменять потому что каждый экземпляр будет переписывать данные, например хранить в базе
    _ROUTE_MAP = {}
    _HANDLE_MODULE_PATH = None

    def __init__(self, port, host_name='localhost', server_name='localhost'):
        super().__init__(host_name, port, server_name, request, response)
        self.os_name = platform.system()

        if self.os_name == 'Windows':
            Flask._HANDLE_MODULE_PATH = inspect.stack()[-1].filename.split("\\")[-1].split('.py')[0]
        if self.os_name == 'Linux':
            Flask._HANDLE_MODULE_PATH = inspect.stack()[-1].filename.split("/")[-1].split('.py')[0]

        # проверяем что основные объекты подходят для работы с фласком
        if not(utils.check_type(session, IDataWorker)):
            raise Exception('Session не соответствует заданным стандартам IDataWorker')

    def route(self, path, method='GET'):
        def inner_route(f):
            Flask._ROUTE_MAP[(path, method)] = f.__name__
            Flask._HANDLE_MODULE_PATH = inspect.getmodule(f)

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
        path = self._request.path()
        print("PATH IS " + str(path))
        method = self._request.method
        print("METHOD IS " + method)
        func_name = Flask._ROUTE_MAP.get((path, method))
        if not func_name:
            raise HTTPError(404, 'Not found')
        print("FUNC NAME IS " + func_name)
        bl_module = importlib.import_module(Flask._HANDLE_MODULE_PATH)
        result = getattr(bl_module, func_name)()
        print("RESULT IS \n" + str(result))
        return result

    def run(self):
        self.serve_forever()
