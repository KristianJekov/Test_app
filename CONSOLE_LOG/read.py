import serial
import time 
from filter import check_all_components_vers
from update_info import check_if_update_available

def read_all():
    high = False
    low = True

    ser = serial.Serial(baudrate=921600)
    ser.port = "COM17"


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

    line = ser.readline()
    device_ver_dict = {}



    while True:
        line = ser.readline().decode('utf-8').rstrip()
        # print(line)
        if check_if_update_available(line):
            break
        #check_all_components_vers(line,device_ver_dict)

        

    
    