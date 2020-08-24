#!/usr/bin/env python

import time
import serial
import os


send_str = "*******rs485888888--\r\n"

os.system("echo 18 > /sys/class/gpio/export")
os.system("echo out > /sys/class/gpio/gpio18/direction")
ser = serial.Serial(port='/dev/ttyAMA0',baudrate =10000000,bytesize=8,stopbits=1,timeout=1)


last_time = time.time()

now_time = time.time()
os.system("echo 1 > /sys/class/gpio/gpio18/value")
time.sleep(0.01)
n = 800
while n>0:
    ser.write(send_str)
    n=n-1
#    time.sleep(0.001)
os.system("echo 0 > /sys/class/gpio/gpio18/value")

