from datetime import datetime
import threading
from socket import *
import time


myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))

sockobj.listen(5)


def now():
    return datetime.now().time()

def handle_client(connection):
    print(f'in handle, thread {threading.current_thread().name} start at {now()}\n')
    time.sleep(10)
    print(f'in handle, thread {threading.current_thread().name} at {now()}\n')
    while True:
        data = connection.recv(1024)
        if not data:
            break
        reply = 'Echo=>{} at {}'.format(data, now())
        connection.send(reply.encode())
    connection.close()
    print(f'in handle, thread {threading.current_thread().name} finish at {now()}\n')


def dispatcher():
    while True:
        print(f'in main, thread name is {threading.current_thread().name} at {now()}\n')
        connection, address = sockobj.accept()
        print('Server connected by', address, end=' ')
        print('at', now())
        threading.Thread(target=handle_client, args=(connection,)).start()


dispatcher()
