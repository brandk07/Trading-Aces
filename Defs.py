import pygame
import time
from pygame import gfxdraw
from pygame import freetype
import math
import json
pygame.font.init()
def update_fps(clock):
    fps = str(int(clock.get_fps()))
    fps_text = fontlist[25].render(fps, pygame.Color("coral"))[0]
    return fps_text

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.5f} seconds to execute.")
        return result
    return wrapper

def time_loop(loop):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        for item in loop:
            result = item(*args, **kwargs)
        end_time = time.time()
        print(f"Loop took {end_time - start_time:.5f} seconds to execute.")
        return result
    return wrapper
pygame.init()
def Getfromfile(stockdict:dict,player):
    with open('Assets/Stockdata/extradata.json','r') as file:
        data = json.load(file)
        if data:
            player.stocks = [[stock[0],stock[1],stockdict[stock[0]]] for stock in data[1]]#[name,price,obj] can't save the object so I save the name and use that to get the object
            player.messagedict = data[2]
            player.graphrange = data[3]
            player.cash = data[4] if data[4] != 0 else 2500
            for i,stockobj in enumerate(stockdict.values()):
                stockobj.graphrange = data[i+5]
            return data[0]#gametime
        else:
            return [0,0,0,9,30,0,'am']#starting time
def Writetofile(stocklist,player,data):
    for stock in stocklist:
        stock.save_data()
    player.save_data()
    with open('Assets/Stockdata/extradata.json','w') as file:
        file.seek(0)# go to the start of the file
        file.truncate()# clear the file
        json.dump(data,file)
    pygame.quit()
    quit()
# currentime = months,weeks,days,hours,minutes,update interval ,am/pm
def Gametime(currentime,playing,screen:pygame.Surface,fps):
    if playing:
        currentime[5] += 1
        if currentime[5] >= 3*60:#update interval, 3*fps(60) = 1 minute in game
            currentime[5] = 0
            currentime[4] += 1
        if currentime[4] >= 60:#if minutes is 60, reset minutes to 0 and add 1 to hours
            currentime[4] = 0
            currentime[3] += 1
        if currentime[3] >= 12:#if hours is 12, reset hours to 1 and change am/pm
            currentime[3] = 1
            currentime[6] = 'pm' if currentime[6] == 'am' else 'am'
    # numtime_text,rect = fontlist[50].render(f'{currentime[3]}:{"0" if currentime[4] < 10 else ""}{currentime[4]}{currentime[6]}',(255,255,255))

    # numtime_rect = numtime_text.get_rect(center=(100, 950))

    # polygon_points = [(25, 925), (175, 925), (175, 975), (25, 975)]
    # pygame.draw.polygon(screen, (80, 80, 80), polygon_points)
    # pygame.draw.polygon(screen, (255, 255, 255), polygon_points, 5)
    # pygame.draw.polygon(screen, (0, 0, 0), polygon_points, 1)
    # screen.blit(numtime_text, numtime_rect)

    return currentime
    
# fonts = lambda font_size: pygame.font.SysFont(r'Assets/antonio/Antonio-Regular.ttf',font_size)
# fonts = lambda font_size: pygame.font.SysFont(r'Assets/antonio/Antonio-Bold.ttf',font_size)
fonts = lambda font_size: freetype.Font(r'Assets/antonio/Antonio-Regular.ttf', font_size*.75)
fontsbold = lambda font_size: freetype.Font(r'Assets/antonio/Antonio-Bold.ttf', font_size*.75)
# fonts = lambda font_size: freetype.Font(r'Assets\antonio\Liquid_Crystal_Extra_Characters.otf', font_size)
bold40 = fontsbold(45)
fontlist = [fonts(num) for num in range(0,100)]#list of fonts from 0-100
font45 = fonts(45)

def drawgametime(currenttime,screen:pygame.Surface):
    numtime_text,rect = fontlist[50].render(f'{currenttime[3]}:{"0" if currenttime[4] < 10 else ""}{currenttime[4]}{currenttime[6]}',(255,255,255))
    numtime_rect = numtime_text.get_rect(center=(100, 950))
    polygon_points = [(25, 925), (175, 925), (175, 975), (25, 975)]
    pygame.draw.polygon(screen, (80, 80, 80), polygon_points)
    pygame.draw.polygon(screen, (255, 255, 255), polygon_points, 5)
    pygame.draw.polygon(screen, (0, 0, 0), polygon_points, 1)
    screen.blit(numtime_text, numtime_rect)
#for time testing
# start_time = time.time()

# for i, point in enumerate(self.pricepoints):
#     # do something

# end_time = time.time()
# print(f"Loop took {end_time - start_time:.5f} seconds to execute.")