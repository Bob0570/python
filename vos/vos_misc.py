#vos_misc

import sys
import os
import time
import datetime
from ctypes import create_string_buffer

def vos_taskSleep(ms):
    time.sleep(ms/1000)

def vod_mkBuf(size):
    buffer = create_string_buffer(size)
    #buffer.value = b'abcd' + b'y'*508
    #print(sizeof(buffer), buffer.value, repr(buffer.raw))
    return buffer

def vos_getsizeof(object):
    size = sys.getsizeof(object)
    return size

def vos_getTimeStr():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second

    timeStr = '%04d'%year + '-' + '%02d'%month + '-' + '%02d'%day + ' ' + '%02d'%hour + ':' + '%02d'%minute + ':' + '%02d'%second
    return timeStr

def vos_getTimeMs():
    microSecond = datetime.datetime.now().microsecond
    return microSecond/1000