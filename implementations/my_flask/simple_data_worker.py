from interfaces.i_data_worker import IDataWorker

class SimpleDataWorker(IDataWorker):
    __data = {}
    __user_id = 1
    
    @staticmethod
    def save_data(data):
        SimpleDataWorker.__data[SimpleDataWorker.__user_id] = data
        SimpleDataWorker.__user_id += 1

    @staticmethod
    def load_data():
        return SimpleDataWorker.__data
    
    @staticmethod
    def load_data_by_id(user_id):
        return SimpleDataWorker.__data.get(user_id)