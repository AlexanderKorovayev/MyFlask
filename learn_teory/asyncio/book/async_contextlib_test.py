import contextlib
import asyncio


@contextlib.asynccontextmanager
async def async_test():
    try:
        print('enter start, IO simulate')
        await asyncio.sleep(1)
        print('enter finish, IO simulate')

        yield 'test'

        print('exit start, IO simulate')
        await asyncio.sleep(2)
        print('exit finish, IO simulate')
    finally:
        print('in')


async def async_test1():
    print('in555')


async def main():
    task = asyncio.create_task(async_test1())
    async with async_test() as test:
        print('in main')
        print(test)


if __name__ == '__main__':
    asyncio.run(main())
