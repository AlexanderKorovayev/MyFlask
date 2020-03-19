import asyncio


async def task(i):
    await asyncio.sleep(0.1)
    print(i)


async def main():
    for i in range(10):
        # благодаря новому get_running_loop теперь можно создавать таски без лупа
        asyncio.create_task(task(i))


# так как в main нет ожидания тасков, то main завершается быстрее чем таски начнут работать так как там есть слип
# главная курутина вызывает кансел у остальных объектов из лупа
# но можно дождаться их выполнения используя возможности лупа
asyncio.run(main())
