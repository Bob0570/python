#for 3rd party on PROXI/ZOLOXI

import sys
import time
import struct
import requests
from vos.vos_misc import *
import openpyxl


xlsFileInfo = {'name':'http_app.xlsx', 'sheet':'list'}
http_port = 80 #self ip: 127.0.0.1
server_ip = '127.0.0.1'
hd_Token = {'Host':'11.22.33.44', 'Accept':'application/json', 'X-SS-AccessToken':'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=='}
pkg_key =  ['Type',	'Method', 'Url', 'Version', 'Header', 'Body', 'App', 'Ref']

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


while True:
    inputCmd = input('->')
    inList = inputCmd.split(' ')
    
    if(inList[0] == 'help'):
        appShowHelp()
        print('->')
        continue
    if(inputCmd == 'exit'):
        break
    if(inList[0] == ''):
        continue

    cmdIndex = int(inList[0])
    if cmdIndex >= len(pkg_list):
        print('unknow command\r\n->')
        continue

    pkg =pkg_list[cmdIndex]

    data = pkg['Method'] + ' ' + pkg['Url'] + ' ' +  pkg['Version'] + '\r\n' + pkg['Header'] + '\r\n\r\n' + pkg['Body']

    url = "http://" +server_ip + pkg['Url']
    json_dict = pkg['Body']
    headers = eval(pkg['Header']) #onvert str to dict
    if(pkg['Method'] == 'POST'):
        _resp = requests.post(url, data=json_dict, headers=headers, verify=False)
        result = _resp.text
    else:   
        _resp = requests.get(url, data=json_dict, headers=headers, verify=False)
        result = _resp.content

    print(result)

