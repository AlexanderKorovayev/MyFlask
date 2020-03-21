import asyncio


async def test(delay):
    await asyncio.sleep(delay)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t1 = loop.create_task(test(1))
    t2 = loop.create_task(test(2))
    # t2.cancel()
    loop.run_until_complete(t1)
    loop.close()
