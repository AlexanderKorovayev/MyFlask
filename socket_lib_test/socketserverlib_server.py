import socketserver
import time

myHost = ''
myPort = 50007


def now():
    return time.ctime(time.time())


class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.client_address, now())
        time.sleep(5)
        while True:
            # self.request – сокет клиента
            data = self.request.recv(1024)
            if not data:
                break
            reply = 'Echo=>{} at {}'.format(data, now())
            self.request.send(reply.encode())
        self.request.close()


# создать сервер с поддержкой многопоточной модели выполнения,
# слушать/обслуживать клиентов непрерывно
myaddr = (myHost, myPort)
server = socketserver.ThreadingTCPServer(myaddr, MyClientHandler)
server.serve_forever()
