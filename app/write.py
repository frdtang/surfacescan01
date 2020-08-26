 
import time
import serial
 
ser = serial.Serial(port='/dev/ttyAMA0',
                    baudrate=38400,
                    bytesize=8,
                    stopbits=1,
                    timeout=1)

send_str = "*******rs485888888--\r\n"

while True:
    ser.write(str.encode(send_str))