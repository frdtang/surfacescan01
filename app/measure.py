 
import time
import serial
import pyftdi.serialext
from pyftdi.ftdi import Ftdi

 
read_port = serial.Serial(port='/dev/ttyS0',
                          baudrate=38400,
                          bytesize=8,
                          stopbits=1,
                          timeout=1
                          )

write_port = pyftdi.serialext.serial_for_url('ftdi://ftdi:232:FT4IVQEG/1',
                                        baudrate=38400,
                                        bytesize=8,
                                        parity=serial.PARITY_EVEN,
                                        stopbits=1,
                                        timeout=1)

Ftdi.show_devices()


send_string = b":01W010;0;E9C3\r\n"
write_port.write(send_string)

resp = read_port.readline() 
print(resp) 
resp = read_port.readline()  
print(resp)


send_string = b":01R002;3955\r\n"
write_port.write(send_string)
resp = read_port.readline()
print(resp)
resp = read_port.readline()  
print(resp)

send_string = b":01R021;****\r\n"
count=0
while count<100:
    write_port.write(send_string)   
    read_port.readline()  
    resp = read_port.readline()  
    
    distance = float(resp.split(b';')[1])
    quality = float(resp.split(b';')[2])
    print({"v" : distance, "q": quality})
    count+=1

