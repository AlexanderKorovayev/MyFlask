from socket import *

serverHost = 'localhost'
serverPort = 50007

message = [b'Hello network world']

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))

for line in message:
    sockobj.send(line)
    data = sockobj.recv(1024)
    print('Client received:', data)

sockobj.close()


serverHost = 'localhost'
serverPort = 50008

message = [b'Hello network world']

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))

for line in message:
    sockobj.send(line)
    data = sockobj.recv(1024)
    print('Client received:', data)

sockobj.close()