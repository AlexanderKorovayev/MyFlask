import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class Session:

    def __init__(self):
        self._container = {}
        self._id = 1
        self._lock = threading.Lock()

    def save_data(self, data):
        with self._lock:
            self._container[self._id] = data
            time.sleep(3)
            self._id += 1

    def load_data(self):
        return self._container

    def load_data_by_id(self, id_data):
        return self._container.get(id_data)


db = Session()


def db_worker(val):
    print(f'start thread {val}\n{datetime.now().time()}\n')
    db.save_data(val)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        for val in range(2):
            print(f'in main\n{datetime.now().time()}\n')
            executor.submit(db_worker, val)

        print(f'in main, finish start threaded\n{datetime.now().time()}\n')

    print(f'finish threaded\n{datetime.now().time()}\n')
    print(db.load_data())
