class HTTPError(Exception):
    """
    ксласс обработчик запросов
    """
    def __init__(self, status, reason, body=None):
        super()
        self.status = status
        self.reason = reason
        self.body = body