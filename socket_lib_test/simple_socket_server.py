from socket import *

my_host = ''
my_port = 2005

sock_obj = socket(AF_INET, SOCK_STREAM)
sock_obj.bind((my_host, my_port))
sock_obj.listen(5)

while True:
    connection, address = sock_obj.accept()
    print('Server connected by', address)
    while True:
        data = connection.recv(1024)
        if not data:
            break
        connection.send(b'Echo=>' + data)
    connection.close()
