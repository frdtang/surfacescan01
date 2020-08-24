 

import serial
 
ser = serial.Serial(port='/dev/ttyAMA0', baudrate=38400,timeout=1)

while True:
    str = ser.readall()  
    if str:  
        print(str )