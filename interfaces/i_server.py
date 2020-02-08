"""
Модуль описывает базовую логику http сервера
"""

import socket


class IServer:
    """
    класс, определяющий базовый функционал для сервера
    """
    def __init__(self, host_name, port_id, server_name):
        self._host = host_name
        self._port = port_id
        self._server_name = server_name
        self._rfile = None

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
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    self.send_error(conn, e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        """
        обслуживание запроса(обработка запроса, выполнение запроса, ответ клиенту)
        :param conn: соединение с клиентом
        """
        try:
            print("IN")
            self.parse_request(conn)
            print("IN1")
            resp = self.handle_request()
            print(resp)
            self.send_response(conn, resp)
            print('!!!')
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)
            print(e)

        if conn:
            print('CLOSE CONNECT')
            conn.close()

    def parse_request(self, conn):
        """
        разбор запроса от клиента
        :param conn:
        :return: объект запроса
        """
        raise NotImplementedError

    def handle_request(self):
        """
        обработка запроса от клиента
        :param req: объект запроса
        :return: данные для клиента
        """
        raise NotImplementedError

    def send_response(self, conn, resp):
        """
        Отправка ответа клиенту
        :param conn: сокет
        :param resp: объект ответа
        """
        raise NotImplementedError

    def send_error(self, conn, err):
        """
        конструирование объекта ошибки и его отправка
        :param conn: сокет
        :param err: ошибка
        """
        raise NotImplementedError
