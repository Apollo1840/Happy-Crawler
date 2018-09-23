# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:09:26 2018

@author: zouco
"""

import math
def cut_range(a, b, bins):
    l = range(a, b)
    le = math.ceil((b-a)/bins)
    result = []
    for i in range(bins):
        result.append(l[i*le:(i+1)*le])
    return result