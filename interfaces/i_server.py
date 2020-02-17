"""
Модуль описывает базовую логику http сервера
"""

import socket
from interfaces.i_request import IRequest
from interfaces.i_response import IResponse
import utils


class IServer:
    """
    класс, определяющий базовый функционал для сервера
    """
    def __init__(self, host_name, port_id, server_name, request, response):
        self.port = port_id
        self.server_name = server_name
        self._rfile = None
        self._host = host_name
        if not (utils.check_type(request, IRequest)):
            raise Exception('объект реквеста не соответствует заданным стандартам IRequest')
        if not (utils.check_type(response, IResponse)):
            raise Exception('объект респонса не соответствует заданным стандартам IResponse')
        self._request = request
        self._response = response

    def serve_forever(self):
        """
        главная функция по обслуживанию клиента
        TODO сделать обслуживание асинхронным или многопроцессорным
        """
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serv_sock.bind((self._host, self.port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self._serve_client(conn)
                except Exception as e:
                    self._send_error(conn, e)
        finally:
            serv_sock.close()

    def _serve_client(self, conn):
        """
        обслуживание запроса(обработка запроса, выполнение запроса, ответ клиенту)
        :param conn: соединение с клиентом
        """
        try:
            print("IN")
            self._parse_request(conn)
            print("IN1")
            self._response = self._handle_request()
            print(self._response)
            self._send_response(conn)
            print('!!!')
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self._send_error(conn, e)
            print(e)

        if conn:
            print('CLOSE CONNECT')
            conn.close()

    def _parse_request(self, conn):
        """
        разбор запроса от клиента
        :param conn:
        :return: объект запроса
        """
        raise NotImplementedError

    def _handle_request(self):
        """
        обработка запроса от клиента
        :return: данные для клиента
        """
        raise NotImplementedError

    def _send_response(self, conn):
        """
        Отправка ответа клиенту
        :param conn: сокет
        """
        raise NotImplementedError

    def _send_error(self, conn, err):
        """
        конструирование объекта ошибки и его отправка
        :param conn: сокет
        :param err: ошибка
        """
        raise NotImplementedError
