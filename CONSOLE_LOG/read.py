import serial
import time 
from filter import *

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
versions_list = []



while check_if_all_ver_equal(versions_list):
    line = ser.readline().decode('utf-8').rstrip()

    check_board_ver(line, versions_list)
    check_sensor_hub_ver(line, versions_list)
    check_batt_ver(line, versions_list)
    check_remote_ver(line, versions_list)

    

    
    