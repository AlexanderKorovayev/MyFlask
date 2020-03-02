"""
модуль описывает базовую логику для работы с данными
"""


class IDataWorker:

    def __init__(self):
        self._container = None
        self._id = None

    def save_data(self, data):
        raise NotImplementedError

    def load_data(self):
        raise NotImplementedError

    def load_data_by_id(self, id_data):
        raise NotImplementedError
