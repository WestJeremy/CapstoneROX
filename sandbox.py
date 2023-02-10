# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 12:37:50 2023

@author: westj
"""

x = [1,1,1,2,1,1]
b = -1

try:
    y = x[:x.index(b)]
except ValueError:
    y = x[:]
    
print(y)
print(x)
#%%
student_tuples = [
    ('john', 'A', 15),
    ('jane', 'B', 12),
    ('dave', 'B', 10),
]
print(sorted(student_tuples, key=lambda student: student[2]))   # sort by age
