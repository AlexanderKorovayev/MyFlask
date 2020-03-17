import asyncio


async def background_job():
    pass


async def option_A(loop):
    loop.create_task(background_job())


async def option_B():
    asyncio.ensure_future(background_job())


async def option_C():
    loop = asyncio.get_event_loop()
    loop.create_task(background_job())


loop = asyncio.get_event_loop()
loop.create_task(option_A(loop))
loop.create_task(option_B)
loop.create_task(option_C)
