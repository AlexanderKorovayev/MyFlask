import asyncio


class Echoprotocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print(f'connection from {transport.get_extra_info("peername")}')

    def data_received(self, data):
        message = data.decode()
        print(f'send back {message}')
        self.transport.write(data)

# плюс такого кода в том что мне не нужно придумывать самому бесконечного цыкла который
# принимает подключения и начинает их обрабатывать
# вместо этого включается эвент луп который сам умеет все принимать и обрабатывать


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    server_coro = loop.create_server(Echoprotocol, 'localhost', 2000)
    server = loop.run_until_complete(server_coro)
    loop.run_forever()
