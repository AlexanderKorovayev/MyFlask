"""
модуль реализующий непосредственно сам фреймворм
"""


from implementations.my_flask_multiprocessing.http_server import http_server
from base_errors.http_errors import HTTPError
from implementations.my_flask_multiprocessing.request import Request
from implementations.my_flask_multiprocessing.response import Response
from implementations.my_flask_multiprocessing.session import session
from interfaces.i_data_worker import IDataWorker
import inspect
import importlib
import platform
import utils
import threading
import multiprocessing
from datetime import datetime
import socket


class Flask(http_server.HTTPServer):
    _ROUTE_MAP = {}
    _HANDLE_MODULE_PATH = None

    def __init__(self, port, host_name='localhost', server_name='localhost'):
        super().__init__(host_name, port, server_name, Request, Response)
        self.os_name = platform.system()

        if threading.current_thread() == threading.main_thread():
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

    def serve_forever(self):
        """
        главная функция по обслуживанию клиента
        """
        print(f'{multiprocessing.current_process().name} in serve forever at {datetime.now().time()}')
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serv_sock.bind((self._host, self.port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                print(f'{multiprocessing.current_process().name} connect {_} at {datetime.now().time()}')
                if len(Flask._process) < multiprocessing.cpu_count() - 1:
                    p = multiprocessing.Process(target=Flask._task_listener, args=(Flask._queue,))
                    p.start()
                Flask._queue.put((Flask._serve_client, conn))

        finally:
            serv_sock.close()

    @staticmethod
    def _serve_client(conn):
        """
        обслуживание запроса(обработка запроса, выполнение запроса, ответ клиенту)
        :param conn: соединение с клиентом
        """
        print(f'start at {datetime.now().time()}')

        try:
            request = Flask._parse_request(conn)
            response = Flask._handle_request(request)
            Flask._send_response(conn, response)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            Flask._send_error(conn, e)

        if conn:
            conn.close()

        print(f'finish at {datetime.now().time()}')

    @staticmethod
    def _handle_request(request):
        """
        обработка запроса от клиента
        :request: объект запроса
        :return: данные для клиента
        """

        path = request.path()
        method = request.method
        func_name = Flask._ROUTE_MAP.get((path, method))
        if not func_name:
            raise HTTPError(404, 'Not found')
        bl_module = importlib.import_module(Flask._HANDLE_MODULE_PATH)
        return getattr(bl_module, func_name)(request)

    def run(self):
        self.serve_forever()

