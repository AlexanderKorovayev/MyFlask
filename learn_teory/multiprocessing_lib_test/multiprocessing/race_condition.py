import multiprocessing
from datetime import datetime


def plus(balance_val):
    print(f'{multiprocessing.current_process().name} balance {balance_val.value} start at {datetime.now().time()}\n')
    for _ in range(50):
        print(f'{multiprocessing.current_process().name} hold balance {balance_val.value} at {datetime.now().time()}\n')
        balance_val.value = balance_val.value + 1
        print(f'{multiprocessing.current_process().name} balance {balance_val.value} at {datetime.now().time()}\n')


def minus(balance_val):
    print(f'{multiprocessing.current_process().name} balance {balance_val.value} start at {datetime.now().time()}\n')
    for _ in range(50):
        print(f'{multiprocessing.current_process().name} hold balance {balance_val.value} at {datetime.now().time()}\n')
        balance_val.value = balance_val.value - 1
        print(f'{multiprocessing.current_process().name} balance {balance_val.value} at {datetime.now().time()}\n')


if __name__ == "__main__":
    balance = multiprocessing.Value('i', 100)

    print(f'in main at {datetime.now().time()}')
    p1 = multiprocessing.Process(target=plus, args=(balance,))
    p2 = multiprocessing.Process(target=minus, args=(balance,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Final balance = {}".format(balance.value))
