from socket import *

serverHost = 'localhost'
serverPort = 2005

message = [b'POST /users?name=Vasya&age=42 HTTP/1.1\r\nHost: example.local\r\n']

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))

for line in message:
    sockobj.send(line)
    data = sockobj.recv(1024)
    print('Client received:', data)

sockobj.close()
