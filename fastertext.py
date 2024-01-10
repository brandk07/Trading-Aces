import pygame
import timeit
from pygame import freetype
import pygame.gfxdraw
from functools import lru_cache 
from random import randint
import re
pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")

fonts = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Regular.ttf', font_size)
fontlist = [fonts(num) for num in range(0,201)]#list of fonts from 0-100

# below is a dictionary of all the rendered numbers
# the key is the size of the font, the value is a list containing a dictionary (explained below) and the renders
# the dictionary contains the length of the number as the key, and the surface that the number is blited to as the value
renderednums = {}# size : [{len(text) : surface}, renders nums 0-9]

# 53 and 25 pre num renderer
# 
# take text as extra argument, but the text won't be in prerenders
@lru_cache(maxsize=100)
def split_string(s):
    # Split the string into parts that are either all digits or all non-digits
    parts = re.split('(\d)', s)

    # Remove any empty strings from the list
    parts = [part for part in parts if part]

    # Convert the numeric parts to integers
    for i in range(len(parts)):
        if parts[i].isdigit():
            parts[i] = str(parts[i])

    return parts
start = timeit.default_timer()
for i in range(100000):
    t = split_string(f"Price: ${16521321:,.2f} dollars")
stop = timeit.default_timer()
print("Time to prerender: ", (stop-start))

# print(split_string(f"Price: ${16521321:,.2f} dollars"))
@lru_cache(maxsize=100)
def string_renderer(string:str, size, color):
    print(f"Caching arguments: {string}, {size}, {color}")
    text = fontlist[size].render(string, color)[0]
    return text

@lru_cache(maxsize=1000)
def num_renderer(string:str, size, color) -> pygame.Surface:
    """Renders text to a surface, and returns the surface"""
    global renderednums
    string = f"Price ${string:,.2f}"
    text = split_string(string)
    # text = f'Price {string:,.2f}'

    # width,height = ((len(string)*size)//(2.1)),(size)*1.1
    width,height = ((len(string)*size)//(2.5)),(size)*1.1
    if size not in renderednums:
        renderednums[size] = [fontlist[size].render(str(i), color)[0] for i in range(0,10)]
        renderednums[size].append(fontlist[size].render('.', color)[0])
        renderednums[size].append(fontlist[size].render(',', color)[0])

    surf = pygame.Surface((width,height))
    surf.set_colorkey((0,0,0))

    blit_sequence = []
    lastwidth = 0
    for i in range(0,len(text)):
        if not text[i].isdigit() and not(text[i] == '.' or text[i] == ','):# if the character(s) is(are) a string
            render = string_renderer(text[i], size, color)
            blit_sequence.append((render, (0 if i == 0 else lastwidth,0)))
            lastwidth += render.get_width()+(size/13)
        else:
            if text[i] == '.' or text[i] == ',':# if the character is a decimal point
                n = 10 if text[i] == '.' else 11; yoffset = height*.75# set the number to 10 if it's a decimal point, 11 if it's a comma
            else:# if the character is a number
                n = int(text[i]); yoffset = height*.08# set the number to the integer value of the character

            blit_sequence.append((renderednums[size][n], (lastwidth,yoffset)))# add to the blit sequence with the offset
            lastwidth += renderednums[size][n].get_width()+(size/13)# add the width of the current

    surf.blits(blit_sequence)
    return surf.copy()

dsize = 45
randomnumbers = [randint(0,1000000) for i in range(0,10000)]
text1 = num_renderer(16521321, dsize, "coral")
start = timeit.default_timer()
for i in range(0,10000):  
    # text = fontlist[25].render(str(16521321), pygame.Color("coral"))[0]
    text1 = num_renderer(randomnumbers[i], dsize, "coral")

stop = timeit.default_timer()
print("Time to prerender: ", (stop-start))


start = timeit.default_timer()
for i in range(0,10000):  
    text2 = fontlist[dsize].render(f"Price ${randomnumbers[i]:,.2f}", pygame.Color("coral"))[0]

stop = timeit.default_timer()
print("Time to render: ", (stop-start))
while True:
    screen.fill((0,50,0))
    
    screen.blit(text1, (0,50))
    screen.blit(text2, (0,300))
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button pressed",pygame.mouse.get_pos())


# @lru_cache(maxsize=1000)
# def num_renderer(string, size, color) -> pygame.Surface:
#     """Renders text to a surface, and returns the surface"""
#     global renderednums
#     # text = split_string(string)
#     text = f'{string:,.2f}'

#     # width,height = ((len(string)*size)//(2.1)),(size)*1.1
#     width,height = ((len(text)*size)//(2.1)),(size)*1.1
#     if size not in renderednums:
#         renderednums[size] = [fontlist[size].render(str(i), color)[0] for i in range(0,10)]
#         renderednums[size].append(fontlist[size].render('.', color)[0])
#         renderednums[size].append(fontlist[size].render(',', color)[0])

#     surf = pygame.Surface((width,height))
#     # surf.fill((0,0,0))
#     # With this line
#     # pygame.gfxdraw.box(surf, (0,0,width,height), (0,0,0))
#     surf.set_colorkey((0,0,0))

#     blit_sequence = []
#     lastwidth = 0
#     for i in range(0,len(text)):
#         if text[i].isdigit() and (text[i] == '.' or text[i] == ','):# if the character(s) is(are) a string
#             render = fontlist[size].render(text[i], color)[0]
#             lastwidth = render.get_width()
#             blit_sequence.append((render, (0 if i == 0 else lastwidth,height)))
#             lastwidth += render.get_width()+(size/13)

#         if text[i] == '.' or text[i] == ',':# if the character is a decimal point
#             n = 10 if text[i] == '.' else 11; yoffset = height*.75# set the number to 10 if it's a decimal point, 11 if it's a comma
#         else:# if the character is a number
#             n = int(text[i]); yoffset = 0# set the number to the integer value of the character

#         # if it's not the first character, add to the blit sequence with an offset
#             # if text[i-1] == '.' or text[i-1] == ',':# checking for the prior character being a decimal point
#             #     n2 = 10 if text[i-1] == '.' else 11
#             # else:
#             #     n2 = int(text[i-1])
#         blit_sequence.append((renderednums[size][n], (lastwidth,yoffset)))# add to the blit sequence with the offset
#         lastwidth += renderednums[size][n].get_width()+(size/13)# add the width of the current

#     surf.blits(blit_sequence)
#     return surf.copy()
