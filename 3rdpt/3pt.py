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

import tkinter
import tkinter.messagebox
from  tkinter import END

sys.path.append("../")
from vos.vos_draw import Vosdraw as Vosui
from vos.vos_misc import *

g_other = {'apiKey':'', 'status':'power on', 'command':99}
#service========================================================================================
def serRecvPkt(body):
    body2 = eval(body)
    event = body2['event']
    statusLabl = my_list[3]['object']
    if(event == 'authServiceState'):
        state = body2['data']['authServiceState']['state']
        if(state == 'login_started'):
            usr_name = my_list[10]['object'].get()
            pass_word = my_list[12]['object'].get()
            pin_code = my_list[14]['object'].get()
            body_usr_name = body2['data']['authInfo']['userID']
            body_pass_word = body2['data']['authInfo']['password']
            body_pin_code = body2['data']['authInfo']['pinnumber']
            if(usr_name == body_usr_name):
                if(pass_word == body_pass_word):
                    g_other['command'] = 4 #auth pass     
                else:
                    g_other['command'] = 99 #auth timeout  
            elif(pin_code == body_pin_code):      
                g_other['command'] = 4 #auth pass   
            else:
                g_other['command'] = 5 #auth fail   
        elif(state == 'user_login'):
            g_other['command'] = 6 #display APP 
            statusLabl['text'] = 'APP dialog'
        elif(state == 'system_started'):
            #httpClt_send(server_ip, pkg_list[0]) #get Token
            g_other['command'] = 0 #get Token
            vos_taskSleep(200)
            #httpClt_send(server_ip, pkg_list[1]) #register_UI
            g_other['command'] = 1 #register_UI
            vos_taskSleep(200)
            g_other['command'] = 2 #send register_IC
            vos_taskSleep(200)
            g_other['command'] = 3 #send Authentication
            vos_taskSleep(200)
    if(event == 'applicationChange'):
        select_app = body2['data']['selectedApp']['app']
        status_app = body2['data']['selectedApp']['status']
        if(select_app == 'print'):
            if(status_app == 'waiting'):
                g_other['command'] = 7 #display print dialog
                statusLabl['text'] = 'print dialog'
            elif(status_app == 'start'):
                g_other['command'] = 8 #send Print Dialog Parameter and get responds: 650_103
                logout('please do 3rd printing\r\n')
            elif(status_app == 'executing'):
                logout('3rd printing executing...\r\n')
                statusLabl['text'] = 'print...'
        if(select_app == 'scan'):
            if(status_app == 'waiting'):
                g_other['command'] = 9 #display scan dialog
                statusLabl['text'] = 'scan dialog'
            elif(status_app == 'start'):
                g_other['command'] = 10 #send scan Dialog Parameter and get responds: 650_107
            elif(status_app == 'executing'):
                logout('3rd printing executing...\r\n')
                statusLabl['text'] = 'print...'
        if(select_app == 'device'):
            g_other['command'] = 13 #display billingCode dialog: 650_123
            statusLabl['text'] = 'billingCode dialog'

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
    body = sock.recv(1024*8)
    logout("\r\n-->Server received below......\r\n")
    logout(method)
    logout(url)
    logout(protocol)
    logout(request_head)
    logout(body)

    response_start_line = "HTTP/1.1 200 OK\r\n"
    #response_headers = "Content-Type: application/json; charset=utf-8\r\n\r\n"
    #response_body = "{\r\n\"apiKey\":\"wEAAAAAJ.....cfXlhIQ\"\r\n\"sessionToken\":\"YYYYYYYYYYYY==\"\r\n}"
    #response = response_start_line + response_headers + response_body
    response = response_start_line

    # 发送数据
    sock.send(response.encode('utf-8'))
    sock.close()

    body2 = body.decode('utf-8')
    serRecvPkt(body2)

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
        logout('connection to' + str(addr) + '\r\n->')
        # 创建新线程来处理TCP连接:
        tRecv = threading.Thread(target=serSockRecv, args=(sock, addr))
        tRecv.start()

def serLinkStart(ipaddr):
    logout("Welcome to http server! - " + ipaddr+ "\r\n->")
    logout('Waiting for connection...\r\n->')
    tLink = threading.Thread(target=serLinkTask)
    tLink.start()
    return tLink


