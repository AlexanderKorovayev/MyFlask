import multiprocessing
import time

def multiprocessing_func(x):
    time.sleep(2)
    print(f'for {x} squared is {x*x}')

if __name__ == '__main__':    
    starttime = time.time()
    processes = []
    for i in range(0,10):
        # multiprocessing_func(i)
        p = multiprocessing.Process(target=multiprocessing_func, args=(i,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print(f'time spended: {time.time() - starttime} second')