import multiprocessing
import concurrent.futures
from datetime import datetime
import time


def square(val):
    print(f'process id is {multiprocessing.current_process().pid} at {datetime.now().time()}')
    print(f'process name is {multiprocessing.current_process().name}\n')
    time.sleep(0.1)
    print(val*val)


def cube(val):
    print(f'process id is {multiprocessing.current_process().pid } at {datetime.now().time()}')
    print(f'process name is {multiprocessing.current_process().name}\n')
    time.sleep(0.1)
    print(val*val*val)


if __name__ == '__main__':
    print(f'process id is {multiprocessing.current_process().pid}')
    print(f'process name is {multiprocessing.current_process().name}\n')

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        print(f'at {datetime.now().time()}')
        executor.submit(square, 5)
        executor.submit(cube, 5)

    print('finish')


