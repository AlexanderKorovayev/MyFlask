"""
модуль описывает базовую логику для работы с данными
"""


class IDataWorker:

    @staticmethod
    def save_data(data):
        raise NotImplementedError

    @staticmethod
    def load_data():
        raise NotImplementedError

    @staticmethod
    def load_data_by_id(id_data):
        raise NotImplementedError