#client===================================================================================================
xlsFileInfo = {'name':'http_app.xlsx', 'sheet':'3pt'}
http_port = 80 #self ip: 127.0.0.1
startNo = 2
endNo = 29
req_head = {'Host':'10.16.13.1', 'Accept':'application/json', 'x-application-id':'123456789', 'X-SS-AccessToken':'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=='}
pkg_key =  ['Command', 'Type',	'Method', 'Url', 'Version', 'Header', 'Body', 'App', 'Ref', 'apiKey']

def mkPkgList(fileName):
    wb_pkg = openpyxl.load_workbook(fileName, data_only=True)
    ws_pkg = wb_pkg[xlsFileInfo['sheet']]
    pkg_list = list()
    #for row in ws_pkg.rows:
    endNo = ws_pkg.max_row
    for row in ws_pkg[startNo:endNo]:
        pkg_val = list()
        for cells in row:
            pkg_val.append(cells.value)
        t_list = dict(zip(pkg_key, pkg_val))
        pkg_list.append(t_list)    
    return pkg_list

def httpClt_send(server_ip, pkg):
    http_header = 'http://'
    if(http_port == 443):
        http_header = 'https://'
    apiKey = g_other['apiKey']
    if((pkg['apiKey'] == 1) and (apiKey != '')):
        url = "http://" +server_ip + pkg['Url'] + '?key=' + apiKey
    else:
        url = "http://" +server_ip + pkg['Url']

    json_dict = pkg['Body'].encode('utf-8')
#headers = eval(pkg['Header']) #onvert str to dict
    req_head['Host'] = server_ip
    headers = req_head
    if (pkg['Method'] == 'POST'):
        _resp = requests.post(url, data=json_dict, headers=headers, verify=False)
        result = _resp.text
    elif (pkg['Method'] == 'PUT'):
        _resp = requests.put(url, data=json_dict, headers=headers, verify=False)
        result = _resp.text
    elif (pkg['Method'] == 'DELETE'):
        _resp = requests.delete(url, data=json_dict, headers=headers, verify=False)
        result = _resp.text    
    else:   
        _resp = requests.get(url, data=json_dict, headers=headers, verify=False)
        result = _resp.content

    logout("\r\n-->Client send \"" + pkg['Command'] + "\" and received below reply......\r\n")
    logout('res.status=' + str(_resp.status_code) + ', res.reason=' + _resp.reason + '\r\n->')
    logout(result)

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
                logout('set Token:'+AccessToken)

#get key - 650-01
    if '/rws/system/exDisplay/register' in url:
        result_list = result.split('\r\n')
        for item in result_list:
            if 'apiKey' in item:
                item_list = item.split(':')
                #keyStr = item_list[1].replace('\"', '')
                keyStr = re.findall('"(.*)"', item_list[1])
                apiKey = keyStr[0]
                g_other['apiKey'] = apiKey
                logout('set apiKey:'+apiKey)

#get scan param - 650-107
    if '/rws/system/exDisplay/scannerDialogInputParameter' in url:
        #g_other['command'] = 11 #check scan param 320_02 for check
        g_other['command'] = 12 #start scan 320_02 for start
        statusLabl = my_list[3]['object']
        statusLabl['text'] = 'check scan param'

    logout("\r\n-->")

def clientTask(root, pkg_list, my_list):    
    while True:
        cmdSelect = g_other['command']
        if( cmdSelect == 99):
            vos_taskSleep(100)
        else:
            server_ip = my_list[1]['object'].get()
            '''
            if(cmdSelect == 3): #认证
                httpClt_send(server_ip, pkg_list[0]) #get Token
                vos_taskSleep(100)
                httpClt_send(server_ip, pkg_list[1]) #register_UI
                vos_taskSleep(100)
            '''
            g_other['command'] = 99
            if(cmdSelect>12):
                cmdSelect = cmdSelect + my_list[15]['object'].current()
            pkg =pkg_list[cmdSelect] #
            httpClt_send(server_ip, pkg)
            cmdText = pkg['Command']
            statusLabl = my_list[3]['object']
            statusLabl['text'] = cmdText

