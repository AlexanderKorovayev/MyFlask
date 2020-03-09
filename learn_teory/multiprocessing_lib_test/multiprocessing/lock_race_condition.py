import multiprocessing
from datetime import datetime


def plus(balance_val, lock_obj):
    print(f'in {multiprocessing.current_process().name} balance {balance_val.value} start at {datetime.now().time()}\n')
    for _ in range(50):
        with lock_obj:
            # lock.acquire()
            print(f'{multiprocessing.current_process().name} hold balance {balance_val.value} at {datetime.now().time()}\n')
            balance_val.value = balance_val.value + 1
            # lock.release()


def minus(balance_val, lock_obj):
    print(f'in {multiprocessing.current_process().name} balance {balance_val.value} start at {datetime.now().time()}\n')
    for _ in range(50):
        with lock_obj:
            # lock.acquire()
            print(f'{multiprocessing.current_process().name} hold balance {balance_val.value} at {datetime.now().time()}\n')
            balance_val.value = balance_val.value - 1
            # lock.release()


if __name__ == "__main__":
    balance = multiprocessing.Value('i', 100)

    lock = multiprocessing.Lock()

    p1 = multiprocessing.Process(target=plus, args=(balance, lock))
    p2 = multiprocessing.Process(target=minus, args=(balance, lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Final balance = {}".format(balance.value))
