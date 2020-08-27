 
import time
import serial
 
 
port = serial.Serial(port='/dev/ttyS0',
                          baudrate=57600,
                          bytesize=8,
                          stopbits=1,
                          timeout=1)

   

port.write(b':01R010;0;E9C3r\n')
while True:

    port.write(str.encode(':01R021;09F4r\n'.encode('utf-8')))
    resp = port.readline()  
    if resp:
        print(resp)  


