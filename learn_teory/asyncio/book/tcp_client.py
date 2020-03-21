import socket


sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def server_connect():

    sockobj.connect(('localhost', 8888))

    sockobj.send(b'test')
    print('sended')
    data = sockobj.recv(1024)
    print('received')
    print('Client received:', data)

    sockobj.close()


server_connect()