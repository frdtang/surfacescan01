 
import time
import serial
import numpy as np
import pyftdi.serialext


class Disk_Surface():
    
    def __init__(self): 
 
        self._sensor_info = {}
        self._data = np.array([]) 
        self._rpm_01 = np.array([]) 
        self._rpm_02 =  np.array([]) 
        self._flatness =  np.array([]) 
        
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
        self._read_port.read(27) 

        # Get sensor info
        self._write_port.write(b":01R002;3955\r\n")
        resp = self._read_port.read(70)  
        self._sensor_info ={
            'sensor': resp.split(b';')[4].decode("utf-8"),
            'serial_number': int(resp.split(b';')[5])}
        
    def read_sensor(self):
        ''' Measure distance to disk'''
        count=0
        start_time = time.time()
        measurement = {"v" : 0, 
                       "q": 0,
                       "time": 0}
        
        while count<100:
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
            
            self._data = np.append(self._data, measurement)
            print(self._data)
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
        
        # Clean up data
        q = np.array([t['q'] for t in self._data])
        good_condition = q == 0        
        self._data =  self._data[good_condition]
        self._data = np.delete(self._data, 0)

        dv = np.array([t['dv'] for t in self._data])
        rpm_condition_01 = dv > 0.1 
        self._rpm =  self._data[rpm_condition_01]

        rpm_condition_02 = dv < 0.1 
        rpm_condition =  np.logical_and(rpm_condition_01,
                                        rpm_condition_02)
        flatness_condition = np.logical_not(rpm_condition)
        self._flatness =  self._data[flatness_condition]
                
        rpm_up = 0
        if self._rpm.size > 1:
            click_UP = [t['time'] for t in self._rpm]
            diff_click_UP = np.diff(click_UP)
            # filtered diff_click_UP to ensure sufficiently apart
            diff_click_UP = diff_click_UP[diff_click_UP > 0.05]
            
            #first second average
            min_dt = np.min(diff_click_UP)
            rpm_up = 60 / (min_dt * 12)
      
        print(f'Measured RPM: {round(rpm_up,2)}\n')

            
        distances = np.array([t['v'] for t in self._flatness])
        mean_distance = round(np.mean(distances), 3)
        std_dev_distance = round(np.std(distances), 3)
        print(f'distance: {mean_distance}\nStd. dev.: {std_dev_distance}\n')


disk_surface = Disk_Surface()
disk_surface.measure()
