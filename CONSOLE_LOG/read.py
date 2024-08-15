import serial

import time
from filter import check_all_components_vers
from update_info import check_if_update_available
import queue as q

def read_all(strg, qq: q.Queue):
    high = False
    low = True
 
    ser = serial.Serial(baudrate=921600)

    ser.port = strg
 
 
    ser.dtr = low

    line = ser.readline()
    device_ver_dict = {}
 

    while True:
        line = ser.readline().decode('utf-8').rstrip()
        qq.put(item=line, block=False)

       # print(str(line))
       # if check_if_update_available(line):
        #     break
         # TODO fix the bug for the secont main loop and etc
         #check_all_components_vers(line,device_ver_dict)
 
