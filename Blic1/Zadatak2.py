# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:56:16 2022

@author: David
"""

def fun(d1,d2):
    assert(isinstance(d1, dict) and isinstance(d2, dict))
    return ([x for x,y in zip(d1.values(),d2.values())])
    
val1 = {"valute":["GBP","USD","CZK"],"cijena":[8.5,7.7,0.3]}
val2={"valute":["EUR","USD","CZK"],"cijena":[7.5,7.7,0.3]}

print(fun(val1,val2))