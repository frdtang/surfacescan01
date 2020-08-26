 
import time
import serial
 
ser = serial.Serial(port='/dev/ttyS0',
                    baudrate=38400,
                    bytesize=8,
                    stopbits=1,
                    timeout=1)

while True:
    resp = ser.readline()  
    if resp:
        print(resp)  
    
    ser.write(b'Hello Laptop\n')
    time.sleep(1)
          

