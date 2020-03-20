import asyncio
from datetime import datetime


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i}) at {datetime.now().time()}")
        await asyncio.sleep(2)  # эмулируем блокировку ввода/вывода
        f *= i
    print(f"Task {name}: factorial({number}) = {f} at {datetime.now().time()}")


async def main():
    test = asyncio.gather(
                          factorial("A", 3),
                          factorial("B", 3),
                          factorial("C", 3)
                         )
    print('test')
    await test
    print('test1')

asyncio.run(main())
