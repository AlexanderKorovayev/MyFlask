"""
По умолчанию обслуживает файлы и сценарии в текущем рабочем каталоге
и принимает соединения на порту 80, если не определены иные значения
для этих параметров с помощью аргументов командной строки;
CGI-сценарии на языке Python должны сохраняться в подкаталоге cgi-bin или htbin
в веб-каталоге; на одном и том же компьютере может быть запущено несколько
серверов для обслуживания различных каталогов при условии, что они
прослушивают разные порты;
"""

import os
from http.server import HTTPServer, CGIHTTPRequestHandler

webdir = '.'
port = 8000

os.chdir(webdir)  # перейти в корневой веб-каталог
srvraddr = ('', port)
srvrobj = HTTPServer(srvraddr, CGIHTTPRequestHandler)
print("server started")
srvrobj.serve_forever()
