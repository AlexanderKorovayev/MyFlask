"""
модуль для вспомогательных функций
"""

import multiprocessing
from queue import Queue
import time
from datetime import datetime


def check_type(obj, base_type):
    """
    Метод проверки соответсвия объекта базовому типу
    :param obj: объект, который необходимо проверить
    :param base_type: базовый тип
    :return: True or False
    """
    rez = False

    if type(obj) == type:
        rez_object = obj
    else:
        rez_object = obj.__class__

    if rez_object.__name__ == 'object':
        return rez
    for base in rez_object.__bases__:
        if base.__name__ == base_type.__name__:
            rez = True
            return rez
        else:
            rez = check_type(base, base_type)
            if rez is True:
                return rez
    return rez


def task(sec):
    print(f'{multiprocessing.current_process().name} task start at {datetime.now().time()}\n')
    time.sleep(sec)
    print(f'{multiprocessing.current_process().name} task finish at {datetime.now().time()}\n')


def task_listener(queue: multiprocessing.Queue):
    print(f'{multiprocessing.current_process().name} start at {datetime.now().time()}')
    while True:
        if not queue.empty():
            task, i = queue.get()
            print(f'{multiprocessing.current_process().name} task is {task} i is {i} at {datetime.now().time()}\n')
            task(i)


def create_process():
    """
    функция проверяет возможнеость создания процесса и создаёт его если это возможно либо помещает в очередь
    :return:
    """

    print(f'{multiprocessing.current_process().name} start at {datetime.now().time()}')
    # создадим очередь размером 100 задач
    queue = multiprocessing.Queue(100)
    processes = []
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=task_listener, args=(queue,))
        p.start()
        processes.append(p)

    # главный поток получает задачу и помещает её в очередь
    # заполним сами очередь из заданий
    for i in range(12):
        queue.put((task, i))

    for p in processes:
        p.join()

    # в очереди будет содержаться таск и пид процесса который должен его обработать, все процессы вытаскивают пид и сверяют со своим

    # очередь потоко безопасна пока один процесс считывает из неё, остальные не могут обратиться к очереди(ПРОВЕРИТЬ!)
    # процесс взял из очереди задачу и начал выполнять её , соответственно он не возьмёти ещё задачу пока не выполнит взятую


create_process()
