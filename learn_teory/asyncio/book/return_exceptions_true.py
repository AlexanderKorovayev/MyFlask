import asyncio


async def f(delay):
    await asyncio.sleep(1/delay)
    return delay


async def main():
    '''
    tasks = []
    for i in range(2):
        tasks.append(asyncio.create_task(f(i)))

    pending = asyncio.all_tasks()
    # print(pending)
    group = asyncio.gather(*pending, return_exceptions=True)
    #await group
    print(f' result is {group}')
    '''
    group = await asyncio.gather(f(0), f(1), return_exceptions=True)
    print(group)

if __name__ == '__main__':
    asyncio.run(main())