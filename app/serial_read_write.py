 
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
                                        parity=serial.PARITY_EVEN,
                                        stopbits=1,                            
                                        timeout=1)

Ftdi.show_devices()


send_string = ":01W010;0;01R021;****"
write_port.write(str.encode(send_string))
    
while True:
    send_string = ":01R021;****"
    write_port.write(str.encode(send_string))
    
    time.sleep(1)
    
    resp = read_port.readline()  
    if resp:
        print(resp)  
