import serial

import time
import queue as q

def read_all(strg, qq: q.Queue):
        
    high = False
    low = True

    ser = serial.Serial(baudrate=921600)
    ser.port = strg

    ser.dtr = low
    ser.rts = high
    ser.dtr = ser.dtr
    ser.open()

    ser.dtr = high
    ser.rts = low
    ser.dtr = ser.dtr

    time.sleep(0.005)

    ser.rts = high
    ser.dtr = ser.dtr 
    ser.dtr = low

    line = ser.readline()

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').rstrip()
        try:
            qq.put(item=line, block=False)
        except q.Full:
            pass

