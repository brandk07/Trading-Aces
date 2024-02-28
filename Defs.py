import pygame,time
from pygame import gfxdraw,freetype
import os,re,random,json,math,timeit
from collections import deque
from Classes.AssetTypes.OptionAsset import OptionAsset
from Classes.AssetTypes.StockAsset import StockAsset
import numpy as np
from functools import lru_cache 
pygame.font.init()
pygame.mixer.init()
pygame.init()


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
        return result
    return wrapper

#  ////////////////////////////////////////////Fonts///////////////////////////////////////////////////////////////////////////////////////
fonts = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Regular.ttf', font_size*.75)
crystalfonts = lambda font_size: freetype.Font(r'Assets\fonts\LiquidCrystal\Liquid_Crystal_Extra_Characters.otf', font_size*.75)
pixfonts = lambda font_size: freetype.Font(r'Assets\fonts\Silkscreen\Silkscreen-Regular.ttf', font_size*.75)
fontsbold = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Bold.ttf', font_size*.75)
# FUN THEME
# fonts = lambda font_size: freetype.Font(r'Assets\fonts\Bangers\Bangers-Regular.ttf', font_size*.75)
# fontsbold = lambda font_size: freetype.Font(r'Assets\fonts\Bangers\Bangers-Regular.ttf', font_size*.75)
# fonts = lambda font_size: freetype.Font(r'Assets\antonio\Liquid_Crystal_Extra_Characters.otf', font_size)
bold40 = fontsbold(45)
fontlist = [fonts(num) for num in range(0,201)]#list of fonts from 0-100
fontlistcry = [crystalfonts(num) for num in range(0,201)]#list of fonts from 0-100
fontlistpix = [pixfonts(num) for num in range(0,201)]#list of fonts from 0-100
font45 = fonts(45)

@lru_cache(maxsize=100)
def s_render(string:str, size, color,font='reg') -> pygame.Surface:
    """Caches the renders of the strings, and returns the rendered surface"""
    # print(f"Caching arguments: {string}, {size}, {color}")
    if font == 'reg':
        text = fontlist[size].render(string, (color))[0]
    elif font == 'cry':
        text = fontlistcry[size].render(string, (color))[0]
    return text
#  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

soundEffects = {
    'clickbutton': pygame.mixer.Sound(r'Assets\Soundeffects\clickbutton.wav'),
    'clickbutton2': pygame.mixer.Sound(r'Assets\Soundeffects\clickbutton2.wav'),
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

percentColor = lambda negative, positive, zero, change : negative if change < 0 else positive if change > 0 else zero

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
                soundEffects['clickbutton2'].play()
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
def limit_digits(num, max_digits, floater=True) -> str:
    if len("{:,.2f}".format(num)) > max_digits:
        return "{:,.2e}".format(num)    
    else:
        return f"{num:,.2f}" if floater else f"{int(num)}"
def time_loop(loop):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        for item in loop:
            result = item(*args, **kwargs)
        end_time = time.time()
        print(f"Loop took {end_time - start_time:.5f} seconds to execute.")
        return result
    return wrapper

def Getfromfile(stockdict:dict,player,gametime):
    with open('Assets/Stockdata/extradata.json','r') as file:
        data = json.load(file)
        print(data)
        if data:
            gametime.setTimeStr(data[0])
            # player.stocks = [[stockdict[stock[0]],stock[1],stock[2]] for stock in data[1]]#[name,price,obj] can't save the object so I save the name and use that to get the object
            # print(data[1])
            player.stocks = [StockAsset(stockdict[stock[0]],stock[1],stock[2],stock[3]) for stock in data[1]]# [stockobj,creationdate,ogprice,quantity]
            player.options = [OptionAsset(stockdict[option[0]],option[1],option[2],option[3],option[4],quantity=option[5],ogprice=option[6],color=tuple(option[7])) for option in data[2]]# options storage is [stockname,strikeprice,expirationdate,optiontype,quantity,ogprice]
            player.graphrange = data[3]
            player.cash = data[4] if data[4] != 0 else 2500
            musicdata = (data[5])
            for i,stockobj in enumerate(stockdict.values()):
                stockobj.graphrange = data[i+6]
            return musicdata
        return [0,0,0]# time, volume, songindex

def Writetofile(stocklist,player,data):
    for stock in stocklist:
        stock.save_data()
    player.save_data()
    
    with open('Assets/Stockdata/extradata.json','w') as file:
        file.seek(0)# go to the start of the file
        file.truncate()# clear the file
        json.dump(data,file)

def closest_point(master_point, points):
    return min(points, key=lambda point: math.sqrt((point[0] - master_point[0])**2 + (point[1] - master_point[1])**2))


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

def drawgametime(currenttime,screen:pygame.Surface):
    numtime_text,rect = fontlist[50].render(f'{currenttime[3]}:{"0" if currenttime[4] < 10 else ""}{currenttime[4]}{currenttime[6]}',(255,255,255))
    numtime_rect = numtime_text.get_rect(center=(100, 950))
    polygon_points = [(25, 925), (175, 925), (175, 975), (25, 975)]
    pygame.draw.polygon(screen, (80, 80, 80), polygon_points)
    pygame.draw.polygon(screen, (255, 255, 255), polygon_points, 5)
    pygame.draw.polygon(screen, (0, 0, 0), polygon_points, 1)
    screen.blit(numtime_text, numtime_rect)

def getcolorgrad(percent):
    
    gradpercent = abs(50/(25/percent))# when perecent is at 25, it will have max color
    if gradpercent > 50:
        gradpercent = 50

    if percent < 0:
        return (50+gradpercent,50-gradpercent,50-gradpercent)
    elif percent > 0:
        return (50-gradpercent,50+gradpercent,50-gradpercent)
    else:
        return (50,50,50)