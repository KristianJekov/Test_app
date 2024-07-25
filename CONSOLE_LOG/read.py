import serial

serial = serial.Serial(port ='/dev/ttyUSB0', baudrate= 9600)

while True:
    value = serial.readline()
    valueInString = str(value, 'UTF-8')
    print(valueInString)