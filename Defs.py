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

        colors = [(0, 102, 204),  (255, 0, 0),   (0, 128, 0),    (255, 165, 0),  (255, 215, 0),  (218, 112, 214),(46, 139, 87),  (255, 69, 0),   (0, 191, 255), (128, 0, 128)]

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

# import math
# from scipy.stats import norm
# import numpy as np

# def calculate_option_cost(stock_price, strike_price, time_to_expiration, annualized_volatility, risk_free_rate, option_type="call"):
#     d1 = (math.log(stock_price / strike_price) + (risk_free_rate + 0.5 * (annualized_volatility ** 2)) * time_to_expiration) / (annualized_volatility * math.sqrt(time_to_expiration))
#     d2 = d1 - annualized_volatility * math.sqrt(time_to_expiration)

#     if option_type == "call":
#         option_price = stock_price * norm.cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_expiration) * norm.cdf(d2)
#     elif option_type == "put":
#         option_price = strike_price * math.exp(-risk_free_rate * time_to_expiration) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)
#     else:
#         raise ValueError("Invalid option type. Use 'call' or 'put'.")

#     return option_price


# import numpy as np

# def annualized_volatility(stock_prices):
#     """
#     Calculate the annualized volatility of a stock based on its daily closing prices.

#     Parameters:
#     - stock_prices (list): List of daily closing prices of the stock.

#     Returns:
#     - annualized_volatility (float): Annualized volatility of the stock.
#     """
#     # Normalize prices
#     normalized_prices = np.array(stock_prices) / stock_prices[0]

#     # Calculate daily returns as logarithmic returns
#     log_returns = np.diff(np.log(normalized_prices))

#     # Calculate standard deviation of daily returns
#     daily_volatility = np.std(log_returns)

#     # Annualize the volatility and convert to percentage
#     annualized_volatility = daily_volatility * np.sqrt(252) * 100  # Assuming 252 trading days in a year

#     return annualized_volatility

# # Example usage:
# stock_prices = [6968.671473400675, 7130.065535543774, 7413.781403525257, 7804.211905571063, 7504.192594931716, 6662.6513250357975, 6651.27444480081, 6410.6296061408775, 5917.474287146435, 6245.1338505537005, 5274.899282224345, 5418.906391525891, 4817.254313086428, 4231.81072941926, 4840.2229778030405, 4314.12702144972, 4175.471447850328, 3780.434234360048, 4277.758649447638, 4487.405767871783, 4263.5080782880805, 5103.681568262018, 5233.036999154541, 5863.534525172299, 6667.2167742608, 7401.018816139965, 9198.332279091126, 8910.70919237949, 9100.32066376311, 10961.723147257198, 12840.067206530097, 14714.302335599088, 17701.235358828046, 20066.886896634336, 22904.68829080952, 23355.614296338368, 23362.580500010095, 26453.578546194778, 31265.715486597128, 36648.09126098657, 40328.91159188258, 42591.90263782226, 36733.793066229904, 32479.90265677884, 28041.94237340091, 24182.800884364664, 23835.824565965242, 28593.012747011988, 28773.725723746607, 31659.361917756927, 31624.944653858034, 37367.76835726075, 46742.8957489271, 53084.902119909675, 50091.330266249526, 47894.68273337462, 46342.177750923525, 55778.14889835074, 67329.80661730806, 77653.32735888498, 84034.25730545163, 84705.29911896402, 72632.44776154935, 71694.39824841112, 71307.15412321776, 63929.040310706834, 58254.26814835845, 60096.190143911714, 55794.20725434445, 47266.703416110235, 41677.30792070973, 54382.76060220838, 73171.30688660842, 73871.87077274256, 72864.4163660437, 82018.79553115902, 85073.84093599494, 101645.04559451054, 94288.70373126621, 85568.801953486, 90677.78466019875, 95149.33691819578, 86300.8741739137, 79571.04414915909, 81027.12107689284, 76883.9689450006, 74554.26927680653, 80545.65482198782, 72469.92000261076, 75284.71562800018, 84796.34751394768, 84871.2615377753, 102897.9329097338, 92956.90332257377, 93969.66691886807, 89407.3095219999, 93126.4391035934, 89765.37417589765, 93925.21869443622, 83268.93746613545, 81880.09584328328, 74894.99257663086, 76797.78567392839, 81587.56104687724, 74561.19552869526, 69078.5881610414, 68479.95132560984, 70030.81473291053, 73025.9963540791, 59123.60386420274, 70299.42793521816, 70810.52023505612, 64370.90043337661, 55342.507030752924, 51347.35400384111, 48129.490603574835, 47915.28525679948, 55933.02536704292, 65379.47908856028, 67830.6517713528, 67224.82883902047, 68320.99638164375, 73731.22625468986, 68699.24399509639, 72062.13324120226, 83505.90607222567, 88034.25766776262, 86300.67256049823, 90263.83690938131, 96729.24714038309, 84957.08327476007, 76891.6093465021, 72663.93461339458, 69386.24122072825, 59072.44684128064, 57612.56213574908, 58283.03843705381, 67624.81113676328, 75334.28314206227, 77006.51252857139, 69783.90231797888, 79149.06076130195, 94977.98602958283, 87609.38439271822, 76052.78758286432, 98109.32472869488, 132511.09652388064, 141000.79596083402, 124007.03714419524, 130286.69079665888, 150474.56309303132, 163703.67473820326, 178165.51437135064, 196388.7281981462, 218474.26578975146, 219072.49598746706, 197687.1898567102, 177527.25883324342, 162252.81345111594, 186540.25844513837, 241878.02651100678, 297701.85577262024, 305940.47759020387, 351521.74097633327, 404667.9508040024, 414117.85670367355, 386825.6681092981, 351190.69112617173, 373004.6341035231, 393874.0720087913, 416415.26399850054, 450379.0324946436, 466472.4552874157, 408222.80998102773, 369889.6820126304, 391889.8783033573, 423736.5911029872, 464723.10830442666, 621812.5002380103, 714606.631214622, 872047.9535671985, 1016651.3789869269, 1205089.5303538993, 1487428.5774086732, 1672647.5695822951, 2052938.6831482092, 2259507.355827015, 2473055.76190208, 2623672.558890709, 3023875.72891826, 3571878.100914787, 4052492.852266942, 4709381.786866437, 5260859.856963037, 5967405.459595003, 6856793.483765439, 7843867.689440922, 7376339.097168212, 7786463.801612487, 8155213.04422233]

# volatility = annualized_volatility(stock_prices)
# print(f"Annualized Volatility: {volatility:.4f}%")




# # Scale down the prices for numerical stability
# scale_factor = 1000000
# stock_price = 4709381.786866437 / scale_factor
# strike_price = 5000000 / scale_factor

# time_to_expiration = 10/365  # 6 months
# # annual_volatility = volatility  # This should be estimated from historical data
# annual_volatility = 20000  # This should be estimated from historical data
# risk_free_rate = 0.05  # You should use the actual risk-free rate
# option_type = "call"

# # Calculate the option cost
# option_cost = calculate_option_cost(stock_price, strike_price, time_to_expiration, annualized_volatility, risk_free_rate, option_type)

# # Scale the option cost back up
# option_cost *= scale_factor

# print("Option cost:", f'{option_cost:,.2f}')
