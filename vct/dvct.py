#vct using for dos command

import sys
import time
import struct

sys.path.append("../")
from vos import vos_sock as vsock
from vos.vos_misc import *

VCT_NORMAL_CMD = 0xbeaf1000
VCT_SCP_CMD = 0xbeaf1004
VCT_SCP_ACK_CMD = 0xbeaf1005
RPC_key = ['msg_types', 'ulSN', 'ulCmd',        'ulPar',    'ulResult', 'symblName',    'sInfo']
RPC_val = [0,           0,      VCT_NORMAL_CMD, [0]*8,      0,          ''*64,         ''*512]
cSock = 0
g_scpAckIndex = 0

def dvcShowHelp():
    helpInfo = [
        "help                          show help info2",
        "connect x.x.x.x               connect ip address",
        "symbol                        run func/show varies",
        "call Addr                     run func of Addr",
        "symbol.                       lkup symbol",
        "symbol:                       lkup whole-matched symbol",
        "d   Addr [units] [width]      show memory",
        "m   Addr val [width]          modify meory",
        "--------------------------------------------------------------------"]
    
    for info in helpInfo:
        print(info)
    return

def dvctSockRecv(data):
    print(data.decode())
    return

    size = vos_getsizeof(data)
    if(size == 624):
        rlist = RPC_val
        rlist[0], rlist[1], rlist[2], *rlist[3], rlist[4], rlist[5], rlist[6] = struct.unpack('3I8II64s512s', data)
        print(rlist[:3], rlist[3], rlist[4], rlist[5].decode(), rlist[6].decode())
        if(rlist[2] == VCT_SCP_ACK_CMD):
            g_scpAckIndex = rlist[3][1]
    else:
        print(data.decode())   

print("Welcome to VCT-PY!\r\n->")
clt_sock = vsock.Sock_clt()
while True:
    inputCmd = input('->')
    inList = inputCmd.split(' ')
    
    if(inList[0] == 'connect'):
        clt_sock.vos_sockConnect(28901, inList[1], dvctSockRecv)
        print('->')
        continue
    if(inList[0] == 'help'):
        dvcShowHelp()
        print('->')
        continue
    if(inputCmd == 'exit'):
        if(clt_sock.status != 0):
            strSend = 'bye'
            clt_sock.vos_sockSendall(strSend.encode())
            vos_taskSleep(200)
            clt_sock.vos_sockClose()
        break
    if(clt_sock.status == 0):   
        print("disconnect. connect to the right ip addr pls\r\n->")
        continue    
    elif(inputCmd == ''):
        print('->')
    else:
        ''''RPC_send = dict(zip(RPC_key, RPC_val))
        RPC_send['symblName'] = ' '
        RPC_send['sInfo'] = inputCmd
        RPC_val2 = list(RPC_send.values())'''
        RPC_val2 = RPC_val
        RPC_val2[5] = ' '
        RPC_val2[6] = inputCmd
        data = struct.pack('3I8II64s512s', *RPC_val2[:3], *RPC_val2[3], RPC_val2[4], RPC_val2[5].encode(), RPC_val2[6].encode())
        clt_sock.vos_sockSendall(data)        
