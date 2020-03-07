"""
модуль для вспомогательных функций
"""

import multiprocessing
from queue import Queue
import time


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
    print('start task')
    time.sleep(sec)
    print('finish task')


def task_listener(queue: multiprocessing.Queue):
    while True:
        task = queue.get()
        task()


def create_process():
    """
    функция проверяет возможнеость создания процесса и создаёт его если это возможно либо помещает в очередь
    :return:
    """

    # создаю общую для потоков очередь, каждый поток создаётся и начинает работать бесконечно пока к нему не придёт
    # новая задача
    # задачи будут находиться в очереди из которой будут доставаться задачи

    # создадим очередь из максимум 100 задач
    queue = multiprocessing.Queue(100)
    processes = []
    for i in range(multiprocessing.cpu_count()):
        # передаём сюда прогу которая будет бесконечно ждать задачу,
        # эту задачу процесс будет забирать из очереди.
        p = multiprocessing.Process(target=task_listener, args=(queue,))
        p.start()
        p.join()
        processes.append(p)

    # главный поток получает задачу и помещает её в очередь
    # заполним сами очередь из заданий
    for i in range(8):
        queue.put(task(i))

    # в очереди будет содержаться таск и пид процесса который должен его обработать, все процессы вытаскивают пид и сверяют со своим

    # очередь потоко безопасна пока один процесс считывает из неё, остальные не могут обратиться к очереди(ПРОВЕРИТЬ!)
    # процесс взял из очереди задачу и начал выполнять её , соответственно он не возьмёти ещё задачу пока не выполнит взятую


create_process()
