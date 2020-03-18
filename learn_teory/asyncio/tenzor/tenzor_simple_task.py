# Tasks
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    # особенность таска в том что он на этом этапе попадает в ивент луп
    # и если он не занят то таск начинает выполянться уже на этом моменте
    task1 = asyncio.create_task(say_after(1, 'hello'))

    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # тут важный нюанс подгодать, где ставить ожидание выполнение таска, нужно ставить примерно в том моменте
    # где выполниться таск который запускали
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
