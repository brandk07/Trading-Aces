import pygame,time
from pygame import gfxdraw,freetype
import os,re,json,math,timeit,random
from random import randint
from collections import deque
from Classes.AssetTypes.OptionAsset import OptionAsset
from Classes.AssetTypes.StockAsset import StockAsset
from Classes.AssetTypes.IndexFundsAsset import IndexFundAsset
from Classes.AssetTypes.LoanAsset import LoanAsset
import numpy as np
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
from Classes.imports.Messages import ErrorMessageHandler
from Classes.imports.Animations import BuyAnimation
from functools import lru_cache 
pygame.font.init()
pygame.mixer.init()
pygame.init()

TXTCOLOR = (220,220,220)
POINTSPERGRAPH = 500
MAXSTEP = 50# Max points that can be added to the graph at a time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
        return result
    return wrapper


#  ////////////////////////////////////////////Fonts///////////////////////////////////////////////////////////////////////////////////////

crystalfonts = lambda font_size: freetype.Font(r'Assets\fonts\LiquidCrystal\Liquid_Crystal_Extra_Characters.otf', font_size*.75)
pixfonts = lambda font_size: freetype.Font(r'Assets\fonts\Silkscreen\Silkscreen-Regular.ttf', font_size*.75)
fontsbold = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Bold.ttf', font_size*.75)
fontsLight = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Light.ttf', font_size*.75)
# FUN THEME
# fonts = lambda font_size: freetype.Font(r'Assets\fonts\Bangers\Bangers-Regular.ttf', font_size*.75)
# fontsbold = lambda font_size: freetype.Font(r'Assets\fonts\Bangers\Bangers-Regular.ttf', font_size*.75)
# fonts = lambda font_size: freetype.Font(r'Assets\antonio\Liquid_Crystal_Extra_Characters.otf', font_size)
bold40 = fontsbold(45)
fonts = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Regular.ttf', font_size*.75)
fontlist = [fonts(num) for num in range(0,201)]#list of fonts from 0-100
fontlistcry = [crystalfonts(num) for num in range(0,201)]#list of fonts from 0-100
fontlistLight = [fontsLight(num) for num in range(0,201)]#list of fonts from 0-100
fontlistpix = [pixfonts(num) for num in range(0,201)]#list of fonts from 0-100
fontlistbold = [fontsbold(num) for num in range(0,201)]#list of fonts from 0-100
font45 = fonts(45)
GRAPHRANGES = ["1H","1D","5D","1M","6M","1Y","5Y"]
MINRANGE = GRAPHRANGES[0]
MAXRANGE = GRAPHRANGES[-1]
INDEXNAMES = ["TDIF","IEIF", "FHMF","Total"]
INDEXFULLNAMES = ['Tech Digital Innovation Fund','Industrial Evolution Index Fund','Future Health Momentum',"Total Market"]

STOCKNAMES = ['QSYN','NRLX','CMDX','PRBM','GFRG','ASCS','BGTX','MCAN','VITL']
FULLSTOCKNAMES = ["QuantumSync Solutions","NeuraNex Technologies","CloudMatrix Systems","Precision Robotics Manufacturing","GreenForge Materials","Atlas Supply Chain Solutions","BioGenix Therapeutics","MediCare Analytics","Vitality Senior Living"]
FSTOCKNAMEDICT = {STOCKNAMES[i]:FULLSTOCKNAMES[i] for i in range(len(STOCKNAMES))}



@lru_cache(maxsize=250)
def s_render(string:str, size, color,font='reg') -> pygame.Surface:
    """Caches the renders of the strings, and returns the rendered surface"""
    # print(f"Caching arguments: {string}, {size}, {color}")
    assert isinstance(string,str), 'The string must be a string'
    if font == 'reg':
        text = fontlist[size].render(string, (color))[0]
    elif font == 'cry':
        text = fontlistcry[size].render(string, (color))[0]
    elif font == 'light':
        text = fontlistLight[size].render(string, (color))[0]
    elif font == 'pix':
        text = fontlistpix[size].render(string, (color))[0]
    elif font == 'bold':
        text = fontlistbold[size].render(string, (color))[0]

    return text
#  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
errors = ErrorMessageHandler(s_render)# error messages DO errors.addMessage(txt:str,coords:list=None)
animationList : list[BuyAnimation] = []
# bigMessageList = []

soundEffects = {# soundEffects['generalClick'].play()
    # 'menuClick': pygame.mixer.Sound(r'Assets\Soundeffects\menuClick.wav'),
    'menuClick': pygame.mixer.Sound(r'Assets\NewSoundEffects\menuClick.wav'),
    'generalClick': pygame.mixer.Sound(r'Assets\Soundeffects\generalClick.wav'),
    'error' : pygame.mixer.Sound(r'Assets\Soundeffects\error.wav'),
    # 'buy': pygame.mixer.Sound(r'Assets\Soundeffects\buy.wav'),
    'buyStock': pygame.mixer.Sound(r'Assets\NewSoundEffects\buyStock.wav'),
    'buyOption': pygame.mixer.Sound(r'Assets\NewSoundEffects\OptionBuy.wav'),
    'sellGain' : pygame.mixer.Sound(r'Assets\NewSoundEffects\sellGain.wav'),
    'sellLoss' : pygame.mixer.Sound(r'Assets\NewSoundEffects\sellLoss.wav'),
    'buyLoan' : pygame.mixer.Sound(r'Assets\NewSoundEffects\buyStock.wav')
}

musicThemes = {}
for song in os.listdir(r'Assets\Music\themes'):
    musicThemes[f'maintheme{song}'] = rf'Assets\Music\themes\{song}'
print(musicThemes)

