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
                print(type(data))
                print(f'data is {data}')
                # проверим, что такой сервер способен принимать запросы пока загружен
                await asyncio.sleep(1)
                test()
                writer.write(data.upper())
                # функция которая не позволяет писать в переполненный буфер
                # и ждёт момента когда снова можно будет писать если буфер переполнился
                await writer.drain()
            else:
                break
        print('leaving connection')
    except asyncio.CancelledError:
        msg = 'connection dropped'
        print(msg)
        asyncio.create_task(send_event(msg))


async def main(host='127.0.0.1', port=8888):
    # asyncio.create_task(task())
    server = await asyncio.start_server(echo, host, port)

    async with server:
        print('in')
        await server.serve_forever()
        print('in1')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bye')
