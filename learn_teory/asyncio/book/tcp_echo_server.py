import asyncio


async def send_event(msg):
    await asyncio.sleep(1)


async def task():
    print('I TASK')


def test():
    print('I test')


async def echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print('new connection')
    try:
        while True: 
            data = await reader.read(100)
            if data:
                # проверим, что такой сервер способен принимать запросы пока загружен
                await asyncio.sleep(2)
                # test()
                writer.write(data.upper())
                # функция которая не позволяет писать в переполненный буфер
                # и ждёт момента когда снова можно будет писать если буфер переполнился
                await writer.drain()
            else:
                break
        print('leaving connection')
    # если есть подключение, то сервер создаёт таск, который закрывается если закрыть и сам сервер
    except asyncio.CancelledError:
        msg = 'connection dropped'
        print(msg)
        # но на этом этапе создаётся ещё один таск, который уже не попадёт в автоматический механизм закрытия
        asyncio.create_task(send_event(msg))


async def main(host='127.0.0.1', port=8888):
    # asyncio.create_task(task())
    server = await asyncio.start_server(echo, host, port)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bye')
