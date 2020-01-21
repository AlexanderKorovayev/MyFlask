class IServer:

    def __init__(self, port):
        self.port = port

    @staticmethod
    def post():
        raise NotImplementedError

    @staticmethod
    def get():
        raise NotImplementedError
