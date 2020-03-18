import asyncio
from datetime import datetime
import time


async def test(i):
    print(f'start test {i} at {datetime.now().time()}')
    await asyncio.sleep(1)
    print(f'finish test {i} at {datetime.now().time()}')


async def main():
    # на этом этапе таски начинают помещаться в эвент луп и если он свободен то начинают выполняться
    # но выполняться сразу они не всегда могут
    task1 = asyncio.create_task(test(1))
    task2 = asyncio.create_task(test(2))

    print(task1.done())
    await asyncio.sleep(1)
    # этот сли не переключит на таски
    # time.sleep(2)
    print(f'start imitation of work at {datetime.now().time()}')
    print(f'finish imitation of work at {datetime.now().time()}')
    await task1
    await task2


asyncio.run(main())
