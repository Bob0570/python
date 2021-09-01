#vct using for windows GUI

import tkinter
import tkinter.messagebox
import struct
import sys

sys.path.append("../")
from vos.vos_draw import Vosdraw as Vosui
from vos import vos_sock as vsock

VCT_NORMAL_CMD = 0xbeaf1000
RPC_val = [0,           0,      VCT_NORMAL_CMD, [0]*8,      0,          ''*64,         ''*512]
my_list=[
    {'type':'label', 	'pos_xy':[ 10,20], 	'size_wh':[100,30],     'text':'ip address:',   'command':None, 'object':None}, 
    {'type':'entry', 	'pos_xy':[120,20], 	'size_wh':[150,30],     'text':'10.16.10.',        'command':None, 'object':None}, 
    {'type':'button', 	'pos_xy':[280,20], 	'size_wh':[100,30],     'text':'connect',       'command':None, 'object':None},
    {'type':'listtext', 'pos_xy':[  0,50], 	'size_wh':[1200,800],   'text':'list',          'command':None, 'object':None},
    {'type':'entry', 	'pos_xy':[ 80,850], 'size_wh':[1150,30],    'text':'help',       'command':None, 'object':None}, 
    {'type':'label', 	'pos_xy':[  0,850], 'size_wh':[  80,30],    'text':'command:',      'command':None, 'object':None}, 
    #6
    {'type':'button', 	'pos_xy':[950,10], 'size_wh':[100,40],     'text':'clear log',     'command':None, 'object':None},
    {'type':'button', 	'pos_xy':[1080,10], 'size_wh':[100,40],     'text':'exit',          'command':None, 'object':None},
]

def logout(info):
    logList = my_list[3]['object']
    logList.insert('end', info)
    logList.yview_moveto(1)

def exitVct():
    os._exit(0)

def clearLog():
    logList = my_list[3]['object']
    logList.delete(1.0, END)

def dvctSockRecv(data):
    logout(data.decode())

def cmdLineProc(ev = None):
    cmdLine = my_list[4]['object'].get()
    cmdInfo = '\r\n->'+cmdLine+'\r\n'
    logout(cmdInfo)
    if(clt_sock.status == 1) and (cmdLine != ''):
        RPC_val[5] = ' '
        data = struct.pack('3I8II64s512s', *RPC_val[:3], *RPC_val[3], RPC_val[4], RPC_val[5].encode(), cmdLine.encode())
        clt_sock.vos_sockSendall(data)        

def connectProc():
    if(clt_sock.status == 0):
        ipAddr = my_list[1]['object'].get()
        clt_sock.vos_sockConnect(28901, ipAddr, dvctSockRecv)
        connectInfo = 'connect done:'+ipAddr
        logout(connectInfo)

        buttonCon = my_list[2]['object']
        buttonCon['text'] = 'disconnect'
    else:
        strSend = 'bye'
        clt_sock.vos_sockSendall(strSend.encode())
        vos_taskSleep(200)
        clt_sock.vos_sockClose()
        logout('disconnet')
        
        buttonCon = my_list[2]['object']
        buttonCon['text'] = 'connect'
    
root = tkinter.Tk()
root.title('python VCT')
root.geometry('1200x900+10+10')
my_draw = Vosui(root)

#ipAddr = tkinter.StringVar(value='10.16.10.')
#my_list[1]['text']= ipAddr
#cmdLine = tkinter.StringVar(value='')
#my_list[4]['text']= cmdLine

my_list[2]['command']= connectProc
my_list[6]['command']= clearLog
my_list[7]['command']= exitVct
my_draw.drawList(my_list)

cmdObj = my_list[4]['object']
cmdObj.bind("<Return>", cmdLineProc)
logList = my_list[3]['object']

clt_sock = vsock.Sock_clt()

logout('welcom to vct!')
logout('\r\n->')
root.mainloop()