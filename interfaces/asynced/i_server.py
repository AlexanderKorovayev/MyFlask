"""
Модуль описывает базовую логику http сервера
"""

import socket
from interfaces.asynced.i_request_async import IRequest
from interfaces.asynced.i_response_async import IResponse
import utils
from datetime import datetime
import asyncio


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

    async def serve_forever(self):
        """
        главная функция по обслуживанию клиента
        """
        server = await asyncio.start_server(self._serve_client, self._host, self.port)

        async with server:
            print('start server')
            await server.serve_forever()

    async def _serve_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        обслуживание запроса(обработка запроса, выполнение запроса, ответ клиенту)
        :param conn: соединение с клиентом
        """
        print(f'connect at {datetime.now().time()}')
        try:
            request = await self._parse_request(reader)
            response = self._handle_request(request)
            await self._send_response(writer, response)
        except Exception as e:
            print(e)
            await self._send_error(writer, e)

        print(f'finish at {datetime.now().time()}')

    async def _parse_request(self, conn):
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

    async def _send_response(self, conn, response):
        """
        Отправка ответа клиенту
        :param conn: сокет
        """
        raise NotImplementedError

    async def _send_error(self, conn, err):
        """
        конструирование объекта ошибки и его отправка
        :param conn: сокет
        :param err: ошибка
        """
        raise NotImplementedError
