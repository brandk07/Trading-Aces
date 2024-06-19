from Classes.imports.Latterscroll import LatterScroll
# import pygame
from Defs import point_in_polygon
mypoly = [(150, 150), (277.94524373378374, 228.29440979982337), (300, 300), (300.0, 150.0000000000001), (150, 150)]
print(point_in_polygon((376, 729),mypoly))

# pygame.mixer.init()
# pygame.mixer.music.load("Assets\Sounds\Timo Versemann - Shalom Chaverim.mp3")
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)
#     print('playing')
# Suppose we have the following dictionary

# mydict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
# print(mydict.setdefault('b', 5))
# print(mydict)
# def getAvgReturn(percent,days):
#     neg = 1 if percent > 0 else -1
#     percent = abs(percent)
#     days = 1/(days/365)
#     return ((1+(percent/100)) ** days )* neg

# # avgreturn =  lambda percent,days : ((1+(abs(percent)/100)) ** (1/(days/365)))*100

# print(str(getAvgReturn(-75,1095))+"%")

# print(round(0.004456,2))

# from optionprice import Option as Op
# myOption = Op(european=True,kind="put",s0=9543.754571035066,k=10024.0,t=208,sigma=0.154,r=0.05)
# print(myOption.getPrice(method="BSM",iteration=1))
print(5%4)
from datetime import datetime, timedelta
from Defs import limit_digits
d1 = datetime.strptime(f"4/19/2035 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p")
d2 = datetime.strptime(f'12/17/2035 12:58:33 PM', "%m/%d/%Y %I:%M:%S %p")
print((d2-d1).total_seconds())

# from decimal import Decimal, getcontext
# import math
# # Set the precision.
# getcontext().prec = 50

# num1 = Decimal('10.123456789123456789123456789123456789123456789123456789')
# num2 = Decimal('20.123456789123456789123456789123456789123456789123456789')

# result = num1 + num2

# print(result)  # Outputs: 30.246913578246913578246913578246913578246913578246913578
# num = Decimal(str(1106.330826943))*Decimal(str(1.52))
# print(num)

# num *= Decimal(str((10**22)))
# print(format(num, '.5e'))
# print(format(num, '.10f'))

# num = (num/Decimal(str(0.041666666666666664)))
# print(format(num, '.5e'))
# print(format(num, ',.10f'))

