# -*- coding: utf-8 -*-

import re
import numpy as np
#import sys

def diff(li):

    sta = int(li.pop())-1
    convert = lambda x : int(x)
    Arr = []    
    
    for i in li:
        Arr.append(list(map(convert,re.findall('\d', i))))
     
    npArr = np.array(Arr) 
    value = Arr[sta]
    dist = np.sqrt((pow(npArr - value,2).sum(axis = 1)))                
    return(npArr[dist.argsort()])


if __name__ == "__main__":

    li = input("좌표입력 : ").split(' ')
    for i in diff(li):
        print(i)









