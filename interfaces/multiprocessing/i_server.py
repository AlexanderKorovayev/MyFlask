"""
Модуль описывает базовую логику http сервера
"""

import socket
from interfaces.threaded.i_request_thread import IRequest
from interfaces.threaded.i_response_thread import IResponse
import utils
import multiprocessing
from datetime import datetime


class IServer:
    """
    класс, определяющий базовый функционал для сервера
    """

    port = None
    server_name = None
    _host = None
    _request = None
    _response = None

    def __init__(self, host_name, port_id, server_name, request, response):
        IServer.port = port_id
        IServer.server_name = server_name
        IServer._host = host_name
        if not (utils.check_type(request, IRequest)):
            raise Exception('объект реквеста не соответствует заданным стандартам IRequest')
        if not (utils.check_type(response, IResponse)):
            raise Exception('объект респонса не соответствует заданным стандартам IResponse')
        IServer._request = request
        IServer._response = response
        # создадим очередь под максимальную нагрузку в 100 запросов
        self._queue = multiprocessing.Queue(100)
        for i in range(multiprocessing.cpu_count()-1):
            p = multiprocessing.Process(target=IServer._task_listener, args=(self._queue,))
            p.start()

    @staticmethod
    def _task_listener(queue: multiprocessing.Queue):
        """
            функция ожидающая задачи
        """
        print(f'{multiprocessing.current_process().name} start at {datetime.now().time()}')
        while True:
            if not queue.empty():
                task, args = queue.get()
                print(f'{multiprocessing.current_process().name} task is {task} i is {args} at {datetime.now().time()}\n')
                task(args)

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
                # очередб не принимает в себя почему-то self._serve_client
                self._queue.put((IServer._serve_client, conn))
                
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
            request = IServer._parse_request(conn)
            response = IServer._handle_request(request)
            IServer._send_response(conn, response)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            IServer._send_error(conn, e)

        if conn:
            conn.close()

        print(f'finish at {datetime.now().time()}')

    @staticmethod
    def _parse_request(conn):
        """
        разбор запроса от клиента
        :param conn:
        :return: объект запроса
        """
        raise NotImplementedError

    @staticmethod
    def _handle_request(request):
        """
        обработка запроса от клиента
        :return: данные для клиента
        """
        raise NotImplementedError

    @staticmethod
    def _send_response(conn, response):
        """
        Отправка ответа клиенту
        :param conn: сокет
        """
        raise NotImplementedError

    @staticmethod
    def _send_error(conn, err):
        """
        конструирование объекта ошибки и его отправка
        :param conn: сокет
        :param err: ошибка
        """
        raise NotImplementedError
