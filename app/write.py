 
import time
import serial
 
ser = serial.Serial(port='/dev/ttyS0',
                          baudrate=38400,
                          bytesize=8,
                          stopbits=1,
                          timeout=1)


while True:
    ser.write(str.encode('Hello laptop!\n'))
    time.sleep(1)
          
