 
import time
import serial
import numpy as np
import pyftdi.serialext


class Disk_Surface():
    
    def __init__(self): 
 
        self._sensor_info = {}
        self._data = [] 
        self._rpm_01 = np.array([]) 
        self._rpm_02 =  np.array([]) 
        self._flatness =  np.array([]) 
        
        self._read_port = serial.Serial(
            port='/dev/ttyS0',
            baudrate=115200,
            bytesize=8,
            stopbits=1,
            timeout=1)

        self._write_port = pyftdi.serialext.serial_for_url(
            'ftdi://ftdi:232:FT4IVQEG/1',
            baudrate=115200,
            bytesize=8,
            parity=serial.PARITY_EVEN,
            stopbits=1,
            timeout=1)
    
    @property
    def data(self):
        return self._data
        
    def measure(self):
        
        self.setup_sensor()
        self.read_sensor()
        self.shutdown()
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
        # self._write_port.write( b":01W034;1;****\r\n")
        # self._read_port.readall()
        
        # activate RS485 RS485 lock
        self._write_port.write(b":01W010;1;****\r\n")
        self._read_port.readline() 


    def analyse(self):
        ''' Analyse data  to get flatness and RPM'''

        for point in self._data:
            if point['dv'] > 0.1:
                self._rpm_01 = np.append(self._rpm_01, point)
            elif point['dv'] < -0.1:
                self._rpm_02 = np.append(self._rpm_02, point)
            else:
                self._flatness = np.append(self._flatness, point)
                
        rpm_up = 0
        if self._rpm_01.size >1:
            click_UP = [t['time'] for t in self._rpm_01]
            diff_click_UP = np.diff(click_UP)
                        
            # filtered diff_click_UP to ensure sufficiently apart
            diff_click_UP = diff_click_UP[diff_click_UP> 0.01]
            rpm_up = 60 / (np.mean(diff_click_UP) * 12)
      
        print(f'Measured UP RPM: {round(rpm_up,2)}\n')

        rpm_down = 0
        if self._rpm_02.size >0 :
            click_DOWN = [t['time'] for t in self._rpm_02]
            diff_click_DOWN = np.diff(click_DOWN)
            
            # filtered diff_click_UP to ensure sufficiently apart
            diff_click_DOWN = diff_click_DOWN[diff_click_DOWN > 0.01]
            mean_click_DOWN = np.mean(diff_click_DOWN)
            

            rpm_down = 60 / (np.mean(diff_click_DOWN) * 12)
        
        print(f'Measured DOWN RPM: {round(rpm_down,2)}\n')
            
        distances = np.array([t['v'] for t in self._flatness])
        mean_distance = round(np.mean(distances), 3)
        std_dev_distance = round(np.std(distances), 3)
        print(f'distance: {np.mean(distances)}\nStd. dev.: {np.std(distances)}\n')


disk_surface = Disk_Surface()
disk_surface.measure()