my_list=[
    {'type':'label', 	'pos_xy':[ 10,20], 	'size_wh':[ 70,30],     'text':'Serv ip:',      'command':None, 'object':None}, 
    {'type':'entry', 	'pos_xy':[ 80,20], 	'size_wh':[100,30],     'text':'10.16.12.61',   'command':None, 'object':None}, 
    #2
    {'type':'label', 	'pos_xy':[200,20], 	'size_wh':[ 60,30],     'text':'Status:',      'command':None, 'object':None}, 
    {'type':'label', 	'pos_xy':[260,20], 	'size_wh':[220,30],     'text':'Power On',     'command':None, 'object':None}, 
    {'type':'label', 	'pos_xy':[490,20], 	'size_wh':[ 80,30],     'text':'user name:',   'command':None, 'object':None}, 
    {'type':'label', 	'pos_xy':[610,20], 	'size_wh':[200,30],     'text':' ',             'command':None, 'object':None}, 
    {'type':'button', 	'pos_xy':[1180,10], 'size_wh':[110,40],     'text':'exit',          'command':None, 'object':None},
    #7:
    {'type':'button', 	'pos_xy':[ 20,60], 	'size_wh':[ 90,30],     'text':'发送',          'command':None, 'object':None},
    {'type':'rdbutton', 'pos_xy':[110,60],  'size_wh':[140,30],     'text':[],              'option':None, 'object':None, 'direct':'Horizen'},
    {'type':'listtext', 'pos_xy':[ 10,130], 'size_wh':[1300,738],   'text':'list',          'command':None, 'object':None},
    #10
    {'type':'entry', 	'pos_xy':[580,20], 	'size_wh':[100,30],     'text':'JS',            'command':None, 'object':None}, 
    {'type':'label', 	'pos_xy':[700,20], 	'size_wh':[ 80,30],     'text':'pass word:',    'command':None, 'object':None}, 
    {'type':'entry', 	'pos_xy':[790,20], 	'size_wh':[100,30],     'text':'123',           'command':None, 'object':None}, 
    {'type':'label', 	'pos_xy':[900,20], 	'size_wh':[ 80,30],     'text':'pin code:',     'command':None, 'object':None}, 
    {'type':'entry', 	'pos_xy':[980,20], 	'size_wh':[160,30],     'text':'456',           'command':None, 'object':None}, 
    {'type':'combobox', 'pos_xy':[920,90],  'size_wh':[250,30],     'text':('aa','bb'),     'command':None, 'object':None}, 
    {'type':'button', 	'pos_xy':[1180,90], 'size_wh':[100,30],     'text':'clear log',     'command':None, 'object':None},
]

def logout(info):
    logList = my_list[9]['object']
    logList.insert('end', info)
    logList.yview_moveto(1)

def exit3pt():
    #sys.exit(0)
    os._exit(0)

def clearLog():
    logList = my_list[9]['object']
    logList.delete(1.0, END)

def commandProc():
    cmdSelect = my_list[8]['option'].get()
    cmdText = my_list[8]['text'][cmdSelect]
    g_other['command'] = cmdSelect

comboboxList = []
pkg_list = mkPkgList(xlsFileInfo['name'])
#print(pkg_list)
i = 0
for pkg_item in pkg_list:
    if(i<13):
        my_list[8]['text'].append(pkg_item['Command'])
    else:
        comboboxList.append(pkg_item['Command'])
    i += 1
my_list[8]['text'].append('other:')
my_list[15]['text'] = tuple(comboboxList)

root = tkinter.Tk()
root.title('3rd Party')
root.geometry('1320x900+10+10')
my_draw = Vosui(root)

my_list[7]['command']= commandProc
my_list[6]['command']= exit3pt
my_list[16]['command']= clearLog
my_draw.drawList(my_list)
my_list[8]['option'].set(3) #default for 认证
my_list[15]['object'].current(0)

#service task create=======================================================
hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)
#req_head['Host'] = ipaddr
tLinkTask = serLinkStart(ipaddr)

#client task create=========================================================
pClientTask = threading.Thread(target=clientTask, args=(root, pkg_list, my_list))
pClientTask.setDaemon(True)
pClientTask.start()

logout("Welcome to 3rd Party APP!\r\n")
logout('\r\n->')
root.mainloop()

    
