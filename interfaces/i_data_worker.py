"""
модуль описывает базовую логику работы с данными
"""

class IDataWorker:
    @staticmethod
    def save_data(user_id, data):
        raise NotImplementedError

    @staticmethod
    def load_data():
        raise NotImplementedError
    
    @staticmethod
    def load_data_by_id(user_id):
        raise NotImplementedError
