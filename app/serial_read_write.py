 
import time
import serial
 
read_port = serial.Serial(port='/dev/ttyS0',
                          baudrate=38400,
                          bytesize=8,
                          stopbits=1,
                          parity= serial.PARITY_EVEN,
                          timeout=1)


while True:

    read_port.write(b':01R020;****\r\n')
    resp = read_port.readline()  
    if resp:
        print(resp)  
    time.sleep(1)
          