import multiprocessing
from datetime import datetime


def withdraw(balance):
    print(f'{multiprocessing.current_process().name} balance {balance.value} start at {datetime.now().time()}\n')
    for _ in range(100):
        balance.value = balance.value - 1
        print(f'in {multiprocessing.current_process().name} balance {balance.value} at {datetime.now().time()}\n')


def deposit(balance):
    print(f'{multiprocessing.current_process().name} balance {balance.value} start at {datetime.now().time()}\n')
    for _ in range(100):
        balance.value = balance.value + 1
        print(f'in {multiprocessing.current_process().name} balance {balance.value} at {datetime.now().time()}\n')


def perform_transactions():
    balance = multiprocessing.Value('i', 100)

    print(f'in main at {datetime.now().time()}')
    p1 = multiprocessing.Process(target=withdraw, args=(balance,))
    p2 = multiprocessing.Process(target=deposit, args=(balance,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Final balance = {}".format(balance.value))


if __name__ == "__main__":
    for _ in range(1):
        # perform same transaction process 10 times
        perform_transactions()
