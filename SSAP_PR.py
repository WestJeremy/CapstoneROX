# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:49:42 2023

@author: westj
"""

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
import array
import pandas as pd
import requests
import re
from scipy.signal import find_peaks
from scipy.stats import linregress

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
        x=(r*np.cos(theta)+self.x0)       #convert to x cartesian
        y=(r*np.sin(theta)+self.y0)       #convert to y cartesian
        
        return x, y 
    
class Linear: 
    def __init__(self,data,points):
        self.data=data #data
        self.points=points #x offset
        
    def get(self,x): 
        peaks= find_peaks(self.data['Intensity'], height=-900)
    
        H=peaks[1]['peak_heights']
        A=[]
        for i in range(len(IPeaks)):
            corr=[IPeaks[i],H[i]]
            A.append(corr)
        SA=sorted(A, key=lambda x: x[1], reverse=True) #sort by peak height largest to smallest
        print(SA)
        XPP=[]
        YPP=[]
        for i in range(self.points):
            #ICP.append(SA[i][0])
            XPP.append(self.data['X'][SA[i][0]])
            YPP.append(self.data['Y'][SA[i][0]])
        LRR=linregress(XPP,YPP)
        
        return LRR[0]*x+LRR[1]
    

class Intensity: #intensity function is a gaussian curve 
    def __init__(self,x0:float,y0:float, mu_x, mu_y, sigma_x, sigma_y):
        self.x0=-x0 #x offset
        self.y0=-y0 #y offset
        self.mu_x=mu_x
        self.mu_y=mu_y
        self.sigma_x=sigma_x #x squish/stretch
        self.sigma_y=sigma_y #y sqush/stretch
        
        
    def get(self,x, y): #gaussian curve definition
        I=np.exp(-0.5 * (((x +self.x0- self.mu_x) / self.sigma_x)**2 + ((y+self.y0 - self.mu_y) / self.sigma_y)**2))
        return I

class Photoresistor:
    def __init__(self,url) -> None:
        self.url=url
    def get(self):
        response = requests.get(self.url)
        if response.ok:
            value = response.text
            pr=re.findall(r'\d+',value)
            pri=-int(pr[0])
            #print('Received value:', value)
            #print('Number', PR)
        else:
            print('Error:', response.status_code)  
          

        return pri

        
#*****************************************************************************************************************
#___Initialization______________
xl=0
yl=0
Loops=3
robot = RDK.Item('Mecademic Meca500 R3')
home = RDK.Item('Home 1')
target = RDK.Item('Target 2')# retrieve the Target item
PR=Photoresistor( 'http://192.168.0.24')

robot.MoveJ(home) 
robot.MoveJ(target)  



for L in range(1,Loops+1):
    print(L)
    if __name__=="__main__":
        print('Calling spiral from class')

        cur_spiral=Spiral(xl,yl,200) #setting params of the spiral we will be using
        x,y=cur_spiral.build(30/L**L,5/L) #build our spiral x y coords
        Ix=1.24
        Iy=-2.3
        TestInt=Intensity(Ix,Iy,0,0,10,10) #set test intensity parameters     
    
        #Plot our spiral
        # plt.plot(x, y, color = 'red', marker = "o") 
        # plt.axis('equal')
        # plt.show()
    
    #initialize params
    X=[]
    Y=[]
    Z=[]
    Iv=[]
    Cv=[]
    
    for i in range(len(x)): #loop to get coord and corresponding intensity
        coord=(x[i],y[i],0)
        X.append(x[i])
        Y.append(y[i])
        Z.append(0)
        Ic=PR.get()
  
        Iv.append(np.array(Ic))

        robot.MoveJ(target.Pose()*transl(coord))
        robot.WaitFinished()
        #pandas dictionary
        titled_columns={'X': X,'Y': Y,'Z': Z,
                        'Intensity': Iv}
        data = pd.DataFrame(titled_columns)


    peaks= find_peaks(data['Intensity'], height=-900)
    print('peaks',peaks)


    IPeaks=peaks[0]
    H=peaks[1]['peak_heights']
    A=[]
    for i in range(len(IPeaks)):
        corr=[IPeaks[i],H[i]]
 
        A.append(corr)
  
 
    
    SA=sorted(A, key=lambda x: x[1], reverse=True) #sort by peak height largest to smallest
    if len(SA) == 1:
        print('one peak detected')
        break
    else:

     CL=Linear(data,2) #current linear line definition

    step=.1/L #linear step size
    xl=data['X'][SA[0][0]] #start x
    yl=CL.get(xl) #start y

    Xl=[xl]  
    Yl=[yl]
    PRS=SA[0][1]
    Il=[PRS]

    if  data['X'][SA[0][0]] < data['X'][SA[1][0]]: 
        step=step
    else:
        step=-step
    
    
    while PR.get() >= .99*PRS:
        
        xl=xl+step
        yl=CL.get(xl)
        PRS=PR.get()
        Xl.append(xl)
        Yl.append(yl)
        Il.append(PRS)
        coord=(xl,yl,0)
        robot.MoveJ(target.Pose()*transl(coord))



    LLdata={'X':Xl,'Y':Yl,'I':Il}
    Ldata=pd.DataFrame(LLdata)
    
    fig = plt.figure()
    plt.style.use('seaborn-notebook')
    ax = fig.add_subplot(111, projection='3d')
    ax.plot3D(data['X'], data['Y'], data['Intensity'])
    ax.plot3D(data['X'][IPeaks], data['Y'][IPeaks], data['Intensity'][IPeaks],"x")
    ax.plot3D(Xl, Yl, Il,'o')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
plt.show()    
 



E=np.sqrt((Ix-xl)**2+(Iy-yl)**2)
print('***Linear Translation********************************************************')
print(Ldata)
print('_________SSAP Report:_________')
print('Calculated peak is at',xl,yl)
print('True peak is at',Ix,Iy)
print('Error is:',E)
print('Linear step size is:',step)
