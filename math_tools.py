# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:09:26 2018

@author: zouco
"""

import math
import numpy as np

def cut_range(a, b, bins):
    l = range(a, b)
    le = math.ceil((b-a)/bins)
    result = []
    for i in range(bins):
        result.append(l[i*le:(i+1)*le])
    return result

def cut_list(the_list, bins):
    if len(the_list) < bins:
        return [None for _ in range(bins)]  # it is important to have None here (for proxies management)
    
    num_last = len(the_list)%bins
    if num_last !=0:
        the_last = the_list[-num_last:]
        the_list = the_list[:-num_last]
    index = np.arange(len(the_list))  
    #return [piece for piece in np.hsplit(index,bins)]
    result = [the_list[piece[0]:piece[-1]+1] for piece in np.hsplit(index,bins)]
    if num_last !=0:
        for i in range(len(the_last)):
            result[i].extend([the_last[i]])
    return result

    

l=[1,2,3,4,5,6,7,8,9,10] 

a = np.array(l)
np.hsplit(a, 2)
[l[list(i)[0]:list(i)[-1]] for i in cut_range(0, len(l), 3)]