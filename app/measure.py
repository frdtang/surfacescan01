 
import time
import serial
import numpy as np
import pyftdi.serialext


class Disk_Surface():
    
    def __init__(self): 
 
        self._sensor_info = {}
        self._data = [] 
        self._rpm_01 = [] 
        self._rpm_02 = [] 
        self._flatness = [] 
        
        self._read_port = serial.Serial(
            port='/dev/ttyS0',
            baudrate=38400,
            bytesize=8,
            stopbits=1,
            timeout=1)

        self._write_port = pyftdi.serialext.serial_for_url(
            'ftdi://ftdi:232:FT4IVQEG/1',
            baudrate=38400,
            bytesize=8,
            parity=serial.PARITY_EVEN,
            stopbits=1,
            timeout=1)
        
    def measure(self):
        
        self.setup_sensor()
        self.read_sensor()
        #self.shutdown()
        self.analyse()
    
    def setup_sensor(self): 
        ''' Setup and get sensor info'''
        
        # activate RS485 RS485 lock
        self._write_port.write(b":01W010;0;E9C3\r\n")
        self._read_port.read(27) 
        
        # Turn laser on
        self._write_port.write(b":01W034;0;****\r\n")
        self._read_port.readline() 
        self._read_port.readline()  


        # Get sensor info
        self._write_port.write(b":01R002;3955\r\n")
        self._read_port.readline()
        resp = self._read_port.readline()  
        self._sensor_info ={
            'sensor': resp.split(b';')[3].decode("utf-8"),
            'serial_number': int(resp.split(b';')[4])}

        print(self._sensor_info)
        
    def read_sensor(self):
        ''' Measure distance to disk'''
        count=0
        start_time = time.time()
        measurement = {"v" : 0, 
                    "q": 0,
                    "time": 0}

        
        while count<1000:
            self._write_port.write(":01R021;****\r\n")    
            resp = self._read_port.read(35)  
            time_now = round(time.time()-start_time,3)
            distance = float(resp.split(b';')[2])
            quality = float(resp.split(b';')[3])
            
            previous = measurement
            
            dv = round(distance - previous['v'],3)
            dt = round(time_now - previous['time'],3)
            
            measurement = {"v" : distance, 
                        "dv" : dv,                  
                        "q": quality,
                        "time": time_now,
                        "dt": dt}
            
            self._data.append(measurement)
            count+=1
            
    def shutdown(self):
        # Turn laser off
        self._write_port.write( b":01W034;1;****\r\n")
        self._read_port.readall()


    def analyse(self):
        ''' Analyse data  to get flatness and RPM'''

        for point in self._data:
            if point['dv'] > 0.1:
                self._rpm_01.append(point)
            elif point['dv'] < -0.1:
                self._rpm_02.append(point)
            else:
                self._flatness.append(point)

        print('RPM data UP')
        click_UP = np.array([t['time'] for t in self._rpm_01])
        diff_click_UP = np.diff(click_UP)
        mean_click_UP=np.mean(diff_click_UP)
        
        # filtered diff_click_UP
        filter_diff_click_UP = diff_click_UP[diff_click_UP<mean_click_UP]
        rpm_up = 60 / (np.mean(filter_diff_click_UP) * 12)
    
        print(f'Measured UP RPM: {rpm_up}\n')


        print('RPM data DOWN')
        click_DOWN = np.array([t['time'] for t in self._rpm_02])
        diff_click_DOWN = np.diff(click_DOWN)
        mean_click_DOWN = np.mean(diff_click_DOWN)
        
        # filtered diff_click_UP
        filter_diff_click_UP = diff_click_DOWN[diff_click_DOWN<mean_click_DOWN]
        rpm_down = 60 / (np.mean(filter_diff_click_UP) * 12)
        
        print(f'Measured DOWN RPM: {rpm_up}\n')
            
        distances = np.array([t['v'] for t in self._flatness])
        print(f'distance: {np.mean(distances)}\n\
              Std. dev.: {np.std(distances)}\n')


disk_surface = Disk_Surface()
disk_surface.measure()
