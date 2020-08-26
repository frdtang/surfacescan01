 
import time
import serial
 
read_port = serial.Serial(port='/dev/ttyS0',
                          baudrate=38400,
                          bytesize=8,
                          stopbits=1,
                          timeout=1)

send_port = serial.Serial(port='/dev/ttyAMA0',
                          baudrate=38400,
                          bytesize=8,
                          stopbits=1,
                          timeout=1)

while True:
    resp = read_port.readline()  
    if resp:
        print(resp)  
    
    #send_port.write('Hello Laptop\n')
    time.sleep(1)
          

