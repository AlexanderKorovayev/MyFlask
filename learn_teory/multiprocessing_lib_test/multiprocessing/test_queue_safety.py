import multiprocessing
from datetime import datetime
import time


def queue_setter(queue):
    print(f'{multiprocessing.current_process().name} start at {datetime.now().time()}')
    for i in range(3):
        queue.put(i)
        print(f'{multiprocessing.current_process().name} put at {datetime.now().time()}')
        time.sleep(0.001)
    print(f'{multiprocessing.current_process().name} finish at {datetime.now().time()}')


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=queue_setter, args=(queue,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not queue.empty():
        print(queue.get())
