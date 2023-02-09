# -*- coding: utf-8 -*-
"""
Python code to receive data from an arduino

The arduino is connected to the PC via USB.

The arduino code streams voltage and time stamp data.
It does so by writing a line of text each time increment

The Python code receives this data.  A thread is used to read and 
convert the from text to integer values, and to save the data in 
a queue.

Client code can then get the data from the queue.


"""  
import serial
import threading
import logging as log
from time import sleep, time


def Now():
    return time() - log._startTime
        

class arduinoReadThread:
    """
   Separate thread to continuously read frames from the arduino, and store in a list
    """
    def __init__(self, arduino):
        self.arduino = arduino
        self.active = True
        self.data = []      # Queue for voltage and timestamp data
        self.count = 0      # Number of lines read since start
        self.maxCount = 30  # When the queue has too many entries discard the 10 oldest entries
        self.avail = 0      # The number of entries available

        self.mutex = threading.Lock()

        self.thread = threading.Thread(target=self.readLoop, name='Arduino read thread', args=(self.arduino, self.mutex))

        print(f"{Now():.3f} Starting read thread")
        self.thread.start()


    def readLoop(self, arduino, mutex):
        '''
        Continuously read lines of data from the arduino serial interface
        '''
        while self.active:
            with mutex:
                l = arduino.readline()

                try:
                    v, t = l.decode('utf-8').split()
                    self.data.append((int(v), int(t)))
                    self.count += 1
                    #print(f"{Now():.3f} read loop: V {v} T {t}  Count {self.count}  Avail {self.avail}")
                except:
                    pass
                
                if len(self.data) > self.maxCount:
                    # Discard oldest 10 entries
                    self.data = self.data[10:]
                    
                self.avail = len(self.data)
                    
            sleep(0.01)  # Give other threads a chance to run
            
        log.info("Arduino Read Thread Exiting")


        
    def getData(self, count=1):
        '''
        Return oldest unread count of (v,t) tuples
        '''

        timeOut = Now() + 5  # Abort if Arduino isn't generating data
        
        # Spin-lock waits until the requested number of entries are available:
        while self.avail < count:
            if Now() > timeOut:
                log.warning('Timeout waiting for arduino data')
                raise Exception('Timeout waiting for data from arduino')
            #print(f"{Now():.3f} getData:  Count {self.count}  Avail {self.avail}")
            sleep(0)

        # After sufficient data is available, remove it from the queue and return it
        with self.mutex:
            d = list(self.data[:count])    # Copy the first count entries into a separate list
            self.data = self.data[count:]  # And remove them from the queue
            self.avail = len(self.data)    # Update the number of available entries

        return d    # Return the data
        
    def flush(self):
        # Discard all old data

        print(f"{Now():.3f}  Flushing {self.avail} entries ")
        with self.mutex:
            self.data = []      # Empty the data list
            self.avail = 0      # And set the number of available entries to zero

class photoResistor:
    
    
    def __init__(self, port='COM4', baudrate=57600):
        
        self.arduino = serial.Serial(port=port, baudrate=baudrate)
        
        self.reader = arduinoReadThread(self.arduino)
        

pr = photoResistor()

pr.reader.flush()



DATA=[]

class Logic:
    def __init__(self,intensity):
        self.intensity=intensity
        
    def LR(self,d):
        if d >300:
            return('right')
        if d <300:
            return('left')
        
datastore=[[0],[0]]

for i in range(200):
    data = pr.reader.getData(1)
    datastore.append(data)
    #print(f"{data}")
    #print(f"{Now():.3f} {data}")
    #print(datastore[-1][0][0])
    
    #print(datastore[-2][0][0])
    
    if i>0 and datastore[-1][0][0]<datastore[-2][0][0]:
        print('Brighter')
        print(datastore[-2][0][0])
        print(datastore[-1][0][0])
        
    elif i>0 and datastore[-1][0][0]>datastore[-2][0][0]:
        print('Dimmer')

pr.reader.active = False