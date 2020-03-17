import asyncio


async def test():
    return 1

coro = test()

try:
    coro.send(None)
except StopIteration as e:
    print(f'answer is {e.value}')
