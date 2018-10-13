#가위 바위 보 게임을 구경합니다.

#조건=================================================================
#1.컴퓨터와 사람의 경기로 구성되며 랜덤으로 값을 가져 프로그램을 실행 할 때마다 
#  결과는 다를 수 있어야 합니다.
#2.if문, 조건부 삼항연산자를 사용하여 코딩을 생성합니다.

import random

man = random.randint(1,3)
com = random.randint(1,3)

vs = man - com

man = ("가위" if man == 1 else "바위") if man == 1 or man == 2  else "보"  
com = ("가위" if com == 1 else "바위") if com == 1 or com == 2  else "보"


if vs == 1 or vs == -2:
    res = "사람 승"
elif vs == -1 or vs == 2:
    res = "컴퓨터 승"
else:
    res = "비겼다"    

print("Man : ", man)
print("Com : ", com)
print("결과 : " , res)