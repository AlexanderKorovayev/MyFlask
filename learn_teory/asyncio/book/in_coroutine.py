import asyncio


async def test():
    return 1

print(test)
coro = test()
print(coro)

try:
    coro.send(None)
except StopIteration as e:
    print(f'answer is {e.value}')
