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

            def inner_inner_route(*args, **kwargs):
                rez = f(*args, **kwargs)
                return rez
            return inner_inner_route
        return inner_route
    
    def _handle_request(self):
        """
        обработка запроса от клиента
        :return: данные для клиента
        """

        path = self._request.path()
        method = self._request.method
        func_name = Flask._ROUTE_MAP.get((path, method))
        if not func_name:
            raise HTTPError(404, 'Not found')
        bl_module = importlib.import_module(Flask._HANDLE_MODULE_PATH)
        getattr(bl_module, func_name)()

    def run(self):
        self.serve_forever()

