import serial
import time 

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


while True:
    line = ser.readline().decode('utf-8').rstrip()
    print(line)