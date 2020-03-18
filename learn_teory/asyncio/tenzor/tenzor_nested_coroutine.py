import asyncio
import time


async def say_after(delay, what):
    print(what)
    await asyncio.sleep(delay)


async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(2, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")


# так как курутины вызываются не в обёртке таска, то происходит последовательное выполнение
# потому что они не выполняются заранее
asyncio.run(main())
