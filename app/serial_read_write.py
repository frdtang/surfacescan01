 
import time
import serial
 
read_port = serial.Serial(port='/dev/ttyAMA0',
                          baudrate=57600,
                          bytesize=8,
                          parity=serial.PARITY_EVEN,
                          stopbits=1)


read_port.write(b':01R010;0;E9C3r\n')

while True:

    read_port.write(b':01R021;09F4r\n')
    resp = read_port.read()  
    if resp:
        print(resp)  
          