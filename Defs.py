import pygame
import time
from pygame import gfxdraw
from pygame import freetype
import math
import json
import random
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
def limit_digits(num, max_digits,floater=True):
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
pygame.init()
def Getfromfile(stockdict:dict,player):
    with open('Assets/Stockdata/extradata.json','r') as file:
        data = json.load(file)
        print(data)
        if data:
            player.stocks = [[stockdict[stock[0]],stock[1],stock[2],] for stock in data[1]]#[name,price,obj] can't save the object so I save the name and use that to get the object
            player.graphrange = data[2]
            player.cash = data[3] if data[3] != 0 else 2500
            for i,stockobj in enumerate(stockdict.values()):
                stockobj.graphrange = data[i+4]

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

def draw_pie_chart(screen: pygame.Surface, values:list, radius, coords, backsurface=None, renderedtext=None):
        """Draws the pie chart for the portfolio menu. value is (value, name)"""

        # get the total value of the stocks
        total = sum([v[0] for v in values])
        percentages = [[round((value[0]) / total,4)*100,value[1]] for value in values]

        other = [0,'Other']

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
            angles[i].append(percent[1])

        corners = [coords, (coords[0] + radius*2, coords[1]), (coords[0] + radius*2, coords[1] + radius*2), (coords[0], coords[1] + radius*2)]
        
        points = []

        colors = [(0, 102, 204),  (255, 0, 0),    (0, 128, 0),    (255, 165, 0),  (255, 215, 0),  (218, 112, 214),(46, 139, 87),  (255, 69, 0),   (0, 191, 255)]

        for colornum, (a1, a2,name) in enumerate(angles):# loop through the angles
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
                    if i != 3 and a2 >= modifieddegrees[i+1 if i <= 2 else 0]:
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
            pygame.draw.polygon(screen, colors[colornum], points)            

        if backsurface == None:  # if the backsurface is not none, then draw the circle on the backsurface
            backsurface = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
            backsurface.fill((40, 40, 40))
            pygame.draw.circle(backsurface, (255, 255, 255), (radius, radius), radius)
            backsurface.set_colorkey((255, 255, 255))

        screen.blit(backsurface, coords)  # blit the backsurface to the screen

        starpos = coords[1]+(((((radius*2))-(len(angles)*30))//2))
        #  drawing the boxes displaying the colors next to the names
        for i, (a1, a2, name) in enumerate(angles):
            c = corners[1]
            cx = c[0]
            cy = starpos
            box_x = cx + 10
            box_y = cy + (i * 30)
            box_width = 15
            box_height = 15
            gfxdraw.filled_polygon(screen, [(box_x, box_y), (box_x + box_width, box_y), (box_x + box_width, box_y + box_height), (box_x, box_y + box_height)], colors[i])
       
        # rendering and blitting the text
        if renderedtext == None or len(renderedtext) != len(angles)+1 or [name for (*_, name) in (angles)] != [name for (_, name) in (renderedtext)] or renderedtext[-1][1] != f'${total:,.2f}':
            renderedtext = [[fontlist[35].render(f'{name}' if type(name) == str else{f'{name:,.2f}'}, (255, 255, 255))[0],name] for (*_, name) in (angles)]
        for i,text in enumerate(renderedtext):
            text_x = cx + 30
            text_y = starpos -5 + (i * 30)
            screen.blit(text[0], (text_x, text_y)) 
        # draw a circle in the middle of the pie chart
        pygame.draw.circle(screen, (0, 0, 0), (coords[0]+radius,coords[1]+radius), radius, 10)
        totaltext = fontlist[45].render(f'${total:,.2f}', (0, 0, 0))[0]
        renderedtext.append([totaltext,f'${total:,.2f}'])
        screen.blit(totaltext, (corners[0][0]+radius-(totaltext.get_width()/2), corners[0][1]+radius-(totaltext.get_height()/2)))

        return backsurface,renderedtext


    
# fonts = lambda font_size: pygame.font.SysFont(r'Assets/antonio/Antonio-Regular.ttf',font_size)
# fonts = lambda font_size: pygame.font.SysFont(r'Assets/antonio/Antonio-Bold.ttf',font_size)

fonts = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Regular.ttf', font_size*.75)
crystalfonts = lambda font_size: freetype.Font(r'Assets\fonts\LiquidCrystal\Liquid_Crystal_Extra_Characters.otf', font_size*.75)
pixfonts = lambda font_size: freetype.Font(r'Assets\fonts\Silkscreen\Silkscreen-Regular.ttf', font_size*.75)
fontsbold = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Bold.ttf', font_size*.75)


# FUN THEME
# fonts = lambda font_size: freetype.Font(r'Assets\fonts\Bangers\Bangers-Regular.ttf', font_size*.75)
# fontsbold = lambda font_size: freetype.Font(r'Assets\fonts\Bangers\Bangers-Regular.ttf', font_size*.75)

# fonts = lambda font_size: freetype.Font(r'Assets\antonio\Liquid_Crystal_Extra_Characters.otf', font_size)
bold40 = fontsbold(45)

fontlist = [fonts(num) for num in range(0,100)]#list of fonts from 0-100
fontlistcry = [crystalfonts(num) for num in range(0,100)]#list of fonts from 0-100
fontlistpix = [pixfonts(num) for num in range(0,100)]#list of fonts from 0-100
    
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

import math
from scipy.stats import norm

def calculate_option_cost(stock_price, strike_price, time_to_expiration, annualized_volatility, risk_free_rate, option_type="call"):
    d1 = (math.log(stock_price / strike_price) + (risk_free_rate + 0.5 * (annualized_volatility ** 2)) * time_to_expiration) / (annualized_volatility * math.sqrt(time_to_expiration))
    d2 = d1 - annualized_volatility * math.sqrt(time_to_expiration)

    if option_type == "call":
        option_price = stock_price * norm.cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_expiration) * norm.cdf(d2)
    elif option_type == "put":
        option_price = strike_price * math.exp(-risk_free_rate * time_to_expiration) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    return option_price

# Example usage:
stock_price = 1_200_000
strike_price = 860_000
time_to_expiration = 10/365  # 6 months
annualized_volatility = 15.99  # This should be estimated from historical data
risk_free_rate = 0.06  # You should use the actual risk-free rate
option_type = "call"

option_cost = calculate_option_cost(stock_price, strike_price, time_to_expiration, annualized_volatility, risk_free_rate, option_type)
# print("Option cost:", option_cost)

import numpy as np

def calculate_annualized_volatility(price_data, trading_days_per_year=365):
    # Calculate daily returns
    daily_returns = np.diff(price_data) / price_data[:-1]

    # Calculate standard deviation of daily returns
    daily_std = np.std(daily_returns)

    # Annualize the standard deviation
    annualized_volatility = daily_std * np.sqrt(trading_days_per_year)

    return annualized_volatility

# Example usage:
price_data = [1263.0064999998863, 1296.4364999999125, 1284.909499999904, 1328.7544999999, 1324.6864999998988, 1312.403499999877, 1137.8284999998782, 1144.5774999998825, 1173.592499999885, 1184.5214999998987, 1230.8284999999091, 1136.2034999999044, 1147.3954999999162, 1128.3484999999205, 1025.9274999999259, 999.9074999999206, 999.5964999999167, 989.7404999999108, 995.556499999908, 985.6024999999092, 1111.8294999999216, 1182.081499999892, 1061.86549999989, 1132.3344999998708, 1203.6704999998917, 1219.2274999998924, 1182.3634999998942, 1174.5984999998866, 1308.0744999998947, 1236.4314999998876, 1143.6334999999021, 1074.2474999998844, 1026.4574999998915, 1061.7534999998857, 947.0334999998893, 1020.4744999998893, 992.8774999998683, 1004.3064999998672, 944.6554999998724, 786.972499999869, 824.241499999869, 856.7654999998674, 762.2634999998727, 641.722499999863, 622.5464999998687, 578.930499999874, 644.1104999998868, 562.5554999998766, 571.6374999998762, 631.211499999873, 570.5194999998806, 589.6764999998791, 453.8184999998789, 397.07249999988085, 331.78849999988125, 312.88849999987866, 417.1824999998766, 517.1004999998823, 457.1814999998794, 407.097499999882, 347.836499999883, 376.6824999998868, 410.4104999998855, 452.5844999998872, 258.7924999998853, 268.0674999998863, 268.16149999988335, 150.3184999998818, 122.24849999988164, 125.83449999988208, 204.54449999988157, 223.36749999988433, 330.6184999998857, 298.45649999988575, 284.4124999998849, 316.962499999884, 328.1324999998822, 452.10049999988496, 378.48449999988713, 371.11749999988825, 386.22849999988955, 427.5154999998871, 299.27849999988723, 276.3034999998858, 239.8694999998822, 199.48549999988225, 187.67049999988248, 181.93449999988226, 89.27049999988279, 79.01749999988301, 66.70849999988435, 613.2989999999994, 638.2389999999991, 674.8589999999961, 549.7760000000056, 466.75500000000744, 467.0880000000058, 369.99600000000646, 390.23900000000924, 221.95000000000667]
volatility = calculate_annualized_volatility(price_data)
# print("Annualized Volatility:", volatility)

