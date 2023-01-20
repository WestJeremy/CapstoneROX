# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:43:18 2023

@author: westj
"""

class Spiral:
    def __init__(self,x0:float,y0:float) -> None:
        self.x0=x0 #x offset
        self.y0=y0 #y offset
        
    def build(self, radius:float, pitch:float):
        return self.x0 * self.y0  * radius * pitch
    
if __name__=="__main__":
    print('Calling spiral from class')
    
    cur_spiral=Spiral(3,4)
    
    
    print(cur_spiral.build(1,2))
