import time
import threading
from socket import *


myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))

sockobj.listen(5)


def now():
    return time.ctime(time.time())


def handle_client(connection):
    time.sleep(5)
    while True:
        data = connection.recv(1024)
        if not data:
            break
        reply = 'Echo=>{} at {}'.format(data, now())
        connection.send(reply.encode())
    connection.close()


def dispatcher():
    while True:
        connection, address = sockobj.accept()
        print('Server connected by', address, end=' ')
        print('at', now())
        threading.Thread(target=handle_client, args=(connection,)).start()


dispatcher()
