#!/usr/bin/env python
          
import time
import serial
import os



send_str = "********abcdefghijklmnopqrstuvwxyz&"

          
os.system("echo 18 > /sys/class/gpio/export")
os.system("echo out > /sys/class/gpio/gpio18/direction") 
      
ser = serial.Serial(port='/dev/ttyAMA0',baudrate =38400,bytesize=8,stopbits=1,timeout=1)
    
last_time = time.time()
while 1:
    now_time = time.time()
    if((now_time-last_time)>=1):
        last_time = now_time
#        print "172 sending"
        os.system("echo 1 > /sys/class/gpio/gpio18/value")
        time.sleep(0.01)
        #ser.write(send_str)
        time.sleep(0.01)
        os.system("echo 0 > /sys/class/gpio/gpio18/value")
    os.system("echo 0 > /sys/class/gpio/gpio18/value")
    time.sleep(0.01)
  
    x=ser.readline()
    print(x)

