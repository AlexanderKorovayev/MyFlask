"""
Класс описывает контейнер для хранения данных во время работы сервера
"""

from interfaces.i_data_worker import IDataWorker


class Session(IDataWorker):

    _container = {}
    _id = 1

    @staticmethod
    def save_data(data):
        Session._container[Session._id] = data
        Session._id += 1

    @staticmethod
    def load_data():
        return Session._container

    @staticmethod
    def load_data_by_id(id_data):
        return Session._container.get(id_data)
