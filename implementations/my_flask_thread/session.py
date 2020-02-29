"""
Класс описывает контейнер для хранения данных во время работы сервера
"""

from interfaces.i_data_worker import IDataWorker
import time


class Session(IDataWorker):

    def __init__(self):
        super().__init__()
        self._container = {}
        self._id = 1

    def save_data(self, data):
        time.sleep(1)
        self._container[self._id] = data
        self._id += 1

    def load_data(self):
        return self._container

    def load_data_by_id(self, id_data):
        return self._container.get(id_data)


session = Session()
