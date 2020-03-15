import inspect
import asyncio


async def test():
    return 'test'

coro = test()

print(type(test))
print(type(coro))
print(inspect.iscoroutinefunction(test))
print(inspect.iscoroutine(coro))