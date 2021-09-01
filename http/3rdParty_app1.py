#for 3rd party on PROXI/ZOLOXI

import sys
import os
import openpyxl
from http.client import HTTPConnection

xlsFileInfo = {'name':'http_app.xlsx', 'sheet':'list'}
http_port = 80 #self ip: 127.0.0.1
hd_Token = {'Host':'11.22.33.44', 'Accept':'application/json', 'X-SS-AccessToken':'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=='}
pkg_key = ['Type',	'Method', 'Url', 'Version', 'Header', 'Body', 'App', 'Ref']
conct = None

def appShowHelp():
    helpInfo = [
        "help                          show help info",
        "connect x.x.x.x               connect ip address",
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
    for row in ws_pkg[13:31]:
        pkg_val = list()
        for cells in row:
            pkg_val.append(cells.value)
        t_list = dict(zip(pkg_key, pkg_val))
        pkg_list.append(t_list)    
    return pkg_list


print("Welcome to 3rd Party APP!\r\n")
print("type help for help\r\n->")
pkg_list = mkPkgList(xlsFileInfo['name'])
#print(pkg_list)
#conct = HTTPConnection('127.0.0.1', http_port)
conct = HTTPConnection('10.16.10.33', http_port)

while True:
    inputCmd = input('->')
    inList = inputCmd.split(' ')
    
    if(inList[0] == 'connect'):
        conct = HTTPConnection(inList[1], http_port) #int(inList[2]))
        print('->')
        continue
    if(inList[0] == 'help'):
        appShowHelp()
        print('->')
        continue
    if(inputCmd == 'exit'):
        if(conct != None):
            conct.close()
        break

    if conct == None:
        print('type connect x.x.x.x #port fristly\r\n->')
        continue
    if(inList[0] == ''):
        continue
    cmdIndex = int(inList[0])
    if cmdIndex >= len(pkg_list):
        print('unknow command\r\n->')
        continue

    pkg =pkg_list[cmdIndex]
    head_dict = eval(pkg['Header']) #convert str to dict
    conct.request(pkg['Method'], pkg['Url'], pkg['Body'].encode('utf-8'), head_dict)           #发送请求报文

    res = conct.getresponse()          #获取响应报文对象
    print('res.status=' + str(res.status) + ', res.reason=' + res.reason + '\r\n->')
    print(res.read().decode('utf-8'))
