# -*- coding: utf-8 -*-
import sys

def triangle(a):
    c = [i for i in range(0, a+1)]
    j = 0
    for i in range((a//10)*2):
        if i % 2 !=0:
            j +=i
            print(' '.join(list(map(lambda x : str(x), c[j-i+1:j+1]))).center(150))     
            if c[j-i+1:j+1] == []: 
                break


if __name__ == "__main__":            
    arg1 = sys.argv[1]
    triangle(int(arg1))

triangle(230)

     