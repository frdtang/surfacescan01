#!/usr/bin/env python
          
import time
import serial
import os



ser = serial.Serial(port='/dev/ttyAMA0',
                    baudrate=38400,
                    bytesize=8,
                    stopbits=1,
                    timeout=1)
    
last_time = time.time()
while 1:
 
    x=ser.readline()
    print(x)
    time.sleep(0.01)

