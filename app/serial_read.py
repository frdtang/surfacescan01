 

import serial
 
ser = serial.Serial(port='/dev/ttyAMA0',baudrate=38400,bytesize=8,stopbits=1,timeout=1)

while True:
    resp = ser.readline()  
    if resp:  
        print(resp)