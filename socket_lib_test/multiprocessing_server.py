import os
import time
from multiprocessing import Process
from socket import *
myHost = ''
myPort = 50007


def now():
    return time.ctime(time.time())


def handle_client(connection):
    print('Child:', os.getpid())                 # child process: reply, exit
    time.sleep(5)                                # simulate a blocking activity
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
        Process(target=handle_client, args=(connection,)).start()


if __name__ == '__main__':
    print('Parent:', os.getpid())
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.bind((myHost, myPort))
    sockobj.listen(5)
    dispatcher()
