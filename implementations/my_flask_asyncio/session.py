"""
Класс описывает контейнер для хранения данных во время работы сервера
"""

from interfaces.i_data_worker import IDataWorker
import time
import asyncio


class Session(IDataWorker):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IDataWorker, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self._container = {}
        self._id = 1

    async def save_data(self, data):
        # симуляция задержки IO
        await asyncio.sleep(1)
        self._container[self._id] = data
        self._id += 1

    async def load_data(self):
        # симуляция задержки IO
        await asyncio.sleep(1)
        return self._container

    async def load_data_by_id(self, id_data):
        # симуляция задержки IO
        await asyncio.sleep(1)
        return self._container.get(id_data)


session = Session()
