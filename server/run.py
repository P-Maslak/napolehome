# -*- coding: utf-8 -*- ?
from http.server import HTTPServer, CGIHTTPRequestHandler
import socket 

server_address = ("", 80)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)

print("Сервер запущен на адресе: %s"%socket.gethostbyname_ex(socket.gethostname())[2][1])

httpd.serve_forever()