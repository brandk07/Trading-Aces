import pygame
from random import randint
from pygame import gfxdraw
from Defs import *
import numpy as np
import json
from Classes.imports.Graph import Graph
from datetime import datetime,timedelta
from Classes.Gametime import GameTime
import math
from Classes.StockVisualizer import StockVisualizer,POINTSPERGRAPH
from functools import lru_cache
from faker import Faker
from Classes.StockPriceEffects import StockPriceEffects

@lru_cache(maxsize=20)
def calculate_volatility(points) -> float:
    """Calculate the volatility of a stock, points must be a tuple"""

    if len(points) < 2:
        return .1
    
    # Calculate daily returns
    returns = np.diff(points) / points[:-1]

    # Calculate standard deviation of daily returns
    daily_volatility = np.std(returns)

    # Annualize volatility
    annualized_volatility = np.sqrt(252) * daily_volatility

    return annualized_volatility
fake = Faker()
with open(r'Assets\ceoSlogans.txt','r') as file:
    slogans = file.readlines()
class CEO():
    def __init__(self) -> None:
        gender = ['male','female'][randint(0,1)]

        self.name = fake.name_female() if gender == 'female' else fake.name_male()
        self.age = randint(30,70)
        self.image = generate_8bit_character(gender)
        self.image = pygame.transform.scale(self.image,(100,100))
        self.slogan = slogans[randint(0,len(slogans)-1)].replace('\n','')

    @lru_cache(maxsize=5)
    def getSloganLines(self,lines):
        """Returns the slogan of the CEO with the amount of lines specified"""
        return separate_strings(self.slogan,lines)
    @lru_cache(maxsize=5)
    def getImageSize(self,xSize,ySize):
        """Returns the image of the CEO with the size of xSize and ySize"""	
        return pygame.transform.scale(self.image,(xSize,ySize)) 
    def addYears(self,years):
        self.age += years
        return self.age


