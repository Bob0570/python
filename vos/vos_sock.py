#vos_socket

import sys
import struct
import threading
import socket

class Sock_clt:  #for client side
    def __init__(self):
        self.hsock = 0
        self.status = 0

    def vos_sockClientRecv(self, fRecv): #for client side
        while True:
            data = self.hsock.recv(1024)
            if data.decode() == 'bye':
                self.hsock.close()
                return
            fRecv(data)
        return

    def vos_sockConnect(self, port, ipAddr, fRecv): #for client side
        hsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.hsock = hsock
        try:
            hsock.connect((ipAddr, port))
        except Exception as e:
            print('connect fail:',ipAddr)
            hsock.close()
            return
        self.status = 1
        print('connect done:',ipAddr)
        tRecv = threading.Thread(target=self.vos_sockClientRecv, args=(fRecv,))
        tRecv.setDaemon(True)
        tRecv.start()
        return

    def vos_sockClose(self): 
        self.hsock.close()
    def vos_sockSendall(self, data): 
        self.hsock.sendall(data)

######################################################below is for server side
class Sock_ser:
    hsock = 0
    status = 0
    sConnect = 0
    def __init__(self):
        pass

    def vos_sockSerRecv(self, fRecv): #for server side
        while True:
            if(self.status == 0):
                self.hsock.listen(1)
                self.sStatu = 1
                sConnect, addr = self.hsock.accept()
                self.sConnect = sConnect
                print('connect done:', addr)
                self.status = 2
            elif(self.status == 2):
                data = self.sConnect.recv(1024)
                if data.decode() == 'bye':
                    strSend = 'bye-bye'
                    self.sConnect.sendall(strSend.encode())
                if data.decode() == 'bye-bye':
                    self.sConnect.close()
                    #sSock.close()
                    self.status = 0
                fRecv(data)

        return

    def vos_sockCreate(self, port, fRecv): #for server side
        hsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.hsock = hsock
        hsock.bind(('', port))
        tRecv = threading.Thread(target=self.vos_sockSerRecv, args=(fRecv,))
        tRecv.start()
        return hsock

    def vos_sockSendall(self, data): 
        self.sConnect.sendall(data)
        

