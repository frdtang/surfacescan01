 

import serial
 
ser = serial.Serial(port='/dev/ttyAMA0', 
                    baudrate=38400,
                    timeout=1)

while True:
    resp = ser.readall()  
    if resp:  
        print(resp )