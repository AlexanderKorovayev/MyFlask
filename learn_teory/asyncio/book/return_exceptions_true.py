import asyncio


async def f(delay):
    await asyncio.sleep(1/delay)
    return delay


async def main():
    loop = asyncio.get_running_loop()
    for i in range(2):
        loop.create_task(f(i))

    pending = asyncio.all_tasks()
    group = asyncio.gather(*pending, return_exceptions=True)
    results = loop.run_until_complete(group)
    print(f' result is {results}')
    loop.close()


if __name__ == '__main__':
    asyncio.run(main())