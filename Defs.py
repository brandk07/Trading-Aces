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
        print(data)
        if data:
            player.stocks = [[stock[0],stock[1],stockdict[stock[0]]] for stock in data[1]]#[name,price,obj] can't save the object so I save the name and use that to get the object
            player.graphrange = data[2]
            player.cash = data[3] if data[3] != 0 else 2500
            for i,stockobj in enumerate(stockdict.values()):
                stockobj.graphrange = data[i+4]
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
    
# fonts = lambda font_size: pygame.font.SysFont(r'Assets/antonio/Antonio-Regular.ttf',font_size)
# fonts = lambda font_size: pygame.font.SysFont(r'Assets/antonio/Antonio-Bold.ttf',font_size)

fonts = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Regular.ttf', font_size*.75)
fontsbold = lambda font_size: freetype.Font(r'Assets\fonts\antonio\Antonio-Bold.ttf', font_size*.75)


# FUN THEME
# fonts = lambda font_size: freetype.Font(r'Assets\fonts\Bangers\Bangers-Regular.ttf', font_size*.75)
# fontsbold = lambda font_size: freetype.Font(r'Assets\fonts\Bangers\Bangers-Regular.ttf', font_size*.75)

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

