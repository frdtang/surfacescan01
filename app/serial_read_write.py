 
import time
import serial
 
 
import time
import serial
 
port = serial.Serial(port='/dev/ttyS0',
                          baudrate=38400,
                          bytesize=8,
                          stopbits=1,
                          timeout=1)

send_port = serial.Serial(port='/dev/ttyAMA0',
                          baudrate=38400,
                          bytesize=8,
                          stopbits=1,
                          timeout=1)
    

port.write(b':01R010;0;E9C3r\n')
while True:

    port.write(b':01R021;09F4r\n')
    resp = port.readline()  
    if resp:
        print(resp)  


