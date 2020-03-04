import multiprocessing


def withdraw(balance, lock):
    for _ in range(10000):
        with lock:
            # lock.acquire()
            balance.value = balance.value - 1
            # lock.release()


def deposit(balance, lock):
    for _ in range(10000):
        with lock:
            # lock.acquire()
            balance.value = balance.value + 1
            # lock.release()


def perform_transactions():
    # initial balance (in shared memory)
    balance = multiprocessing.Value('i', 100)

    # creating a lock object
    lock = multiprocessing.Lock()

    # creating new processes
    p1 = multiprocessing.Process(target=withdraw, args=(balance, lock))
    p2 = multiprocessing.Process(target=deposit, args=(balance, lock))

    # starting processes
    p1.start()
    p2.start()

    # wait until processes are finished
    p1.join()
    p2.join()

    # print final balance
    print("Final balance = {}".format(balance.value))


if __name__ == "__main__":
    for _ in range(10):
        # perform same transaction process 10 times
        perform_transactions()
