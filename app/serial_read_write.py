 
import time
import serial
 
port = serial.Serial(port='/dev/ttyS0',
                          baudrate=57600,
                          bytesize=8,
                          parity=serial.PARITY_EVEN,
                          stopbits=1)


# port=serial.rs485.RS485(port='/dev/ttyS0',baudrate=57600)
# port.rs485_mode = serial.rs485.RS485Settings(False,True)


port.write(b':01R010;0;E9C3r\n')
while True:

    port.write(b':01R021;09F4r\n')
    resp = port.readline()  
    if resp:
        print(resp)  


