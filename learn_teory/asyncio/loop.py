import asyncio


async def f():
    await asyncio.sleep(0)
    return 111


loop = asyncio.get_event_loop()
coro = f()
print(loop.run_until_complete(coro))
