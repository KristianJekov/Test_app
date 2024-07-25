import serial

ser = serial.Serial('COM17', 921600)

while True:
    line = ser.readline()
    valueinString =str(line, "UTF-8")
    print(valueinString)
