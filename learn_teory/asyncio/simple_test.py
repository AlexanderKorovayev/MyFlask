import asyncio


async def block_io():
    print('start block')
    await asyncio.sleep(2)
    print('finish block')
    return 55


async def test():
    asyncio.create_task(block_io())
    print('hello')
    await asyncio.sleep(0.1)
    print('world')
    return 5


async def main():
    res = await test()
    print(res)
    # main это основная корутина и после её завершения все остальные дочерние корутины так же завершатся.
    # что бы предотвротить их завершение нобходимо собрать их в группу и дождаться завершения через gather 
    tasks = {el for el in asyncio.all_tasks() if el != asyncio.current_task()}
    print(tasks)
    res1 = await asyncio.gather(*tasks, return_exceptions=True)
    print(res1)


if __name__ == '__main__':
    asyncio.run(main())