class Stock():
    """Class contains the points and ability to modify the points of the stock
    an object of stockVisualizer is created to visualize the stock"""

    def __init__(self,name,volatility,color,gametime) -> None:
        self.color,self.name = color,name
        self.ceo = CEO()
        #variables for graphing the stock 
        #make graphingrangeoptions a dict with the name of the option as the key and the value as the amount of points to show
        self.graphrangeoptions = {"1H":3600,"1D":23_400,"1W":117_000,"1M":491_400,"3M":1_474_200,"1Y":5_896_800}
        self.condensefacs = {key:value/POINTSPERGRAPH for key,value in self.graphrangeoptions.items()}#the amount of points that each index of the graph has
        # self.graphrange = '1H' # H, D, W, M, 3M, Y
        self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphfillvar = {key:0 for key in self.graphrangeoptions.keys()}# used to see when to add a point to a graph
        
        # self.bonustrendranges = [[(-1*i,i),(100000-(i*8325),500000-(i*41400))] for i in range(12)]
        self.bonustrendranges = [[(-i,i),(randint(1,12000),randint(12001,1_500_000))] for i in range(12)]
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]

        self.datafromfile()# Retrieves the data from the file
        self.price = self.graphs['1H'][-1]# the price of the stock at the last graphed point
        self.dividend = 0
        self.volatility = volatility
        self.recentrenders = {}# a dict of the renders of the recent prices
        self.priceEffects = StockPriceEffects(self,gametime)
        self.graph = Graph()
        # print()
    

    def __str__(self) -> str:
        return f'{self.name}'
    
    def getVolatility(self,graphrange="1Y"):
        return calculate_volatility(tuple(self.graphs[graphrange]))
    
    def getValue(self):
        """Returns the price of the stock"""
        return self.price
    
    def getPoint(self,graphrange,ind):
        """Returns the point at a specific index"""
        return self.graphs[graphrange][ind]
    
    # @lru_cache(maxsize=10)
    def getPointDate(self,date:datetime,gametime:GameTime):
        assert isinstance(date,datetime), "date must be a datetime object"
        assert isinstance(gametime,GameTime), "gametime must be a GameTime object"
        def getNumTradingDays(date1:datetime,date2:datetime):
            """Returns the number of trading days between two dates"""
            diff2 = (date2-date1)
            days = diff2.days
            if days < 0:
                return 0
            tradingsecs = 0
            date1 = datetime.strptime(f"{date1.month}/{date1.day}/{date1.year} 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p")
            # print(f"Num days is {days}")
            for i in range(days):
                # print(f"i is {i}, date is {date1+timedelta(days=i)}, {gametime.isOpen(date1+timedelta(days=i))}, tradingsecs is {tradingsecs}")
                # if (day:=date1+timedelta(days=i)).weekday() < 5:
                if gametime.isOpen(date1+timedelta(days=i))[0]:
                    
                    tradingsecs += 3600*6.5
            date1 = datetime.strptime(f"{date2.month}/{date2.day}/{date2.year} {date1.hour}:{date1.minute}:{date1.second} AM", "%m/%d/%Y %I:%M:%S %p")
            diff2 = (date2-date1).seconds

            # print(diff2+tradingsecs)
            return diff2 + tradingsecs
        def getClosestDate(secondsAgo):
            """Returns the point closest to the number of seconds ago a date was"""
            
            # ranges = [3600,23_400,604_800,2_592_000,7_776_000,31_104_000]
            if secondsAgo > 23_400:# if more than 1 trading day has passed
                secondsAgo = getNumTradingDays(date,gametime.time)

            key = list(self.graphrangeoptions)[-1]# sets it to the last key	"1Y"
            for k,value in (self.graphrangeoptions.items()):
                if value > secondsAgo:
                    key = k
                    break
            secondsPerPoint = self.graphrangeoptions[key]/POINTSPERGRAPH
            # Have to multiply by the weird number because the graphrangeoption only takes trading day seconds
            # The one below counts all seconds so the number is an approximate trading day seconds to total seconds
            closestIndex = POINTSPERGRAPH-math.ceil((secondsAgo)/secondsPerPoint)+1# Finding the closet Index
            if closestIndex >= len(self.graphs[key]):
                closestIndex = len(self.graphs[key])-1
            if closestIndex < -len(self.graphs[key]):
                closestIndex = 0
            # print(closestIndex,key,len(self.graphs[key]))
            # print(closestIndex,key,"is the closest index")

            return self.graphs[key][closestIndex]
        
        diff = gametime.time-date
        return getClosestDate(diff.total_seconds())
        
    def resetTrends(self):
        """Sets/resets the trends for the stock"""
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]#resets the trends for each bonus trend

    def getPercent(self,graphrange="1Y"):
        """Returns the percent change of the stock"""
        return ((self.graphs[graphrange][-1]/self.graphs[graphrange][0])-1)*100
    
    def getPercentDate(self,date:datetime,gametime:GameTime):
        """Returns the percent change from a specific date to today"""
        point = self.getPointDate(date,gametime)
        # print(point,"is the point")
        return ((self.price/point)-1)*100

        
    def reset_graphs(self):
        """resets the graphs to be empty"""
        # for i in ["1H","1D","1W","1M","3M","1Y","trends"]:
        newprice = randint(*self.starting_value_range)
        for grange in self.graphs.keys():# for each graph range, ["1H","1D","1W","1M","3M","1Y","trends"], assign the new price to each graph
            self.graphs[grange] = np.array([newprice])

    def datafromfile(self):
        """gets the data from each file and puts it into the graphlist"""
        with open(f'Assets/Stockdata/{self.name}/data.json', 'r')as f:
            data = [json.loads(line) for line in f]

            for i,grange in enumerate(self.graphs.keys()):
                if data[i]:# if the file is not empty
                    self.graphs[grange] = np.array(data[i])# add the contents to the graphs
                else:
                    self.graphs[grange] = np.array([100])# if the file is empty then set the graph to 100
            if len(data[-1]) > 0:
                self.bonustrends = data[-1]
            else:
                self.resetTrends()

    def save_data(self):
        with open(f'Assets/Stockdata/{self.name}/data.json','w') as file:
            file.seek(0)  # go to the start of the file
            file.truncate()  # clear the file
            for item in list(self.graphs.values()):
                for i in range(len(item)):
                    item[i] = float(item[i])
                json_item = json.dumps(item.tolist())  # Convert the list to a JSON string
                file.write(json_item + '\n')  # Write the JSON string to the file with a newline character
            
            file.write(json.dumps(self.bonustrends))
        

    def addpoint(self, lastprice, multiplier=1,maxstep=25):
        """returns the new price of the stock
        maxstep is the maximum multiplier added to 1 price movement, a lower value will make it more accurate but slower"""
        vol = int(self.volatility+self.priceEffects._modifers["volatility"])# the volatility of the stock
        tempP = self.priceEffects._modifers["priceTrend"]# the temporary price trend
        while multiplier > 0:
            step = multiplier % maxstep if multiplier < maxstep else maxstep# how much to multiply the movement by

            for i, bonustrend in enumerate(self.bonustrends):# for each bonus trend
                if bonustrend[1] <= 0:  # if the time is out
                    self.bonustrends[i] = [randint(*self.bonustrendranges[i][0]), randint(*self.bonustrendranges[i][1])]
                else:
                    bonustrend[1] -= step

            total_trend = sum(trend[0] for trend in self.bonustrends)# the total trend of all the bonus trends
            total_trend = total_trend if total_trend >= 0 else -1 * (total_trend // 2)# if the total trend is negative, then divide it by 2
            total_trend += tempP# add the temporary price trend to the total
            highvolitity = vol + total_trend# the highest volitility that the stock can have
            lowvolitity = -vol + total_trend# the lowest volitility that the stock can have
            
            factor = (randint(lowvolitity, highvolitity) / 500_000) * step# the factor that the price will be multiplied by
            lastprice = lastprice * ((1 + factor) if randint(0, 1) else (1 - factor))  # returns the new price of the stock
            multiplier -= step

        return lastprice
    
    def fill_graphs(self):
        def get_lowestgraph(pointsmade):
            for name,points in self.graphs.items():
                """Returns the name of the lowest graph that should get points added to it"""
                # the line below figures out if the amount of points made is greater than the amount of points that the graph can have
                if (diff:=self.graphrangeoptions["1Y"]-self.graphrangeoptions[name]) <= pointsmade:
                    # figuring out the amount of points that each index of the graph has
                    condensefactor = self.condensefacs[name]
                    # if the amount of points made is greater than or equal to the amount of points that the graph can have
                    if pointsmade-diff >= condensefactor*len(points):
                        return name

        self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}# reset the graphs

        lastgraphed = ""
        pointsmade = 0
        while len(self.graphs['1H']) < POINTSPERGRAPH:
            newgraphed = get_lowestgraph(pointsmade)# gets the name of the lowest graph that should get points added to it
            if newgraphed == None:# if there is no graph that needs points added to it for the amount of points made
                pointsmade += 1# advance pointsmade until there is a graph that needs points added to it
                continue
            if self.graphs[newgraphed].size == 0:# if the graph is empty
                if lastgraphed == "":# if there is no last graphed (Only used for the year graph)
                    self.graphs[newgraphed] = np.array([self.price],dtype=object)
                else:# this is when the first point is added to a graph after the year graph
                    self.graphs[newgraphed] = np.append(self.graphs[newgraphed],self.graphs[lastgraphed][-1])

            lastgraphed = newgraphed
            multiplier = int(self.graphrangeoptions[lastgraphed]/POINTSPERGRAPH)
            
            newpoint = self.addpoint(self.graphs[lastgraphed][-1],multiplier)

            for name,points in self.graphs.items():# for each graph
                if (diff:=self.graphrangeoptions["1Y"]-self.graphrangeoptions[name]) <= pointsmade:# figures out if the amount of pointsmade is greater than the amount of points that the graph can have
                    condensefactor = self.condensefacs[name]
                    if pointsmade-diff >= condensefactor*len(points):
                        self.graphs[name] = np.append(self.graphs[name],newpoint)

            pointsmade += multiplier
        self.price = self.graphs['1H'][-1]

    def update_range_graphs(self,stockvalues=0):
        
        for key in self.graphrangeoptions:
            condensefactor = self.condensefacs[key]
            self.graphfillvar[key] += 1
            if self.graphfillvar[key] == int(condensefactor):#if enough points have passed to add a point to the graph (condensefactor is how many points must go by to add 1 point to the graph)
                #add the last point to the list
                self.graphfillvar[key] = 0
                if type(self) == Stock:
                    self.graphs[key] = np.append(self.graphs[key],self.price)
                else:
                    self.graphs[key] = np.append(self.graphs[key],stockvalues)
            
            if len(self.graphs[key]) > POINTSPERGRAPH:
                # print('deleting',key,len(self.graphs[key]))
                self.graphs[key] = np.delete(self.graphs[key],0)

    def update_price(self,gamespeed,PlayerClass):
        # if self.bankrupcy(False):#if stock is not bankrupt
        #     pass
        
        if type(self) == Stock:#making sure that it is a Stock object and that update is true
            self.price = self.addpoint(self.price,multiplier=gamespeed,maxstep=5)#updates the price of the stock
            # self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable
            for _ in range(gamespeed):
                self.update_range_graphs()
            self.price = self.graphs["1H"][-1]
        elif type(self) == PlayerClass:# if Player object

            # stockvalues = sum([stock[0].price*stock[2] for stock in self.stocks])
            self.price = self.getNetworth()
            for _ in range(gamespeed):
                self.update_range_graphs(self.getNetworth())#updates the range graphs
    
