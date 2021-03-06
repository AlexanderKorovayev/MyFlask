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
    _queue = None
    _process = []

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
        IServer._queue = multiprocessing.Queue(100)


    @staticmethod
    def _task_listener(queue: multiprocessing.Queue):
        """
            функция ожидающая задачи
        """

        while True:
            if not queue.empty():
                task, args = queue.get()
                task(args)

    def serve_forever(self):
        """
        главная функция по обслуживанию клиента
        """

        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serv_sock.bind((self._host, self.port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                IServer._queue.put((IServer._serve_client, conn))
                
        finally:
            serv_sock.close()

    @staticmethod
    def _serve_client(conn):
        """
        обслуживание запроса(обработка запроса, выполнение запроса, ответ клиенту)
        :param conn: соединение с клиентом
        """

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
