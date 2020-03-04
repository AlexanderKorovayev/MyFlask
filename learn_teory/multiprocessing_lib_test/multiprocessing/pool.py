import multiprocessing


def square(n):
    print(f'Worker process id for {n}: {multiprocessing.current_process().name}')
    return n*n


if __name__ == "__main__":
    # input list
    mylist = [1, 2, 3, 4, 5]

    # creating a pool object
    p = multiprocessing.Pool()

    # map list to target function
    result = p.map(square, mylist)

    print(result)
