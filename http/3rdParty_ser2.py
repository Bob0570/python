import sys
import time
import struct
import socket
import threading
from vos.vos_misc import *
 
# 处理每一个请求
def serSockRecv(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    data = sock.recv(2048)
   
    request = data.decode('utf-8')
    request_list = request.split('\r\n\r\n')
    line_header = request_list[0]
    body = request_list[1]

    request_list2 = line_header.split('\r\n', 1)
    request_line = request_list2[0]
    request_head = request_list2[1]

    line_list = request_line.split(' ')
    method = str(line_list[0].upper())
    url = line_list[1]
    protocol = line_list[2]
    print(method)
    print(url)
    print(protocol)
    print(request_head)
    print(body)

    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: received\r\n"
    response_body = "<h1>Python HTTP Test</h1>"
    response = response_start_line + response_headers + "\r\n" + response_body

    # 发送数据
    sock.send(response.encode('utf-8'))
    sock.close()


print("Welcome to http server!\r\n->")
# 开启服务器
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
s.bind(('', 80))
s.listen(5)
print('Waiting for connection...')
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=serSockRecv, args=(sock, addr))
    t.start()


