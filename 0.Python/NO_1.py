# -*- coding: utf-8 -*-

import re
import sys

class strCalculator:
    chOp = dict(zip(['*','/','+','-','(',')'], [5,5,3,3,1,1]))     
    
    def __init__(self, fx):
        try:
            _ , self.fx = fx.split('=')
        except ValueError as e:
            print(e)
    def change_L(self):
        reC = re.compile(r'(?:(?<=[^\d\.])(?=\d)|(?=[^\d\.]))', re.MULTILINE)
        return [x for x in re.sub(reC, ' ', self.fx).split(' ') if x]
    
    @staticmethod
    def calRL(L, R, op):
        if op == '*':
            return(float(L) * float(R))
        if op == '/':
            return(float(L) / float(R))
        if op == '+':
            return(float(L) + float(R))
        if op == '-':
            return(float(L) - float(R))
 

class CheckN(Exception):
    def __init__(self):
        super().__init__("입력 값 오류 | ex): arg1 -> y=20+((10*x)/(100-x)) arg2 -> 3")

       

def postFix(Str,chOp,x):
    
    tBox = []
    ioBox = []    
    for ar in Str:
        if ar.lower() == 'x':
            ar = int(x)
        if ar not in chOp:
            tBox.append(ar)
            
        elif ar == '(':
            ioBox.append(ar)
        
        elif ar == ')':    
            while ioBox !=[] and ioBox[-1] != '(':
                tBox.append(ioBox.pop())
            ioBox.pop()
        else:
            while ioBox !=[] and chOp[ioBox[-1]] > chOp[ar]:
                tBox.append(ioBox.pop())
            ioBox.append(ar)
    
    while ioBox:
        tBox.append(ioBox.pop())            

    return(tBox)


def workProcess(fx,x):
    
    Cwork = strCalculator(fx)
    Str = Cwork.change_L()
    chOp = Cwork.chOp
    tBox = postFix(Str,chOp,x)
    
    calBox = []    
    for i in tBox:
        if i not in chOp:
            calBox.append(i)
        
        if i in chOp:
            op = i
            R = calBox.pop()
            L = calBox.pop()
            calBox.append(Cwork.calRL(L,R,op))
    
    return(calBox[0])




if __name__ == "__main__":
    
    if len(sys.argv) > 3:
        arg1 = ' '.join(sys.argv[1:-1])
        arg2 = sys.argv[-1]
    elif len(sys.argv) <3:    
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
    else:
        raise CheckN()
    result = workProcess(arg1 ,arg2)
    print(' 입력 값 x : ', arg2, '\n','결과 값 y : ', result)




