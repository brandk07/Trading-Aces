from Classes.imports.Latterscroll import LatterScroll
# import pygame

# pygame.mixer.init()
# pygame.mixer.music.load("Assets\Sounds\Timo Versemann - Shalom Chaverim.mp3")
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)
#     print('playing')
# Suppose we have the following dictionary

# l = LatterScroll()
# d = []

# for i in range(5):
#     d.append({
#         f'{i}t1': (5,5,35,(255,255,255)),
#         f'{i}t2sdfsdfsdfsdfs': (25,5,35,(255,255,255)),
#         f'{i}t3': ((f'{i}t2sdfsdfsdfsdfs',53),5,35,(255,255,255))
#     })
# print(d)
# for i in range(4):
#     width, texts = l.storeTextsVariable(resetlist=True,**d[0])
#     print(width,'width')
#     print(texts,'texts')
#     for i in range(4):
#         width, texts = l.storeTextsVariable(extraspace=500,**d[i+1])

# print(width,'width')
# print(texts,'texts')

# import timeit

# def sdf(a,b,c=5,*args):
#     print(a,b,c)
#     for arg in args:
        
#         print(arg)
# import numpy as np
# mylist = [3, 4, 5, 6, 7, 8, 9, 10]
# print(mylist[0:])
from decimal import Decimal, getcontext
import math
# Set the precision.
getcontext().prec = 50

# num1 = Decimal('10.123456789123456789123456789123456789123456789123456789')
# num2 = Decimal('20.123456789123456789123456789123456789123456789123456789')

# result = num1 + num2

# print(result)  # Outputs: 30.246913578246913578246913578246913578246913578246913578
num = Decimal(str(1106.330826943))*Decimal(str(1.52))
print(num)

num *= Decimal(str((10**22)))
print(format(num, '.5e'))
print(format(num, '.10f'))

num = (num/Decimal(str(0.041666666666666664)))
print(format(num, '.5e'))
print(format(num, ',.10f'))

# mylist = np.array(mylist,dtype=object)
# print(mylist-1)
# # sdf(22,23,c=24,*mylist)
# for i in range(len(mylist)-1,0,-1):
#     print(mylist[i])

# mylist = [['XKSTO ', 50, (255, 165, 0)], ['48 Shares', 35, (190, 190, 190)], ['$5,732.00', 0, (190, 190, 190)]]

# print([(i[0],i[1],i[2]) for i in mylist])
# multiplier = 7

# print(multiplier % 10 if multiplier < 10 else 10)

# print(3//2)
# start = timeit.default_timer()
# for i in range(1000000):
#     d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
#     items = list(d.items())
#     slice = items[1:3]
#     slice_dict = dict(slice)

# stop = timeit.default_timer()
# print("Time to prerender: ", (stop-start))
# [0, 114, 111, 112, 114, 113] width
# [{(5, 5): <Surface(25x22x32 SW)>, (25, 5): <Surface(29x22x32 SW)>, (53, 5): <Surface(30x22x32 SW)>, (45, 5): <Surface(30x22x32 SW)>, (85, 5): <Surface(29x22x32 SW)>}, {(5, 5): <Surface(22x22x32 SW)>, (25, 5): <Surface(26x22x32 SW)>, (53, 5): <Surface(27x22x32 SW)>, (45, 5): <Surface(27x22x32 SW)>, (85, 5): <Surface(26x22x32 SW)>}, {(5, 5): <Surface(23x22x32 SW)>, (25, 5): <Surface(27x22x32 SW)>, (53, 5): <Surface(28x22x32 SW)>, (45, 5): <Surface(28x22x32 SW)>, (85, 5): <Surface(27x22x32 SW)>}, {(5, 5): <Surface(25x22x32 SW)>, (25, 5): <Surface(29x22x32 SW)>, (53, 5): <Surface(30x22x32 SW)>, (45, 5): <Surface(30x22x32 SW)>, (85, 5): <Surface(29x22x32 SW)>}, {(5, 5): <Surface(24x22x32 SW)>, (25, 5): <Surface(28x22x32 SW)>, (53, 5): <Surface(29x22x32 SW)>, (45, 5): <Surface(29x22x32 SW)>, (85, 5): <Surface(28x22x32 SW)>}] texts
# [114, 111, 112, 114, 113] width
# [{(5, 5): <Surface(25x22x32 SW)>, (25, 5): <Surface(29x22x32 SW)>, (53, 5): <Surface(30x22x32 SW)>, (45, 5): <Surface(30x22x32 SW)>, (85, 5): <Surface(29x22x32 SW)>}, {(5, 5): <Surface(22x22x32 SW)>, (25, 5): <Surface(26x22x32 SW)>, (53, 5): <Surface(27x22x32 SW)>, (45, 5): <Surface(27x22x32 SW)>, (85, 5): <Surface(26x22x32 SW)>}, {(5, 5): <Surface(23x22x32 SW)>, (25, 5): <Surface(27x22x32 SW)>, (53, 5): <Surface(28x22x32 SW)>, (45, 5): <Surface(28x22x32 SW)>, (85, 5): <Surface(27x22x32 SW)>}, {(5, 5): <Surface(25x22x32 SW)>, (25, 5): <Surface(29x22x32 SW)>, (53, 5): <Surface(30x22x32 SW)>, (45, 5): <Surface(30x22x32 SW)>, (85, 5): <Surface(29x22x32 SW)>}, {(5, 5): <Surface(24x22x32 SW)>, (25, 5): <Surface(28x22x32 SW)>, (53, 5): <Surface(29x22x32 SW)>, (45, 5): <Surface(29x22x32 SW)>, (85, 5): <Surface(28x22x32 SW)>}] texts