#for 3rd party on PROXI/ZOLOXI

import inspect
import ctypes
import sys
import time
import struct
import requests
import socket
import threading
import openpyxl
import re

#service========================================================================================
# 处理每一个请求
def serSockRecv(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    data = sock.recv(2048)
   
    request = data.decode('utf-8')
    request_list = request.split('\r\n\r\n')
    line_header = request_list[0]
    #body = request_list[1]

    request_list2 = line_header.split('\r\n', 1)
    request_line = request_list2[0]
    request_head = request_list2[1]

    line_list = request_line.split(' ')
    method = str(line_list[0].upper())
    url = line_list[1]
    protocol = line_list[2]
    body = sock.recv(2048)
    print("\r\n-->Server received below......\r\n")
    print(method)
    print(url)
    print(protocol)
    print(request_head)
    print(body)

    response_start_line = "HTTP/1.1 200 OK\r\n"
    #response_headers = "Content-Type: application/json; charset=utf-8\r\n\r\n"
    #response_body = "{\r\n\"apiKey\":\"wEAAAAAJ.....cfXlhIQ\"\r\n\"sessionToken\":\"YYYYYYYYYYYY==\"\r\n}"
    #response = response_start_line + response_headers + response_body
    response = response_start_line

    # 发送数据
    sock.send(response.encode('utf-8'))
    sock.close()

def serLinkTask():    
    # 开启服务器
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听端口:
    s.bind(('', 80))
    #s.bind(('', 443))
    s.listen(5)
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        print('connection to' + str(addr) + '\r\n->')
        # 创建新线程来处理TCP连接:
        tRecv = threading.Thread(target=serSockRecv, args=(sock, addr))
        tRecv.start()

def serLinkStart(ipaddr):
    print("Welcome to http server! - " + ipaddr)
    print('Waiting for connection...\r\n->')
    tLink = threading.Thread(target=serLinkTask)
    tLink.start()
    return tLink


#client===================================================================================================
xlsFileInfo = {'name':'http_app.xlsx', 'sheet':'list'}
http_port = 80 #self ip: 127.0.0.1
server_ip = '127.0.0.1' #'10.16.10.50'
startNo = 12
endNo = 34
req_head = {'Host':'10.16.13.1', 'Accept':'application/json', 'x-application-id':'123456789', 'X-SS-AccessToken':'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=='}
pkg_key =  ['Type',	'Method', 'Url', 'Version', 'Header', 'Body', 'App', 'Ref', 'apiKey']
apiKey = ''

def appShowHelp():
    helpInfo = [
        "help                          show help info",
        "serip x.x.x.x                server ip address",
        "-----------------------------------------------------------------------------------------------------------"]
    
    print(helpInfo[0])
    print(helpInfo[1])

    cnt = 0
    for pkg_item in pkg_list:
        print('%2d'%cnt + ': ' + pkg_item['Type'])
        cnt += 1
    print(helpInfo[2])    
    return

def mkPkgList(fileName):
    wb_pkg = openpyxl.load_workbook(fileName, data_only=True)
    ws_pkg = wb_pkg[xlsFileInfo['sheet']]
    pkg_list = list()
    #for row in ws_pkg.rows:
    #for row in ws_pkg[12:31]:
    for row in ws_pkg[startNo:endNo]:
        pkg_val = list()
        for cells in row:
            pkg_val.append(cells.value)
        t_list = dict(zip(pkg_key, pkg_val))
        pkg_list.append(t_list)    
    return pkg_list

hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)
#req_head['Host'] = ipaddr
req_head['Host'] = server_ip
#tLinkTask = serLinkStart(ipaddr)
print("Welcome to 3rd Party APP!\r\n")
print("type help for help\r\n->")
pkg_list = mkPkgList(xlsFileInfo['name'])
#print(pkg_list)

while True:
    inputCmd = input('->')
    inList = inputCmd.split(' ')
    
    if(inList[0] == 'help'):
        appShowHelp()
        print('->')
        continue
    if(inputCmd == 'exit'):
        #tLinkTask._stop()
        break
    if(inList[0] == 'serip'):
        server_ip = inList[1] 
        continue
    if(inList[0] == ''):
        continue

    cmdIndex = int(inList[0])
    if cmdIndex >= len(pkg_list):
        print('unknow command\r\n->')
        continue

    pkg =pkg_list[cmdIndex]
    #data = pkg['Method'] + ' ' + pkg['Url'] + ' ' +  pkg['Version'] + '\r\n' + pkg['Header'] + '\r\n\r\n' + pkg['Body']

    if((pkg['apiKey'] == 1) and (apiKey != '')):
        url = "http://" +server_ip + pkg['Url'] + '?key=' + apiKey
    else:
        url = "http://" +server_ip + pkg['Url']

    json_dict = pkg['Body'].encode('utf-8')
    #headers = eval(pkg['Header']) #onvert str to dict
    headers = req_head
    if (pkg['Method'] == 'POST'):
        _resp = requests.post(url, data=json_dict, headers=headers, verify=False)
        result = _resp.text
    elif (pkg['Method'] == 'PUT'):
        _resp = requests.put(url, data=json_dict, headers=headers, verify=False)
        result = _resp.text
    else:   
        _resp = requests.get(url, data=json_dict, headers=headers, verify=False)
        result = _resp.content

    print("\r\n-->Client received below reply......\r\n")
    print('res.status=' + str(_resp.status_code) + ', res.reason=' + _resp.reason + '\r\n->')
    print(result)

    #get X-SS-AccessToken - 181-01
    if '/rws/system/validate' in url:
        result_list = result.split('\r\n')
        for item in result_list:
            if 'sessionToken' in item:
                item_list = item.split(':')
                #AccessToken = item_list[1].replace('\"', '\"')
                AccessToken_tmp = re.findall('"(.*)"', item_list[1])
                AccessToken = AccessToken_tmp[0]
                req_head['X-SS-AccessToken'] = AccessToken
                print('set Token:'+AccessToken)

    #get key - 650-01
    if '/rws/system/exDisplay/register' in url:
        result_list = result.split('\r\n')
        for item in result_list:
            if 'apiKey' in item:
                item_list = item.split(':')
                #keyStr = item_list[1].replace('\"', '')
                keyStr = re.findall('"(.*)"', item_list[1])
                apiKey = keyStr[0]
                print('set apiKey:'+apiKey)
