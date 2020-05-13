import asyncio


async def test():
    return 5


async def f():
    rez = await test()
    return rez


try:
    coro = f()
    test = coro.send(None)
    print('test ' + test)
except StopIteration as e:
    print(e.value)