def playmusic(musicdata):
    if musicdata[0] == 0:
        pygame.mixer.music.load(r"Assets\Music\themes\maintheme1.wav")
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.load(rf"Assets\Music\themes\maintheme{musicdata[0]}.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.get_endevent
    pygame.mixer.music.set_volume(musicdata[1])
    
    return musicdata

# Mostly used for deciding color of the percent change, it was just really annoying to write out the if statements every time
p3choice = lambda negative, positive, zero, change : (negative if change < 0 else positive) if round(change,2) != 0 else zero

getTSizeCharsAndNums = lambda chars, xSpace : int(((xSpace/chars)-0.9506)/0.2347)# 
# strSizes = {'0': (0.259, 1.201), '1': (0.158, 0.697), '2': (0.229, 1.031), '3': (0.25, 1.221), '4': (0.273, 0.977), '5': (0.226, 0.787), '6': (0.262, 0.832), '7': (0.258, 0.987), '8': (0.248, 1.372), '9': (0.248, 0.873), '.': (0.065, 0.885)}
# returns the font size that will fit the text in the xSpace
strSizes = {str(num):[fontlist[i].get_rect(str(num)) for i in range(1,199)] for num in range(10)}
strSizes['.'] = ([fontlist[i].get_rect('.') for i in range(1,199)])
def getTSizeNums(chars:str, xSpace:int,maxsize:int=199) -> int:
    """Returns the font size that will fit the text in the xSpace"""
    xSpace*=.7
    def getSize(size, totalSpace, chars, lastwidth:int):
        """Lastwidth is the last width of text, totalSpace is the total space the text should take up, chars is the text to be rendered"""
        newSum = sum([fontlist[size].get_rect(c).width for c in chars])
        if newSum == totalSpace:
            return size
        elif newSum < totalSpace and lastwidth > totalSpace:# if the current is under, but the last was too big, than current is best
            return size
        elif newSum > totalSpace and lastwidth < totalSpace:# If the current is too big, but the last was smaller, than last is best
            return size-1 if size > 1 else 1
        elif newSum < totalSpace and lastwidth < totalSpace:
            if size >= maxsize:
                if size >= 199:
                    print("Max txt size reached from (getTSizeNums in Defs)")# Won't raise an error, but will return the max size
                return maxsize
            return getSize(size+1, totalSpace, chars, newSum)
        elif newSum > totalSpace and lastwidth > totalSpace:
            if size <= 1:
                print("Min size reached from (getTSizeNums in Defs)")# Won't raise an error, but will return the min size
            return getSize(size-1, totalSpace, chars, newSum)
        else:
            print(newSum, totalSpace, lastwidth, size, chars, fontlist[size].get_rect(chars).width)
    if chars == '': return 1
    getTSizeNum = lambda chars, xSpace : int(((xSpace/len(chars))+0.8)/0.225)
    testSize = max(min(getTSizeNum(chars, xSpace),maxsize),1)
    return getSize(testSize, xSpace, chars, 0)

brightenCol = lambda color, multiplier : tuple([min(255, c*multiplier) for c in color])# brightens the color by the multiplieron

def reuserenders(renderlist,texts,textinfo,position) -> list:
    """renderlist is a list of dicts, 
    texts is the list of strings to be rendered, 
    textinfo is a list of tuples containing the font size and the font index, 
    position is the index of the renderlist to be used"""
    for x, text in enumerate(texts):
        if text in renderlist[position]:
            render = renderlist[position][text]  # reuse old renders if possible
            renderlist[position].pop(text)  # remove the text from the recentrenders
            renderlist[position][text] = render  # add the text back to the recentrenders - so it is at the end of the dict (doesn't get deleted)
        else:  # if the text is not in the recentrenders or recent renders doesn't have enough texts
            render = fontlist[textinfo[x][1]].render(text, textinfo[x][0])[0]  # render the text
            renderlist[position][text] = render  # add the text to the recentrenders
    for text in list(renderlist[position].keys()):
        if text not in texts:
            renderlist[position].pop(text)
    return renderlist
emptytext = fontlist[45].render('Empty',(190,190,190))[0]

def getScreenRefreshBackGrounds(surface:pygame.Surface):
    menuSurface = surface.copy()
    screenSurface = surface.copy()
    menupoints = [(185,10),(1910,10),(1910,980),(185,980)]
    topbarpoints = [(185,10),(1910,10),(1910,95),(185,95)]
    gfxdraw.filled_polygon(menuSurface, menupoints,(40,40,40,150))
    pygame.draw.polygon(menuSurface, (0,0,0), menupoints,5)

    gfxdraw.filled_polygon(menuSurface, topbarpoints,(85,85,85))
    pygame.draw.polygon(menuSurface, (0,0,0), topbarpoints,5)

        
    return menuSurface,screenSurface
def doBuffer(screen:pygame.Surface,backgroundBtyes):
    pixels = screen.get_buffer()
    pixels.write(backgroundBtyes)
    del pixels  # Release the buffer


def text_input(screen, coords, wh, current_str, keyPressed, txtSize=45) -> str:
    """Draws an input box on the screen and , returns the text in the box"""
    input_rect = pygame.Rect(coords, wh)
    
    special_keys = {
        "return": "Enter",
        "space": "Space",
        "backspace": "Backspace",
        "left shift": "Shift",
        "right shift": "Shift",
        "left ctrl": "Ctrl",
        "right ctrl": "Ctrl",
        "left alt": "Alt",
        "right alt": "Alt",
        "tab": "Tab",
        "escape": "Esc"
    }
    if keyPressed == None:
        pass
    
    elif keyPressed in list(special_keys.values()):
        if keyPressed == "Backspace" and len(current_str) > 0:
            current_str = current_str[:-1]
        # elif special_keys[key] == "Enter":
        #     return current_str
        elif keyPressed == "Space":
            current_str += " "
    else:
        if len(keyPressed) == 1 and len(current_str) <  30:
            current_str += keyPressed
    
    # Draw input box and text
    
    pygame.draw.rect(screen, (0, 0, 0), input_rect, 5, 10)

    width,height = drawCenterTxt(screen, current_str, txtSize, (255, 255, 255), (coords[0] + wh[0]//2, coords[1]+wh[1]-22), centerY=False,fullY=True)
    
    # make the cursor blink
    if int(time.time() * 2) % 2 == 0:
        
        lw = fontlist[txtSize].get_rect(' ' if len(current_str) == 0 else current_str[-1]).width
        x = coords[0] + wh[0]//2 + width/2 - lw - 1
        y = coords[1] + wh[1]//2 + 20 + 3
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x,y,lw+4,3))
    return current_str

@lru_cache(maxsize=15)
def getBorderedImage(image:pygame.Surface,borderWidth:int,borderColor:tuple,wh:tuple,borderRadius:int) -> pygame.Surface:
    """Returns the image with a border around it (IF YOUR IMAGE HAS THE COLOR (1,1,1) IN IT, IT WILL BE REMOVED)"""

    outSideSurf = pygame.Surface(wh)# first create an outside surface
    outSideSurf.fill((1,1,1))# fill it with a color that is not in the image
    pygame.draw.rect(outSideSurf,(0,0,0),(0,0,wh[0],wh[1]),border_radius=borderRadius)# draw a cutout of what is be displayed on the realSurf
    outSideSurf.set_colorkey((0,0,0))# make that cut out transparent

    realSurf = pygame.Surface(wh)# create the real surface
    if image.get_width() != wh[0] or image.get_height() != wh[1]:# if the image is not the same size as the surface
        image = pygame.transform.smoothscale(image,wh)
    realSurf.blit(image,(0,0))# blit the image to the real surface first
    realSurf.blit(outSideSurf,(0,0))# blit the outside surface to the real surface (out side is black, so it will cut out the image)
    realSurf.set_colorkey((1,1,1))# remove that outside black portion
    pygame.draw.rect(realSurf,borderColor,(0,0,wh[0],wh[1]),width=borderWidth,border_radius=borderRadius)

    return realSurf

def drawBoxedImage(screen,coords,image,wh=None,borderRadius=0,borderWidth=5,borderColor=(0,0,0)):
    """Draws a box around the image, with the border width and color"""
    if wh == None:
        wh = image.get_width(),image.get_height()
    if borderRadius != 0:
        image = getBorderedImage(image,borderWidth,borderColor,wh,borderRadius)
        screen.blit(image,coords); return
    
    screen.blit(image,coords)
    pygame.draw.rect(screen,borderColor,(*coords,*wh),borderRadius)



def drawCenterTxt(screen,text:str,txtSize:int,color:tuple,coords:tuple,centerX=True,centerY=True,fullX=False,fullY=False,outline=False,font='reg') -> tuple:
    """Draws text centered on the screen, 
    centerx and y will minus half the wh of the txt,
    full will minus the full width of the txt (drawing from the top left)
    returns the width and height of the text"""
    valueText = s_render(text,txtSize,color,font)
    x,y = coords
    width,height = valueText.get_width(), valueText.get_height()
    if centerX: x -= width//2
    if centerY: y -= height//2
    if fullX: x -= width
    if fullY: y -= height
    screen.blit(valueText,(x,y))
    if outline:
        pygame.draw.rect(screen, (0,0,0), (x-5,y-5,width+10,height+10), 5, 10)
    return width,height

def drawCenterRendered(screen,renderedTxt,coords:tuple,centerX=True,centerY=True,fullX=False,fullY=False) -> None:
    """Works same as drwaCenterTxt but with pre-rendered text
    centerx and y will minus half the wh of the txt,
    full will minus the full width of the txt (drawing from the top left) """
    valueText = renderedTxt
    x,y = coords
    if centerX: x -= valueText.get_width()//2
    if centerY: y -= valueText.get_height()//2
    if fullX: x -= valueText.get_width()
    if fullY: y -= valueText.get_height()
    screen.blit(valueText,(x,y))
def drawClickableBox(screen,coords:tuple,text:str,textsize:int,color1:tuple,color2:tuple,mousebuttons:int,centerX=False,centerY=False,fill=False,border=True,topLeftX=False) -> bool:
    """Draws a clickable box on the screen, returns True if the box is clicked
    Will center the X position onto coords[0] of the text if centerX is True"""
    
    valueText = s_render(text,textsize,color1)
    x,y = coords
    w,h = valueText.get_width()+50, valueText.get_height()+30
    if centerX: x -= w//2
    if centerY: y -= h//2
    if topLeftX: x -= w
    if border:
        pygame.draw.rect(screen, (0,0,0), (x,y,w,h), 5, 10)
    
    myrect = pygame.Rect(x,y,w,h)

    if myrect.collidepoint(pygame.mouse.get_pos()):
        if fill:# Rather than changing the text, the box will fill in
            pygame.draw.rect(screen, color2, (x,y,w,h), border_radius=10)
            pygame.draw.rect(screen, (0,0,0), (x,y,w,h), 5, 10)
        else:# The text will change color
            valueText = s_render(text,textsize,color2)# re-render the text with a different color

        if mousebuttons == 1:
            soundEffects['generalClick'].play()
            return True
        
    screen.blit(valueText,(x+25,y+15))
    return False
def drawClickableTxt(screen,coords,text,textsize,color1,color2,mousebuttons,centerX=False,centerY=False):
    """Draws a clickable text on the screen, returns True if the text is clicked"""
    valueText = s_render(text,textsize,color1)
    x,y = coords
    if centerX: x -= valueText.get_width()//2
    if centerY: y -= valueText.get_height()//2
    myrect = pygame.Rect(x,y,valueText.get_width(),valueText.get_height())

    if myrect.collidepoint(pygame.mouse.get_pos()):
        valueText = s_render(text,textsize,color2)# re-render the text with a different color
        if mousebuttons == 1:
            soundEffects['generalClick'].play()
            return True
    screen.blit(valueText,(x,y))
def drawClickableBoxWH(screen,coords:tuple,wh:tuple,text:str,textsize:int,color1:tuple,color2:tuple,mousebuttons:int,fill=False) -> bool:
    """Same as drawClickable Box, but you give width and height and the text will be centered"""
    
    valueText = s_render(text,textsize,color1)
    x,y = coords
    w,h = wh

    pygame.draw.rect(screen, (0,0,0), (x,y,w,h), 5, 10)
    
    myrect = pygame.Rect(x,y,w,h)

    if myrect.collidepoint(pygame.mouse.get_pos()):
        if fill:# Rather than changing the text, the box will fill in
            pygame.draw.rect(screen, color2, (x,y,w,h), border_radius=10)
            pygame.draw.rect(screen, (0,0,0), (x,y,w,h), 5, 10)
        else:# The text will change color
            valueText = s_render(text,textsize,color2)# re-render the text with a different color

        if mousebuttons == 1:
            soundEffects['generalClick'].play()
            return True
        
    screen.blit(valueText,(x+(w//2)-(valueText.get_width()//2),y+(h//2)-(valueText.get_height()//2)))
    return False
def drawBoxedText(screen,text,size,boxcolor,textcolor,pos):
    valueText = s_render(text,size,textcolor)
    x = pos[0]-(valueText.get_width()//2)-25; y = pos[1]-(valueText.get_height()//2)-15
    w,h = valueText.get_width()+50, valueText.get_height()+30
    pygame.draw.rect(screen, boxcolor, (x,y,w,h), border_radius=10)
    pygame.draw.rect(screen, (1,1,1), (x,y,w,h), 5, 10)
    
    screen.blit(valueText,(pos[0]-(valueText.get_width()//2),pos[1]-(valueText.get_height()//2)))

def drawBoxedTextWH(screen,coords,wh,text,size,textcolor,centerX=False,centerY=False,fill=None) -> None:
    """Fill should be the color it is filled with, if None, it will just be the text and outline"""
    x,y = coords
    if centerX: x -= wh[0]//2
    if centerY: y -= wh[1]//2

    w,h = wh
    
    if fill != None:
        pygame.draw.rect(screen, fill, (x,y,w,h), border_radius=10)
    pygame.draw.rect(screen, (0,0,0), (x,y,w,h), 5, border_radius=10)

    
    drawCenterTxt(screen,text,size,textcolor,(x+w//2,y+h//2),centerX=True,centerY=True)


def drawLatterScroll(screen:pygame.Surface,values:list,allrenders:list,barvalue:int,getpoints,shifts:tuple,selected_value:int,mousebuttons:int,defaultHeight:int,alltexts,percents) -> list:
    """Draws the scroll bar for the latter menu"""
    xshift,yshift = shifts
    mousex, mousey = pygame.mouse.get_pos()

    for i, stock in enumerate(values[barvalue:barvalue+5]):
        ioffset = i+barvalue
        texts = alltexts[i]
        twidth = allrenders[i][texts[0]].get_width() + 25
        twidth2 = max(allrenders[i][texts[1]].get_width(), allrenders[i][texts[2]].get_width()) + 40
        twidth3 = max(allrenders[i][texts[3]].get_width(), allrenders[i][texts[4]].get_width()) + 45
        
        # find the points for the polygons
        points,points2,points3,totalpolyon = getpoints(twidth, twidth2, twidth3, (i * xshift), (i * yshift))

        # check if the mouse is hovering over the polygon
        hover = False
        if point_in_polygon((mousex, mousey), totalpolyon):  # check if mouse is inside the polygon
            hover = True
            if mousebuttons == 1:
                soundEffects['generalClick'].play()
                selected_value = ioffset

        polycolor = (30, 30, 30) if not hover else (80, 80, 80)
        # polycolor = (60, 60, 60) if selected_value == ioffset else polycolor

        # ----------Draw the text----------
        screen.blit(allrenders[i][texts[0]], (points[0][0] + 20, points[0][1] + 35))  # display name of stock
        screen.blit(allrenders[i][texts[2]], (points[0][0] + 45 + twidth, points[0][1] + 65))# display current price of stock

        screen.blit(allrenders[i][texts[1]], (points[0][0] + 30 + twidth, points[0][1] + 10))# display bought price of stock
        screen.blit(allrenders[i][texts[3]], (points[0][0] + 30 + twidth + twidth2, points[0][1] + 10))# display profit of stock
        screen.blit(allrenders[i][texts[4]], (points[0][0] + 45 + twidth + twidth2, points[0][1] + 65))# display percent change of stock
        
        # top left, top right, bottom right, bottom left
        bottom_polygon = [[totalpolyon[0][0]+12, totalpolyon[0][1] + defaultHeight - 15], 
                            [totalpolyon[1][0], totalpolyon[1][1]], 
                            [totalpolyon[2][0], totalpolyon[2][1]], 
                            [totalpolyon[3][0], totalpolyon[3][1]],
                            [totalpolyon[3][0]-15, totalpolyon[3][1]],
                            [totalpolyon[3][0]-3, totalpolyon[3][1] + defaultHeight - 15],
                            ]
        if hover or selected_value == ioffset:
            if percents[i] > 0:bottomcolor = (0, 200, 0)
            elif percents[i] == 0:bottomcolor = (200, 200, 200)
            else:bottomcolor = (200, 0, 0)
        else:
            if percents[i] > 0: bottomcolor = (0, 80, 0)
            elif percents[i] == 0: bottomcolor = (80, 80, 80)
            else: bottomcolor = (80, 0, 0)
        if not selected_value == ioffset:
            pygame.draw.polygon(screen, bottomcolor, bottom_polygon)
        outlinecolor = (0, 0, 0) if selected_value != ioffset else (180, 180, 180)
        pygame.draw.polygon(screen, outlinecolor, points, 5)  # draw the outline of the polygon
        pygame.draw.polygon(screen, outlinecolor, points2, 5)  # draw the outline of the second polygon
        pygame.draw.polygon(screen, outlinecolor, points3, 5)  # draw the outline of the third polygon
            
    emptyboxnum = 5-len([(stock) for i,stock in enumerate(values) if i >= barvalue and i < barvalue+5])
    for i in range(emptyboxnum):
        ioffset = i+(5-emptyboxnum)
        points,points2,points3,totalpolyon = getpoints(150,200,200,(ioffset*xshift),(ioffset*yshift))
        
        gfxdraw.filled_polygon(screen, points, (30,30,30))
        gfxdraw.filled_polygon(screen, points2, (30,30,30))
        gfxdraw.filled_polygon(screen, points3, (30,30,30))
        pygame.draw.polygon(screen, (0,0,0), points, 5)
        pygame.draw.polygon(screen, (0,0,0), points2, 5)
        pygame.draw.polygon(screen, (0,0,0), points3, 5)
        # screen.blit(emptytext, (320 + (ioffset * xshift), 235 + (ioffset * yshift)))  # display name of stock
        # Use the points from the first polygon to draw teh empty text
        screen.blit(emptytext, (points[0][0]+40, points[0][1]+40))  # displays empty text
    return allrenders,selected_value



def checkboxOptions(screen,options,selectedOptions,pos,wh,mousebuttons,disabledOptions=None,txtSize=30) -> tuple:
    """Displays the options in options, will return the option that is click (option,index), 
    disabledOptions is a list of options that are disabled,"""
    width = wh[0]//len(options)
    if disabledOptions == None:
        disabledOptions = {}
    
    for i,option in enumerate(options):
        
        x,y = pos[0]+(i*width),pos[1]
        rect = pygame.Rect(x,y,width-5,wh[1])
        color = (120,120,120)
        txt = s_render(option, txtSize, (210, 210, 210))
        screen.blit(txt, (x+5+width/2-txt.get_width()/2,y+wh[1]/2-txt.get_height()/2))
        if rect.collidepoint(pygame.mouse.get_pos()):
            color = (160,160,160) if not option in disabledOptions else (200,0,0)
            pygame.draw.rect(screen, color, rect, width=3,border_radius=10)
            if mousebuttons == 1:
                soundEffects['generalClick'].play()
                return (option, i)
                # screen.blit(s_render(disabledOptions[option], 40, (180,0,0)), (x,y-20))

        if option not in disabledOptions:
            pygame.draw.rect(screen, (0,0,0), [x+10,y+wh[1]/2-8,16,16], 3)# draws the outline of the box
        # rectangle inside the one above
        if option in selectedOptions:
            pygame.draw.rect(screen, color, rect, width=3,border_radius=10)
            pygame.draw.rect(screen, (200,200,200), [x+13,y+wh[1]/2-5,10,10])

def drawBoxedLines(screen,coords:tuple,txt:str,linesNum:int,txtSize:int,color:tuple,centerX=False,centerY=False,fullX=False,fullY=False) -> None:
    """Draws a box with lines of text in it"""
    x,y = coords

    txtLines = separate_strings(txt,linesNum)
    txtLines = [s_render(line,txtSize,color) for line in txtLines]
    maxX = max([line.get_width() for line in txtLines])
    w,h = maxX+40, (txtLines[0].get_height()+10)*linesNum+20
    if centerX: x -= w//2
    if centerY: y -= h//2
    if fullX: x -= w
    if fullY: y -= h
    if x+w > screen.get_width():
        x = screen.get_width()-w
    if y+h > screen.get_height():
        y = screen.get_height()-h
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    pygame.draw.rect(screen, (40,40,40), (x,y,w,h), border_radius=10)
    pygame.draw.rect(screen, (0,0,0), (x,y,w,h), 3, 10)
    for i, line in enumerate(txtLines):
        # screen.blit(line,(x+20,y+10+(i*(txtLines[0].get_height()+10))))
        drawCenterRendered(screen,line,(x+w//2,y+10+(i*(txtLines[0].get_height()+10))),centerX=True,centerY=False)

    

def drawLinedInfo(screen,coord:tuple,wh:tuple,infoList:list[(str,int|str)],txtsize,color,middleData=None,diffSizes=None):
    """Draws the info in infoList [str (left side), value:int/str (right side)], in the box at coord with width and height wh
    Diff sizes can be a tuple containing the sizes of the left and right side text"""
    if middleData != None:
        assert len(infoList) == len(middleData), 'The middleData must be the same length as the infoList'

    sep = wh[1]//len(infoList)
    x,y = coord
    y += sep/3
    for i, (string,value) in enumerate(infoList):
        newY = y+(i*sep)
        screen.blit(s_render(string,txtsize if not diffSizes else diffSizes[0],color),(x+10,newY))# display the string on the left
        valueText = s_render(str(value),txtsize if not diffSizes else diffSizes[1],color)# render the value
        screen.blit((valueText),(x+wh[0]-valueText.get_width()-10,newY))
        if middleData != None and middleData[i] != "":
            drawCenterTxt(screen,middleData[i],txtsize,color,(x+wh[0]//2,newY),centerX=True,centerY=False)
        if i != len(infoList)-1:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, newY+(sep/2)*1.2, wh[0], 3))

def drawLinedInfoBigColored(screen,coord:tuple,wh:tuple,infoListL:list,infoListR:list,sizeLg:int,sizeSm:int,colors:list):
    """Displays two lists with str1,value1 on left and str2,value2 on right
    the str is bigger and the the second dict's str is colored"""
    assert len(infoListL) == len(infoListR), 'The two lists must have the same length'
    sep = wh[1]//len(infoListL)
    x,y = coord
    for i, ((leftStr,leftVal),(rightStr,rightVal)) in enumerate(zip(infoListL,infoListR)):
        newY = y+(i*sep)
        lStr = s_render(leftStr,sizeLg,TXTCOLOR)# string on the left (Q1)
        rStr = s_render(rightStr,sizeLg,colors[i])# string on the right (Beat/Miss) with color
        lVal = s_render(str(leftVal),sizeSm,(120,120,120))# value on the left (Q1)
        rVal = s_render(str(rightVal),sizeSm,colors[i])# value on the right (Beat/Miss) with color
        screen.blit(lStr,(x+10,newY))# display the string on the left
        totalXw = rStr.get_width()+rVal.get_width()
        screen.blit(rStr,(x+wh[0]-totalXw-15,newY))# display the string on the right
        yposl = newY+lStr.get_height()-lVal.get_height()
        yposr = newY+rStr.get_height()-rVal.get_height()
        screen.blit(lVal,(x+20+lStr.get_width(),yposl))# display the value on the left
        screen.blit(rVal,(x+wh[0]-rVal.get_width()-5,yposr))# display the value on the right

        # screen.blit((valueText),(x+wh[0]-valueText.get_width()-10,newY))
        if i != len(infoListL)-1:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, newY+(sep/2)*1.2, wh[0], 3))
                
def update_fps(clock,lastfps:deque):
    fps = str(int(clock.get_fps()))
    lastfps.append(fps)
    fps_text = s_render(fps, 25, (225,64,35))
    intlastfps = [int(fps) for fps in lastfps]
    averagefps = sum(intlastfps)/len(lastfps)
    averagefps_text = s_render(str(int(averagefps)), 25, (225,64,35))
    lowestfps = min(intlastfps)
    lowestfps_text = s_render(str(lowestfps), 25, (225,64,35))
    return fps_text,averagefps_text,lowestfps_text

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.5f} seconds to execute.")
        return result
    return wrapper
def limit_digits(num, max_digits,truncate=False) -> str:
    
    if len("{:,.2f}".format(num)) > max_digits:
        return "{:,.2e}".format(num)    
    else:
        return f"{int(num):,d}" if truncate else f"{num:,.2f}"
def time_loop(loop):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        for item in loop:
            result = item(*args, **kwargs)
        end_time = time.time()
        print(f"Loop took {end_time - start_time:.5f} seconds to execute.")
        return result
    return wrapper
def setGameTime(gametime):
    with open('Assets/extradata.json','r') as file:
        data = json.load(file)
        if data:
            gametime.setTimeStr(data[0])
            # return gametime
def Getfromfile(stockdict:dict,indexFunds:dict,player,gametime):
    with open('Assets/extradata.json','r') as file:
        data = json.load(file)
        print(data)
        if data:
            # gametime.setTimeStr(data[0])
            # player.stocks = [[stockdict[stock[0]],stock[1],stock[2]] for stock in data[1]]#[name,price,obj] can't save the object so I save the name and use that to get the object
            # print(data[1])
            player.stocks = [StockAsset(player,stockdict[stock[0]],stock[1],stock[2],stock[3],dividends=stock[4],portfolioPercent=stock[5]) for stock in data[1]]# [stockobj,creationdate,ogprice,quantity]
            player.options = [OptionAsset(player,stockdict[option[0]],option[1],option[2],option[3],option[4],option[5],porfolioPercent=option[6],ogValue=option[7],color=tuple(option[8])) for option in data[2]]# options storage is [stockname,strikeprice,expirationdate,optiontype,quantity,ogprice]
            player.loans = [LoanAsset(loan[0],loan[1],loan[2],loan[3],loan[4],loan[5]) for loan in data[3]]# loans storage is [rate,term,principal,principalLeft,interestpaid, termleft]
            player.indexFunds = [IndexFundAsset(player,indexFunds[indexfund[0]],indexfund[1],indexfund[2],indexfund[3],dividends=indexfund[4],portfolioPercent=indexfund[5]) for indexfund in data[4]]# indexfunds storage is [name,creationdate,ogprice,quantity,dividends]
            # player.graphrange = data[3]
            player.cash = data[5] if data[5] != 0 else 2500
            musicdata = (data[6])

            player.getExtraData(data[7],gametime)
            # for i,stockobj in enumerate(stockdict.values()):
            #     stockobj.graphrange = data[i+6]
            return musicdata
        else:
            player.getExtraData(None,gametime)
        return [0,0,0]# time, volume, songindex

def Writetofile(stocklist,player,data):
    for stock in stocklist:
        stock.save_data()
    player.save_data()
    
    with open('Assets/extradata.json','w') as file:
        file.seek(0)# go to the start of the file
        file.truncate()# clear the file
        json.dump(data,file)

def closest_point(master_point, points):
    return min(points, key=lambda point: math.sqrt((point[0] - master_point[0])**2 + (point[1] - master_point[1])**2))

def pointInCircle(point, circlePos,radius) -> bool:
    """Checks if a point is inside a circle."""
    return math.sqrt((point[0] - circlePos[0])**2 + (point[1] - circlePos[1])**2) < radius

def point_in_polygon(point, polygon) -> bool:
    """Checks if a point is inside a polygon."""
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if (point[1] > min(p1y, p2y)) and (point[1] <= max(p1y, p2y)) and (point[0] <= max(p1x, p2x)):
            if p1y != p2y:
                xinters = (point[1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if (p1x == p2x) or (point[0] <= xinters):
                    inside = not inside
        p1x, p1y = p2x, p2y
    return inside
def point_in_triangle(point, triangle):
    """Checks if a point is inside a triangle."""
    x, y = point
    x1, y1 = triangle[0]
    x2, y2 = triangle[1]
    x3, y3 = triangle[2]
    denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
    c = 1 - a - b
    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1
@lru_cache(maxsize=10)
def createbacksurf(radius):
    backsurface = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
    backsurface.fill((0, 0, 0))
    pygame.draw.circle(backsurface, (255, 255, 255), (radius, radius), radius)
    backsurface.set_colorkey((255, 255, 255))
    return backsurface
def draw_pie_chart(screen: pygame.Surface, values:list, radius, coords):
        """Draws the pie chart for the portfolio menu. value is (value, name, color)"""
        # the polygons are blit to this, then the backsurface is blit, then the backsurface is turned transparent and wholesurf is blit to the screen
        wholesurf = pygame.Surface((radius*2,radius*2))

        total = sum([v[0] for v in values])# get the total value of the stocks
        percentages = [[round((value[0]) / total,4)*100,value[1],value[2]] for value in values]

        other = [0,'Other',(255,255,0)]

        for i in range(len(percentages)-1,-1,-1):
            if percentages[i][0] < 5:# if the percentage is less than 5%, then add it to the ""other"" category
                other[0] += percentages[i][0]
                percentages.remove(percentages[i])

        if other[0] > 0:# if there is an other category, then add it to the list
            percentages.append(other)
        percentages.sort(key=lambda x:x[0],reverse=True)
        percentindex = math.radians(0)
        
        angles = []
        for i,percent in enumerate(percentages):# loop through the percentages and get the angles
            angles.append([math.radians(percentindex)])# the first angle is the previous angle
            percentindex += (percent[0]/100)*360
            angles[i].append(math.radians(percentindex))# the second angle is the current angle
            angles[i].append(percent[1])# the name
            angles[i].append(percent[2])# the color

        corners = [coords, (coords[0] + radius*2, coords[1]), (coords[0] + radius*2, coords[1] + radius*2), (coords[0], coords[1] + radius*2)]
        
        points = []

        for colornum, (a1, a2,name,color) in enumerate(angles):# loop through the angles
            p0 = (coords[0] + radius, coords[1]+radius)
            p1 = (coords[0] + radius + radius * math.cos(a1), radius + coords[1] + (radius * math.sin(a1) * -1))# the first point on the circle
            p2 = (coords[0] + radius + radius * math.cos(a2), radius + coords[1] + (radius * math.sin(a2) * -1))# the second point on the circle - drawn after the corner points
            points = [p0, p1, p2, p0]# put the first points in the list, more points will be added in between p1 and p2

            addedcorners = set()
            a1 = int(math.degrees(a1))
            a2 = int(math.degrees(a2))

            num = int((a1//90)*90)
            modifieddegrees = [(degree+num if degree+num < 360 else degree+num-360) for degree in [0,90,180,270]]# the degrees but shifted so that the first degree (relative to a1) is 0
            for i,degree in enumerate(modifieddegrees):
                # checking the possible cases for when the angle is between the two angles
                if a1 >= degree and a1 < degree+90:
                        addedcorners.add(degree)
                # Next case is for when neither a1 or a2 are in the same quadrant as the degree, but the angle is still between the two angles
                if a1 <= degree:
                    if i != 3 and a2 >= degree+90:
                        addedcorners.add(degree)
                # Next case is for when a2 is in the same quadrant as the degree, but a1 is not
                if a2 >= degree:
                    if a2 <= modifieddegrees[i+1 if i <= 2 else 0]:
                        addedcorners.add(degree)
                    elif modifieddegrees[i+1 if i <= 2 else 0] == 0 and a2 <= 360:
                        addedcorners.add(degree)

            # the corners start at the top left and go clockwise
            # the list below [90,0,270,180] has the corresponding index of the degrees list to the corners list
            dto_corner = lambda degree : corners[[90,0,270,180].index(degree)]
            for degree in addedcorners:
                points.insert(-2,dto_corner(degree))
            # draw the polygon
            pygame.draw.polygon(wholesurf, color, [(x[0]-coords[0],x[1]-coords[1]) for x in points])            


        wholesurf.blit(createbacksurf(radius), (0,0))  # blit the backsurface to the screen
        wholesurf.set_colorkey((0,0,0))
        screen.blit(wholesurf, coords)
        starpos = coords[1]+(((((radius*2))-(len(angles)*30))//2))
        #  drawing the boxes displaying the colors next to the names
        for i, (a1, a2, name,color) in enumerate(angles):
            c = corners[1]
            cx = c[0]
            cy = starpos
            box_x = cx + 10
            box_y = cy + (i * 30)
            box_width = 15
            box_height = 15
            gfxdraw.filled_polygon(screen, [(box_x, box_y), (box_x + box_width, box_y), (box_x + box_width, box_y + box_height), (box_x, box_y + box_height)], color)

        # rendering and blitting the text
        
        renderedtext = [[s_render(f'{name}' if type(name) == str else{f'{name:,.2f}'},35,(255,255,255)),name] for (*_, name,color) in (angles)]
        for i,text in enumerate(renderedtext):
            text_x = cx + 30
            text_y = starpos -5 + (i * 30)
            screen.blit(text[0], (text_x, text_y)) 
        # draw a circle in the middle of the pie chart
        pygame.draw.circle(screen, (0, 0, 0), (coords[0]+radius,coords[1]+radius), radius, 10)
        totaltext = fontlist[45].render(f'${total:,.2f}', (0, 0, 0))[0]
        renderedtext.append([totaltext,f'${total:,.2f}'])
        screen.blit(totaltext, (corners[0][0]+radius-(totaltext.get_width()/2), corners[0][1]+radius-(totaltext.get_height()/2)))
@lru_cache(maxsize=10)
def separate_strings(text:str, lines:int) -> list:
    """Returns list of lines number of equal strings - based on # of chars not words"""
    separated_events = []
    sub_length = len(text) // lines  # approximate length of each string

    for i in range(lines):
        if i >= lines - 1:  # last string
            separated_events.append(text)
        else:  # not last strings
            char_count = 0
            for j, char in enumerate(text):
                char_count += 1
                if char_count >= sub_length and char == ' ':  # don't split words
                    break
            separated_events.append(text[:j])
            text = text[j+1:]  # remove the part of the text that has been separated

    return separated_events

def separate_stringsdict(textdict:dict,lines:int) -> list:
    """Returns separated dict of strings from textlist into (int lines) equal parts"""
    separated_strings = {}
    totallength = lambda stringlist: sum([len(string) for string in stringlist])
    for stock, events in textdict.items(): # stock is the stock name, events is a list of events
        separated_strings[stock] = []
        for event in events: # each event is a string
            separated_events = []
            sub_length = len(event) // lines# approximate length of each string
            words = event.split(' ')
            for i in range(lines):
                removedwords = []
                if i >= lines-1:# last string
                    separated_events.append(' '.join(words))
                else:# not last strings
                    while totallength(removedwords) < sub_length*.9:# add words until the length of the string is greater than the sub_length
                        if not words:
                            break
                        removedwords.append(words.pop(0))
                    separated_events.append(' '.join(removedwords))
            separated_strings[stock].append(separated_events)
    return separated_strings

def movingRect(screen,value,maxvalue,width,height,x,y):
    """Draws the rect that moves with the value"""
    offset = 1 if abs(value) >= maxvalue else abs(value/maxvalue)
    colorval = (120*offset)+70
    color = p3choice((colorval,0,0),(0,colorval,0),(190,190,190),value)

    # Draws the rect that moves with the value

    if value < 0: 
        newx = x-(offset*width*0.5) + width*0.5
        pygame.draw.rect(screen, color, pygame.Rect(newx, y, (0.5*width*offset), height),border_bottom_left_radius=25,border_top_left_radius=25)
    else: 
        pygame.draw.rect(screen, color, pygame.Rect(x+ width*0.5, y, (0.5*width*offset), height),border_bottom_right_radius=25,border_top_right_radius=25)
    
    screen.blit(s_render(f"{'+' if value > 0 else ''}{value:,.3f}%", 55, (0, 0, 0)), (x+width//2-50, y+height//2-20))
    
    # Draws the outline of the rect
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(870,y,740,height), width=7, border_radius=10)

def drawgametime(currenttime,screen:pygame.Surface):
    numtime_text,rect = fontlist[50].render(f'{currenttime[3]}:{"0" if currenttime[4] < 10 else ""}{currenttime[4]}{currenttime[6]}',(255,255,255))
    numtime_rect = numtime_text.get_rect(center=(100, 950))
    polygon_points = [(25, 925), (175, 925), (175, 975), (25, 975)]
    pygame.draw.polygon(screen, (80, 80, 80), polygon_points)
    pygame.draw.polygon(screen, (255, 255, 255), polygon_points, 5)
    pygame.draw.polygon(screen, (0, 0, 0), polygon_points, 1)
    screen.blit(numtime_text, numtime_rect)

def getcolorgrad(percent):
    
    gradpercent = abs(50/(25/percent))# when percent is at 25, it will have max color
    if gradpercent > 50:
        gradpercent = 50

    if percent < 0:
        return (50+gradpercent,50-gradpercent,50-gradpercent)
    elif percent > 0:
        return (50-gradpercent,50+gradpercent,50-gradpercent)
    else:
        return (50,50,50)

def generate_8bit_character(gender='male'):
    width, height = 64, 54
    img = Image.new('RGBA', (width, height), color=(0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    colors = {
        'skin': [(255,214,179), (241,194,125), (224,172,105), (141,85,36)],
        'hair': {
            'male': [(50,30,0), (100,60,0), (0,0,0)],
            'female': [(186,85,211), (255,140,0), (150,75,0), (0,0,0)]
        },
        'shirt': {
            'male': [(0,0,255), (0,100,0), (150,75,0), (100,100,100)],
            'female': [(255,105,180), (255,0,255), (255,192,203), (255,255,0)]
        },
        'eyes': [(0,0,0), (0,100,0), (0,0,100), (100,50,0), (100,0,100)]
    }
    
    def fill_rect(x, y, w, h, color):
        draw.rectangle([x, y, x+w, y+h], fill=color)

    # Draw shirt
    shirt_color = random.choice(colors['shirt'][gender])
    fill_rect(2, 35, width-4, 18, shirt_color)
    
    # Draw neck and face
    skin_tone = random.choice(colors['skin'])
    fill_rect(8, 0, width-16, 35, skin_tone)
    
    # Draw hair
    hair_color = random.choice(colors['hair'][gender])
    if gender == 'male':
        hair_style = random.randint(0, 3)
        if hair_style == 0:  # Short hair
            fill_rect(8, 0, width-16, 6, hair_color)
        elif hair_style == 1:  # Side part
            fill_rect(8, 0, width//2, 6, hair_color)
        elif hair_style == 2: # dot hair
            for i in range(random.randint(0, 25)):
                fill_rect(random.randint(11,width-16), random.randint(1,8), 1, 1, hair_color)
        else:  # Spiked hair
            for i in range(4):
                fill_rect(10+i*12, 0, 8, 8-i*2, hair_color)
               
    else:  # female
        hair_style = random.randint(0, 2)
        if hair_style == 0:  # Long hair
            fill_rect(8, 0, width-16, 12, hair_color)
            fill_rect(6, 12, 4, 23, hair_color)
            fill_rect(width-10, 12, 4, 23, hair_color)
        elif hair_style == 1:  # Ponytail
            fill_rect(8, 0, width-16, 8, hair_color)
            fill_rect(width-14, 8, 6, 27, hair_color)
        else:  # Short bob
            fill_rect(8, 0, width-16, 8, hair_color)
            draw.arc((6, -2, width-6, 12), 0, 180, fill=hair_color, width=4)

    # Draw eyes
    eye_color = random.choice(colors['eyes'])
    eye_style = random.randint(0, 2)
    eye_white = (255, 255, 255)
    
    def draw_eye(x, y):
        if eye_style == 0:  # Round eyes
            fill_rect(x, y, 8, 8, eye_white)
            fill_rect(x+2, y+2, 4, 4, eye_color)
        elif eye_style == 1:  # Oval eyes
            fill_rect(x, y, 8, 6, eye_white)
            fill_rect(x+2, y+1, 4, 4, eye_color)
        else:  # Square eyes
            fill_rect(x, y, 8, 8, eye_white)
            fill_rect(x+2, y+2, 4, 4, eye_color)

    draw_eye(20, 14)
    draw_eye(36, 14)

    # Draw mouth
    mouth_style = random.randint(0, 2)
    if mouth_style == 0:  # Smile
        draw.arc((24, 21, 40, 33), 0, 180, fill=(0,0,0), width=2)
    elif mouth_style == 1:  # Neutral
        fill_rect(24, 30, 16, 2, (0,0,0))
    else:  # Open mouth
        fill_rect(24, 28, 16, 6, (0,0,0))
        fill_rect(26, 30, 12, 2, (200,0,0))  # Tongue
        
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    # return img