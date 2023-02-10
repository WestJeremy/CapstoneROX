# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:43:18 2023

@author: westj
"""
# from robodk.robolink import *       # import the robolink library (bridge with RoboDK)
# RDK = Robolink()   
# from robodk.robomath import *   
import math
import numpy as np
import matplotlib.pyplot as plt 
import array
import pandas as pd
from scipy.signal import find_peaks

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
    

class Intensity: #intensity function is a gaussian curve 
    def __init__(self,x0:float,y0:float, mu_x, mu_y, sigma_x, sigma_y):
        self.x0=x0 #x offset
        self.y0=y0 #y offset
        self.mu_x=mu_x
        self.mu_y=mu_y
        self.sigma_x=sigma_x #x squish/stretch
        self.sigma_y=sigma_y #y sqush/stretch
        
        
    def get(self,x, y): #gaussian curve definition
        I=np.exp(-0.5 * (((x +self.x0- self.mu_x) / self.sigma_x)**2 + ((y+self.y0 - self.mu_y) / self.sigma_y)**2))
        return I

        

if __name__=="__main__":
    print('Calling spiral from class')

    cur_spiral=Spiral(0,0,100) #setting params of the spiral we will be using
    x,y=cur_spiral.build(3,.75) #build our spiral x y coords
    
    
    TestInt=Intensity(.1,.2,0,0,2,1) #set test intensity parameters     
    
    #Plot our spiral
    plt.plot(x, y, color = 'red', marker = "o") 
    plt.axis('equal')
    plt.show()
    
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
    Ic=TestInt.get(x[i],y[i])
    Iv.append(np.array(Ic))
    
#pandas dictionary
titled_columns={'X': X,'Y': Y,'Z': Z,
                'Intensity': Iv}
data = pd.DataFrame(titled_columns)

# dI=np.diff(data['Intensity'])
# dI=np.insert(dI,0,-1)
# data['dI']=dI

# dp=np.array(np.sqrt(np.diff(data['X'])**2+(np.diff(data['Y'])**2))) #change in position from previous point
# dp=np.insert(dp,0,1) #placeholder to make sizes match
# data['dp']=dp

# data['dI/dp']=data['dI']/data['dp']

#Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
peaks = find_peaks(data['Intensity'], height=.1)
height=peaks[1]
peakpos=peaks[0]

ax.plot3D(data['X'], data['Y'], data['Intensity'])
ax.plot3D(data['X'][peaks], data['Y'][peaks], data['Intensity'][peaks],"x")

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()


# Ipks=data['Intensity'][peaks]

# ii=np.sort(Ipks)



#IpksS=Ipks[:,2].sort(reverse=True)
m=max(data['Intensity'])
print(np.where(data['Intensity'] == m)[0])
#rint(ii)



print(data)
print(data['Intensity'][3])

