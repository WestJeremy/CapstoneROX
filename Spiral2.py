# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:43:18 2023

@author: westj
"""
from robodk.robolink import *       # import the robolink library (bridge with RoboDK)
RDK = Robolink()   
from robodk.robomath import *   
import math
import numpy as np
import matplotlib.pyplot as plt 

class Spiral:
    def __init__(self,x0:float,y0:float,points:float) -> None:
        self.x0=x0 #x offset
        self.y0=y0 #y offset
        self.points=points
        
    def build(self, radius:float, spacing:float):
        revs=radius/spacing            #calc number of revolutions
        k=spacing/(2*np.pi)                       
        theta=np.array(np.linspace(0,revs*2*np.pi,self.points)) #how many points and angle coord
        r=k * theta                       #radius coord
        x=(r*np.cos(theta)+self.x0)
        y=(r*np.sin(theta)+self.y0)             #convert to y cartesian
        
        return x, y #convert to x cartesian
    

class Intensity:
    def __init__(self,x0:float,y0:float):
        self.x0=x0 #x offset
        self.y0=y0 #y offset
    def get(self,x,y):
        
        R = np.array(np.sqrt((x-self.x0)**2 + (y-self.y0)**2));
        Int = np.sin(R)*100;
        return Int

if __name__=="__main__":
    print('Calling spiral from class')

    cur_spiral=Spiral(0,0,10)
    x,y=cur_spiral.build(50,10)
    
    
    X = np.arange(-5, 5, 0.1)
    Y = np.arange(-5, 5, 0.1)
    
    TestInt=Intensity(.1,.2)
    I=TestInt.get(3,4)
    
    I=TestInt.get(X,Y)
    print('The intensity is',I)        
    
    #print(cur_spiral.build(50,10))
    plt.plot(x, y, color = 'red', marker = "o") 
    plt.axis('equal')
    plt.show()


# for i in range(len(x)):
#     coord=(x[i],y[i],0)
#     print(coord)
#     print('')