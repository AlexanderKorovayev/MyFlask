import asyncio


async def main():
    print('hello')
    # в этот момент мы сообщаем ивент лупу что будет происходить долгая операция во время которой можно переключиться
    # на другие задачи
    await asyncio.sleep(1)
    print('world')


# корутину нельзя запустить просто так, она не запустится
# main()

asyncio.run(main())


