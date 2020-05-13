import asyncio
import time


def block():
    time.sleep(1)
    return 5


async def wrap_block():
    res = await block()
    return res


async def main():
    task = asyncio.create_task(wrap_block())
    print('start work')
    asyncio.sleep(1)
    print('finish work')


asyncio.run(main())