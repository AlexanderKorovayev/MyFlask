import time
import asyncio
from datetime import datetime


async def main():
    print(f'{datetime.now().time()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{datetime.now().time()} Goodbye!')
    loop.stop()


def blocking():
    time.sleep(0.5)
    print(f"{datetime.now().time()} Hello from a thread!")


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_in_executor(None, blocking)
loop.run_forever()
pending = asyncio.Task.all_tasks(loop=loop)
group = asyncio.gather(*pending)
loop.run_until_complete(group)
loop.close()