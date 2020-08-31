 
import time
import serial
import pyftdi.serialext
from pyftdi.ftdi import Ftdi
 
read_port = serial.Serial(port='/dev/ttyS0',
                          baudrate=57600,
                          bytesize=8,
                          stopbits=1,
                          timeout=1
                          )



write_port = pyftdi.serialext.serial_for_url('ftdi://ftdi:232:FT4IVQEG/1',
                                        baudrate=57600,
                                        bytesize=8,
                                        parity='E',
                                        stopbits=1,                            
                                        timeout=1)

Ftdi.show_devices()

while True:
    send_string = ":01R021;09F4\r\n"
    write_port.write(str.encode(send_string))
    
    time.sleep(1)
    
    resp = read_port.readline()  
    if resp:
        print(resp)  
