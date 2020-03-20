import asyncio
import time


async def some_work():
    print('I some work')
    await asyncio.sleep(1)
    print('I some work again')


async def my_async_yield(init_val):
    for val in init_val:
        # тут есть блок операция и контекст переключится, потому что это асинхронный генератор
        print('start block operation')
        await asyncio.sleep(1)
        print('finish block operation')
        yield val


def my_yield(init_val):
    for val in init_val:
        # тут есть блок операция и контекст не переключится, потому что это простой генератор
        print('start block operation')
        time.sleep(1)
        print('finish block operation')
        yield val


# асинхронность может работать в простом генераторе, переключение между тасками происходит как надо
async def main():
    task = asyncio.create_task(some_work())

    for val in my_yield([1, 2, 3]):
        print(val)
        await asyncio.sleep(1)


# но бывает, что мы пишем генератор в котором могут происходить блокирующие операции
async def main1():
    task = asyncio.create_task(some_work())

    async for val in my_async_yield([1, 2, 3]):
        print(val)
        await asyncio.sleep(1)


if __name__ == '__main__':
    # неасинхронный вариант
    # asyncio.run(main())

    # асинхронный вариант
    asyncio.run(main1())
