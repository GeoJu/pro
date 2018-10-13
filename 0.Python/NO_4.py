# -*- coding: utf-8 -*-

import re
import operator

class Nsort:
    def __init__(self, li, sep):
        self.li = li.split(sep)
        self.li = {i.strip().lower():len(i.strip()) for i in self.li} 
        self.li = sorted(self.li.items(), key = operator.itemgetter(1))
        self.mBox = list()
        self.eqBox = list()

    def eqSort(self):
        list(map(lambda x : self.mBox.append(x), sorted(self.eqBox)))
        self.eqBox = list()
    
    def con(self):
        for i in range(len(self.li)):
            
            if i != len(self.li)-1: 
                  
                if self.li[i][1] != self.li[i-1][1] and self.li[i][1] != self.li[i+1][1]:
                    self.mBox.append(self.li[i])
                
                if self.li[i][1] == self.li[i-1][1] or self.li[i][1] == self.li[i+1][1]:
                    self.eqBox.append(self.li[i])
                
                    if self.li[i][1] != self.li[i+1][1]:    
                        self.eqSort()
        
        if self.eqBox != []:
            self.eqBox.append(self.li.pop())                                
            self.eqSort()
        else: 
            self.mBox.append(self.li.pop())              
        
        for sText in self.mBox:
             print(sText[0])   


if __name__ == "__main__":
    reTxt = open('/home/nara/test.txt','r').read()
    sep = re.search("['\n'\' '\',']", reTxt).group()
    lsSort = Nsort(reTxt, sep)
    lsSort.con()


