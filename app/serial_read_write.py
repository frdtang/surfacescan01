 
import time
import serial
 
port = serial.Serial(port='/dev/ttyS0',
                          baudrate=57600,
                          bytesize=8,
                          stopbits=1,
                          timeout=1
                          )

while True:
    port.write(b'Hello world')
    resp = port.readline()  
    if resp:
        print(resp)  


