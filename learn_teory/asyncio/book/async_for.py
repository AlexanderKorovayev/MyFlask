import asyncio
import time


async def some_work():
    print('I some work')
    await asyncio.sleep(1)
    print('I some work again')


class MyAsyncFor:
    def __init__(self, val):
        self.val = val

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.val += 1
        # тут есть блок операция и контекст переключится, потому что это асинхронный итератор
        print('start block operation')
        await asyncio.sleep(1)
        print('finish block operation')
        if self.val == 5:
            raise StopAsyncIteration
        return self.val


class MyFor:
    def __init__(self, val):
        self.val = val

    def __iter__(self):
        return self

    def __next__(self):
        self.val += 1
        # тут есть блок операция, но контекст не перключается на другой таск, потому что итератор не асинхронных
        print('start block operation')
        time.sleep(1)
        print('finish block operation')
        if self.val == 5:
            raise StopIteration
        return self.val


# асинхронность может работать в простом итераторе, переключение между тасками происходит как надо
async def main():
    task = asyncio.create_task(some_work())

    for val in MyFor(0):
        print(val)
        await asyncio.sleep(1)


# но бывает, что мы пишем итератор в котором могут происходить блокирующие операции
async def main1():
    task = asyncio.create_task(some_work())

    async for val in MyAsyncFor(0):
        print(val)
        await asyncio.sleep(1)


if __name__ == '__main__':
    # неасинхронный вариант
    # asyncio.run(main())

    # асинхронный вариант
    asyncio.run(main1())
