from datetime import datetime
import asyncio


async def main():
    print(f'{datetime.now().time()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{datetime.now().time()} Goodbye!')
    loop.stop()


loop = asyncio.get_event_loop()
loop.create_task(main())
# запускается бесконечный цыкл ожидания заданий, пока кто-то не вызовет loop.stop()
loop.run_forever()
print('in')
# собираем таски которые были в цикле, возможно не все выполнелись 
pending = asyncio.Task.all_tasks(loop=loop)
# доработка всех неуспевшых доработать в цыкле задач
group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()