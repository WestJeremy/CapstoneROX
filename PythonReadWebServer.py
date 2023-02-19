# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 00:01:40 2023

@author: westj
"""

import requests
import re

url = 'http://192.168.0.24'
PRA=[]
while True:
    response = requests.get(url)
    if response.ok:
        value = response.text
        PR=re.findall(r'\d+',value)
        #print('Received value:', value)
        print(PR)
        PRA=PRA.append(PR)
    else:
        print('Error:', response.status_code)




        