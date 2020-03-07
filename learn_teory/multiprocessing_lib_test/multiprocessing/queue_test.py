import multiprocessing
from datetime import datetime
import time


def square_list(mylist, q):
    """
    function to square a given list
    """
    print(f'in {multiprocessing.current_process().name} at {datetime.now().time()}')
    for num in mylist:
        q.put(num * num)
        print(f'put {num * num} {datetime.now().time()}\n')
        time.sleep(0.001)


def print_queue(q):
    """
    function to print queue elements
    """
    print(f'in {multiprocessing.current_process().name} at {datetime.now().time()}\n')
    while True:
        if not q.empty():
            #print(q.get())
            print(f'get {q.get()} {datetime.now().time()}\n')


if __name__ == "__main__":
    # input list
    mylist = [1, 2, 3, 4]

    q = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=square_list, args=(mylist, q))
    p2 = multiprocessing.Process(target=print_queue, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
