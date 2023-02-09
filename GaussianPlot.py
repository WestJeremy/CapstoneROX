# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 21:26:54 2023

@author: westj
"""
#from ChatGPT
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def gaussian(x, y, mu_x, mu_y, sigma_x, sigma_y):
    return np.exp(-0.5 * (((x - mu_x) / sigma_x)**2 + ((y - mu_y) / sigma_y)**2))

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)

X, Y = np.meshgrid(x, y)
Z = gaussian(X, Y, 0, 0, 2, 1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

plt.show()
