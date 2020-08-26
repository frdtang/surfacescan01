 

import serial
 
ser = serial.Serial(port='/dev/tty0', 
                    baudrate=38400,
                    timeout=1)

while True:
    resp = ser.readall()  
    if resp:  
        print(resp )