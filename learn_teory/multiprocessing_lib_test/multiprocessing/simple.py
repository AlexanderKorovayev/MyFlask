import multiprocessing
import time


def square(val):
    time.sleep(2)
    print(f'process id is {multiprocessing.current_process().pid}')
    print(f'process name is {multiprocessing.current_process().name}\n')
    print(val*val)


def cube(val):
    time.sleep(2)
    print(f'process id is {multiprocessing.current_process().pid}')
    print(f'process name is {multiprocessing.current_process().name}\n')
    print(val*val*val)


if __name__ == '__main__':
    print(f'process id is {multiprocessing.current_process().pid}')
    print(f'process name is {multiprocessing.current_process().name}\n')

    p1 = multiprocessing.Process(target=square, args=(5,))
    p2 = multiprocessing.Process(target=cube, args=(5,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print('finish')


