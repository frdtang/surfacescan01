 
import time
import serial
 
ser = serial.Serial(port='/dev/ttyS0',
                    baudrate=38400,
                    bytesize=8,
                    stopbits=1,
                    timeout=1)

send_str = b'Hello laptop!\n'

while True:
    ser.write(str.encode('Hello laptop!\n'))