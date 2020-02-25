from socket import *
import threading
import multiprocessing


serverHost = 'localhost'
serverPort = 2005

message = b'TEST'
sockobj = socket(AF_INET, SOCK_STREAM)


def server_connect():

    sockobj.connect((serverHost, serverPort))

    sockobj.send(message)
    data = sockobj.recv(1024)
    print('Client received:', data)

    sockobj.close()


#server_connect()


if __name__ == '__main__':

    print('start thread')

    thread_pool = []

    for i in range(4):
        thread = multiprocessing.Process(target=server_connect)
        thread.start()

    for i in thread_pool:
        i.join()

    print('finish thread')

