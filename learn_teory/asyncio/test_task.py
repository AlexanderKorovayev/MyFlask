import asyncio
from datetime import datetime
import time


async def test(i):
    print(f'start test {i} at {datetime.now().time()}')
    await asyncio.sleep(0.1)
    print(f'finish test {i} at {datetime.now().time()}')


async def main():
    # на этом этапе таски начинают помещаться в эвент луп и если он свободен то начинают выполняться
    # но выполняться сразу они не всегда могут
    task1 = asyncio.create_task(test(1))
    task2 = asyncio.create_task(test(2))

    # обычный sleep не переключит контекст
    # time.sleep(2)

    loop = asyncio.get_event_loop()
    print(f'loop is runing {loop.is_running()}')

    print(f'check if task is done - {task1.done()}, at {datetime.now().time()}')

    print(f'start imitation of work at {datetime.now().time()}')
    await asyncio.sleep(1)
    print(f'finish imitation of work at {datetime.now().time()}')

    await task1
    await task2

    print(f'check if task is done - {task1.done()}, at {datetime.now().time()}')

asyncio.run(main())
