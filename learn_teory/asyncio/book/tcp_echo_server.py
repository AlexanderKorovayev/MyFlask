import asyncio


async def send_event(msg):
    await asyncio.sleep(1)


async def echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print('new connection')
    try:
        while data := await reader.readline():
            print('in')
            print(f'data is {data}')
            writer.write(data.upper())
            await writer.drain()
        print('leaving connection')
    except asyncio.CancelledError:
        msg = 'connection dropped'
        print(msg)
        asyncio.create_task(send_event(msg))


async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bye') 