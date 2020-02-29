"""
Модуль описывает базовую логику http сервера
"""

import socket
from interfaces.i_request_thread import IRequest
from interfaces.i_response_thread import IResponse
import utils
import threading
from datetime import datetime


class IServer:
    """
    класс, определяющий базовый функционал для сервера
    """
    def __init__(self, host_name, port_id, server_name, request, response):
        self.port = port_id
        self.server_name = server_name
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
        """
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serv_sock.bind((self._host, self.port))
            serv_sock.listen()

            while True:
                print(f'IN MAIN {datetime.now().time()}\n')
                conn, _ = serv_sock.accept()

                # МНОГОПРОЦЕССОРНОСТЬ
                # фласк должен посчитать скалько ядер можно использовать, и параллелить запросы на их колличесвто
                # остальное помещать в очередь и вытаскивать когда одно из ядер освободится

                # МНОГОПОТОЧНОСТЬ
                # по сути многопоточнгость выполняется в одном главном потоке, поэтому нет особого смысла обрабатывать
                # параллельно несколько запросов от клиента в одном ядре
                # фласк будет иметь метод с транспортной задержкой, во время её работы он сможет обработать
                # остальные запросы из очереди
                # Но тут важно понимать один момент, если у нас много потоков то переключение между ними создаст время
                # и задержки, нужно понимать, больше или меньше время переключения чем задержка в каждом потоке

                # проблема производитель потребитель акктуальна для случаев, когда у потоков общий ресурс и надо
                # обращаться к нему поочереди

                # подумать как обращаться к общему объекту сессий, для кода это общий объект
                # дома написать код который многопоточно пишет данные в сессию
                # подумать как запуускать многопоточный код, через маин или нет, нужны ли джоины

                print(f'connected {_[1]}')
                threading.Thread(target=self._serve_client, args=(conn, _[1])).start()
                
        finally:
            serv_sock.close()

    def _serve_client(self, conn, pid):
        """
        обслуживание запроса(обработка запроса, выполнение запроса, ответ клиенту)
        :param conn: соединение с клиентом
        """
        try:
            print(f'thread {pid} started {datetime.now().time()}\n')
            request = self._parse_request(conn)
            print('REQUEST YES')
            response = self._handle_request(request)
            print('RESPONSE YES')
            self._send_response(conn, response)
            print('SEND RESPONSE YES\n')
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self._send_error(conn, e)

        if conn:
            conn.close()
        print(f'thread {pid} finish {datetime.now().time()}\n')

    def _parse_request(self, conn):
        """
        разбор запроса от клиента
        :param conn:
        :return: объект запроса
        """
        raise NotImplementedError

    def _handle_request(self, request):
        """
        обработка запроса от клиента
        :return: данные для клиента
        """
        raise NotImplementedError

    def _send_response(self, conn, response):
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
