import asyncio


# в целом, когда работаем с выражениями листа то перебираем в них какой нибудь встроенный объект
# но иногда приходится создавать свой объект
async def my_comprehensions_async():
    for i in [1, 2, 3, 4, 5]:
        print('in comprehension')
        yield i
        await asyncio.sleep(1)


async def test_task():
    print('in task')
    await asyncio.sleep(10)
    print('out task')


async def main():
    task = asyncio.create_task(test_task())
    #await test_task()
    result = [el async for el in my_comprehensions_async()]
    # главнвя функция может завершится быстрее тасков которые есть ещё, поэтому один из способов ожидания их завершения
    # это await task
    if not task.done():
        await task 


if __name__ == '__main__':
    asyncio.run(main())