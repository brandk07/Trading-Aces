from Classes.imports.Latterscroll import LatterScroll
# import pygame

# pygame.mixer.init()
# pygame.mixer.music.load("Assets\Sounds\Timo Versemann - Shalom Chaverim.mp3")
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)
#     print('playing')
# Suppose we have the following dictionary

mydict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
print(mydict.setdefault('b', 5))
print(mydict)
def getAvgReturn(percent,days):
    neg = 1 if percent > 0 else -1
    percent = abs(percent)
    days = 1/(days/365)
    return ((1+(percent/100)) ** days )* neg

# avgreturn =  lambda percent,days : ((1+(abs(percent)/100)) ** (1/(days/365)))*100

print(str(getAvgReturn(-75,1095))+"%")
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

