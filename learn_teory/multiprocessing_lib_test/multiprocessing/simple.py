import multiprocessing
import concurrent.futures


def square(val):
    print(f'process id is {multiprocessing.current_process().pid}')
    print(f'process name is {multiprocessing.current_process().name}\n')
    print(val*val)


def cube(val):
    print(f'process id is {multiprocessing.current_process().pid}')
    print(f'process name is {multiprocessing.current_process().name}\n')
    print(val*val*val)


if __name__ == '__main__':
    print(f'process id is {multiprocessing.current_process().pid}')
    print(f'process name is {multiprocessing.current_process().name}\n')

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        executor.submit(square, 5)
        executor.submit(cube, 5)

    print('finish')


