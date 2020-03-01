from socket import *


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


server_connect()
