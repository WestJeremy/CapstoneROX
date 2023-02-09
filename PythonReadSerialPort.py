# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 21:27:50 2023

@author: westj
"""
import serial

try:
    arduino=serial.Serial('COM3',timeout=1)
except:
        print('Please check the port')
        
rawdata=[]
count=0
while count <3:
    rawdata.append(str(arduino.readline()))
    count+=1
print(rawdata)