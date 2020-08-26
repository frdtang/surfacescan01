 
import time
import serial
 
ser = serial.Serial(port='/dev/ttyAMA0',
                    baudrate=38400,
                    bytesize=8,
                    stopbits=1,
                    timeout=1)

while True:
    ser.write('Hello World\n')
    time.sleep(1)
        


