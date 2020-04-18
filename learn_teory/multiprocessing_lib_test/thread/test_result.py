import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue


def test():
    return 5

def test_with_queue(queue: Queue):
    queue.put(5)


if __name__ == '__main__':
    # так результат не получить
    '''
    t = threading.Thread(target=test)
    test = t.start()
    print(test)
    '''
    # а так получить
    '''
    with ThreadPoolExecutor(max_workers=3) as executor:
        submit_object = executor.submit(test)
    res = submit_object.result()
    print(res)
    '''
    # и так тоже
    '''
    queue = Queue()
    p = threading.Thread(target=test_with_queue, args=(queue,))
    p.start()
    print(queue.get())
    '''
