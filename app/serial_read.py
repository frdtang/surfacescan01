 

import serial
 
ser = serial.Serial(port='/dev/ttyAMA0', 
                    parity=serial.PARITY_EVEN,
                    baudrate=38400, 
                    stopbits=1,
                    bytesize=8,
                    timeout=1)

while True:
    resp = ser.write(":01R020;****\r\n")
    if resp:  
        print(resp )