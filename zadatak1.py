# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:43:50 2022

@author: David
"""
"""lista = [x for x in range(5,50)] #dictionary comprehension
d2 = {k:v for k,v in enumerate(lista)}
print(d2)"""

def fun(l):
    return {k:v[::-1] for k,v in enumerate(l) if all(isinstance(x, str) for x in l)}

l=["stol", "stolica", "krevet", "fotelja"]

print(fun(l))