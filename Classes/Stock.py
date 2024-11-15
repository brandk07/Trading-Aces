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
import calendar

@lru_cache(maxsize=20)
def calculate_volatility(points) -> float:
    """Calculate the volatility of a stock, points must be a tuple"""

    if len(points) < 2:
        return .1
    
    prices = np.array(points)

    # Calculate periodic log returns
    returns = np.log(prices[1:] / prices[:-1])

    # Calculate standard deviation of returns (sample standard deviation)
    std_dev = np.std(returns, ddof=1)

    # Number of periods per year (since data spans one year)
    n = len(returns)

    # Annualized volatility
    annualized_volatility = std_dev * np.sqrt(n)

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
        sloganInd = randint(0,len(slogans)-1)
        self.slogan = slogans[sloganInd].replace('\n','')
        self.givenVolatility = sloganInd*15+700
    def getVolatility(self):
        return self.givenVolatility
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

    def __init__(self,name,color,gametime,volatility) -> None:
        self.color,self.name = color,name
        # self.ceo = CEO()
        #variables for graphing the stock 
        #make graphingrangeoptions a dict with the name of the option as the key and the value as the amount of points to show
        self.graphrangeoptions = {"1H":3600,"1D":23_400,"5D":117_000,"1M":491_400,"6M":2_946_000,"1Y":5_896_800,"5Y":29_484_000}
        # self.graphrangeoptions = {"1H":3600,"1D":23_400,"1W":117_000,"1M":491_400,"3M":1_474_200,"1Y":5_896_800,"5Y":29_484_000,"10Y":58_968_000}
        self.condensefacs = {key:value/POINTSPERGRAPH for key,value in self.graphrangeoptions.items()}#the amount of points that each index of the graph has
        # self.graphrange = '1H' # H, D, W, M, 3M, Y
        # self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphs = {key:deque([],maxlen=POINTSPERGRAPH) for key in self.graphrangeoptions.keys()}
        
        self.graphfillvar = {key:0 for key in self.graphrangeoptions.keys()}# used to see when to add a point to a graph
        
        # self.bTrendRanges = [[(-i,i),(100000-(i*8000),500000-(i*41000))] for i in range(12)]

        self.bTrendRanges = [[(-int(i**.9),int(i**.9)),(randint(1,300),randint(301,100000))] for i in range(20)]
        # self.bTrendRanges = [[(i-15,15-i),(randint(1,i*300),randint(i*301,(i**2)*10_000))] for i in range(1,15)]

        # self.bTrendRanges = [[(-i,i),(randint(1,12000),randint(12001,1_500_000))] for i in range(12)]# the ranges for the bonus trends
        # self.bTrendRanges = [[(-i,i),(randint(1,12000),randint(12001,1_500_000))] for i in range(12)]# the ranges for the bonus trends
        self.bTrends = [[randint(*x[0]),randint(*x[1])] for x in self.bTrendRanges]# the trends for the stock

        self.datafromfile(gametime)# Retrieves the data from the file
        self.price = self.graphs[MINRANGE][-1]# the price of the stock at the last graphed point
        # self.dividendYield = 0#
        # self.givenVolatility = self.ceo.getVolatility()
        self.givenVolatility = volatility# volatility that the stock will trend towards, still use getVolatility to calculate the real volatility
        self.recentrenders = {}# a dict of the renders of the recent prices
        self.graph = Graph()
        # print()



    def __str__(self) -> str:
        return f'{self.name}'
    
    def getVolatility(self,graphrange="1Y"):
        return calculate_volatility(tuple(self.graphs[graphrange]))
    
    def updateDividendYield(self,gametime):
        """Updates the dividend percentage 0.02x the percent change from the previous day"""
        
        self.dividendYield += 0.0025*self.getPercentDate(gametime.time-timedelta(days=1),gametime)
        self.dividendYield = max(0,round(self.dividendYield,2))# round and make sure it is not negative
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
        
    def getQuarterReturns(self,quarter:int,gametime:GameTime):
        """Returns the returns of a specific quarter this year"""
        assert quarter in range(1,5), "quarter must be between 0 and 4"
        
        start = datetime(gametime.time.year,3*quarter-2,1)
        
        if start > gametime.time:
            start -= timedelta(days=365)
        end = datetime(gametime.time.year,3*quarter,calendar.monthrange(gametime.time.year, 3*quarter)[1])
        if end > gametime.time and (gametime.time.month-1)//3+1 != quarter:# if the quarter is not the current quarter and the end is after the current date
            end -= timedelta(days=365)
        # if end.month == 12:
        #     end = datetime(gametime.time.year,12,31)
        # print(start,end,gametime.time)
        
        p1 = self.getPointDate(start,gametime)
        p2 = self.getPointDate(end,gametime)
        # print(f"Quarter {quarter} returns are {p2/p1}, p1:{p1}, p2:{p2}, start {3*quarter-2}, end {3*quarter}")
        return ((p2/p1)-1)*100


    def getPercent(self,graphrange="1Y"):
        """Returns the percent change of the stock"""
        assert graphrange in self.graphrangeoptions.keys(), f"graphrange must be a valid key in the graphrangeoptions : {list(self.graphrangeoptions.keys())}"
        return ((self.graphs[graphrange][-1]/self.graphs[graphrange][0])-1)*100
    
    def getPercentDate(self,date:datetime,gametime:GameTime):
        """Returns the percent change from a specific date to today"""
        point = self.getPointDate(date,gametime)
        # print(point,"is the point")
        return ((self.price/point)-1)*100

        
    # def reset_graphs(self):
    #     """resets the graphs to be empty"""
    #     # for i in ["MINRANGE","1D","1W","1M","3M","1Y","trends"]:
    #     newprice = randint(*self.starting_value_range)
    #     for grange in self.graphs.keys():# for each graph range, ["MINRANGE","1D","1W","1M","3M","1Y","trends"], assign the new price to each graph
    #         self.graphs[grange] = np.array([newprice])

    def datafromfile(self,gametime):
        """gets the data from each file and puts it into the graphlist"""
        with open(f'Assets/Stockdata/{self.name}/data.json', 'r')as f:
            data = [json.loads(line) for line in f]

            for i,grange in enumerate(self.graphs.keys()):
                if data[i]:# if the file is not empty
                    # self.graphs[grange] = np.array(data[i])# add the contents to the graphs
                    self.graphs[grange] = deque(data[i],maxlen=POINTSPERGRAPH)
                else:
                    # self.graphs[grange] = np.array([100])# if the file is empty then set the graph to 100
                    self.graphs[grange] = deque([randint(10,800)],maxlen=POINTSPERGRAPH)
            if data[-3] != None and data[-3] != []:
                self.dividendYield = data[-3]# the dividend yield
            else:
                self.dividendYield = randint(0,500)/100# dividend Percentage - starts at a certain amount, every day it is updated each day based how it performed
            if len(data[-2]) > 0:
                self.priceEffects = StockPriceEffects(self,gametime,fileData=data[-2]) 
            else:
                self.priceEffects = StockPriceEffects(self,gametime)

            if len(data[-1]) > 0:
                self.bTrends = data[-1]
            else:
                self.resetTrends()

    def save_data(self):
        with open(f'Assets/Stockdata/{self.name}/data.json','w') as file:
            file.seek(0)  # go to the start of the file
            file.truncate()  # clear the file
            for item in list(self.graphs.values()):
                for i in range(len(item)):
                    item[i] = float(item[i])
                # json_item = json.dumps(item.tolist())  # Convert the list to a JSON string
                json_item = json.dumps(list(item))  # Convert the list to a JSON string
                file.write(json_item + '\n')  # Write the JSON string to the file with a newline character

            file.write(json.dumps(self.dividendYield)+'\n')
            d1 = [d.savingInputs() for d in self.priceEffects.pastReports]
            d2 = [d.savingInputs() for d in self.priceEffects.futureReports]
            file.write(json.dumps([d1,d2])+'\n')

            file.write(json.dumps(self.bTrends))

        

    def addpoint(self, lastprice, multiplier=1,maxstep=MAXSTEP):
        """returns the new price of the stock
        maxstep is the maximum multiplier added to 1 price movement, a lower value will make it more accurate but slower"""
        vol = int(self.givenVolatility+self.priceEffects._modifers["volatility"])# the volatility of the stock
        tempP = self.priceEffects._modifers["priceTrend"]# the temporary price trend
        while multiplier > 0:
            step = multiplier % maxstep if multiplier < maxstep else maxstep# how much to multiply the movement by

            for i, bonustrend in enumerate(self.bTrends):# for each bonus trend
                if bonustrend[1] <= 0:  # if the time is out
                    self.bTrends[i] = [randint(*self.bTrendRanges[i][0]), randint(*self.bTrendRanges[i][1])]
                else:
                    bonustrend[1] -= step

            total_trend = sum(trend[0] for trend in self.bTrends)# the total trend of all the bonus trends
            total_trend += tempP# add the temporary price trend to the total
            highvolitity = vol + total_trend# the highest volitility that the stock can have
            lowvolitity = -vol + total_trend# the lowest volitility that the stock can have
            try:   
                factor = (randint(lowvolitity, highvolitity) / 20_000_000) * step# the factor that the price will be multiplied by
            except:
                raise ValueError(f"Highvolitity: {highvolitity}, Lowvolitity: {lowvolitity}, Total trend: {total_trend}, Volatility: {vol}, Temp Price: {tempP}")
            lastprice = lastprice * (1 + factor)
            multiplier -= step

        return lastprice,step
    
    def resetTrends(self):
        """Sets/resets the trends for the stock"""
        self.bTrends = [[randint(*x[0]),randint(*x[1])] for x in self.bTrendRanges]#resets the trends for each bonus trend
    def resetTrend(self,tIndex):
        """Resets a specific trend"""
        self.bTrends[tIndex] = [randint(*self.bTrendRanges[tIndex][0]),randint(*self.bTrendRanges[tIndex][1])]

    def addPointLong(self,lastprice,distance,condenseFactor):
        """Returns the new price of the stock for really long periods like adding 5 years of points right away"""
        if distance == 0:
            return lastprice
        # print(distance,condenseFactor)
        totalTrend = 0
        emPoints = 0# Emulated points
        while emPoints < distance:
            # First find out how much we need to go in this iteration of the while loop, which trend needs to be reset first
            resetInd,runDistance = min([(i,time) for i,(val,time) in enumerate(self.bTrends)], key=lambda x:x[1])
            runVal = 0
            if runDistance > distance-emPoints:
                runDistance = distance-emPoints
            for i, (val,time) in enumerate(self.bTrends):
                self.bTrends[i][1] -= runDistance
                runVal += val
            self.resetTrend(resetInd)
            totalTrend += runVal*runDistance
            emPoints += runDistance
        totalTrend /= emPoints
        highvolitity = int(totalTrend + self.givenVolatility/distance)# the highest volitility that the stock can have
        lowvolitity = int(totalTrend - self.givenVolatility/distance)# the lowest volitility that the stock can have
        try:
            factor = (randint(lowvolitity, highvolitity) / 20_000_000) * distance# the factor that the price will be multiplied by
        except:
            raise ValueError(f"Highvolitity: {highvolitity}, Lowvolitity: {lowvolitity}, Total trend: {totalTrend}, Volatility: {self.givenVolatility}")
        lastprice = lastprice * (1 + factor)

        return lastprice
                    

        

    def fill_graphs(self):
        
        def getNextLowest(pointsmade):
            
            pointsUntil = []
            for name,points in self.graphs.items():
                """Returns the amount of points needed until the next graph point will come
                Returns (points "distance", name)"""
                # the line below figures out if the amount of points made is greater than the amount of points that the graph can have
                if (diff:=self.graphrangeoptions[MAXRANGE]-self.graphrangeoptions[name]) <= pointsmade+self.condensefacs[MAXRANGE]:
                    # figuring out the amount of points that each index of the graph has
                    condensefactor = self.condensefacs[name]
                    # if the amount of points made is greater than or equal to t he amount of points that the graph can have
                    # if pointsmade-diff >= condensefactor*len(points):
                    #     return name
                    # Diff is the "starting" amount of points that need to be filled before the graph should even be touched
                    # then the condensefactor * len(points) shows how many have been added
                    # Then just find the distance (-) between the two and return the lowest distance
                    pointAmt = min(POINTSPERGRAPH,len(points))
                    distance = (diff+(condensefactor*pointAmt))-pointsmade
                    # print(distance,name,diff,condensefactor*len(points),pointsmade)
                    
                    # print(f"Diff : {diff:,.2f}, Name: {name}, Dis: {distance:,.2f} mulit : {condensefactor*pointAmt:,.2f}, pointsm : {pointsmade:,.2f}")
                    if distance >= 0:
                        pointsUntil.append((distance,name))
            # print(pointsUntil)
            return min(pointsUntil,key=lambda x:x[0])

        # self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}# reset the graphs
        self.graphs = {key:deque([],maxlen=POINTSPERGRAPH) for key in self.graphrangeoptions.keys()}
        # self.graphs[MAXRANGE] = np.array([self.price])
        self.graphs[MAXRANGE] = deque([self.price],maxlen=POINTSPERGRAPH)
        lastgraphed = MAXRANGE
        pointsmade = 0
        while len(self.graphs[MINRANGE]) < POINTSPERGRAPH:
            distance,name = getNextLowest(pointsmade)
            # print(distance,name,self.graphs[name].size)

            newpoint = self.addPointLong(self.graphs[lastgraphed][-1],distance,self.condensefacs[name])
            lastgraphed = name
            # self.graphs[name] = np.append(self.graphs[name],newpoint)
            self.graphs[name].append(newpoint)
            pointsmade += distance
        
        self.price = self.graphs[MINRANGE][-1]
        

    # def fill_graphs(self):
    #     def get_lowestgraph(pointsmade):
    #         for name,points in self.graphs.items():
    #             """Returns the name of the lowest graph that should get points added to it"""
    #             # the line below figures out if the amount of points made is greater than the amount of points that the graph can have
    #             if (diff:=self.graphrangeoptions["5Y"]-self.graphrangeoptions[name]) <= pointsmade:
    #                 # figuring out the amount of points that each index of the graph has
    #                 condensefactor = self.condensefacs[name]
    #                 # if the amount of points made is greater than or equal to the amount of points that the graph can have
    #                 if pointsmade-diff >= condensefactor*len(points):
    #                     return name

    #     self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}# reset the graphs

    #     lastgraphed = ""
    #     pointsmade = 0
    #     while len(self.graphs['1H']) < POINTSPERGRAPH:
    #         newgraphed = get_lowestgraph(pointsmade)# gets the name of the lowest graph that should get points added to it
    #         if newgraphed == None:# if there is no graph that needs points added to it for the amount of points made
    #             pointsmade += 1# advance pointsmade until there is a graph that needs points added to it
    #             continue
    #         if self.graphs[newgraphed].size == 0:# if the graph is empty
    #             if lastgraphed == "":# if there is no last graphed (Only used for the year graph)
    #                 self.graphs[newgraphed] = np.array([self.price],dtype=object)
    #             else:# this is when the first point is added to a graph after the year graph
    #                 self.graphs[newgraphed] = np.append(self.graphs[newgraphed],self.graphs[lastgraphed][-1])

    #         lastgraphed = newgraphed
    #         multiplier = int(self.graphrangeoptions[lastgraphed]/POINTSPERGRAPH)
            
    #         newpoint = self.addpoint(self.graphs[lastgraphed][-1],multiplier,maxstep=100)

    #         for name,points in self.graphs.items():# for each graph
    #             if (diff:=self.graphrangeoptions["5Y"]-self.graphrangeoptions[name]) <= pointsmade:# figures out if the amount of pointsmade is greater than the amount of points that the graph can have
    #                 condensefactor = self.condensefacs[name]
    #                 if pointsmade-diff >= condensefactor*len(points):
    #                     self.graphs[name] = np.append(self.graphs[name],newpoint)

    #         pointsmade += multiplier
    #     self.price = self.graphs['1H'][-1]

    def update_range_graphs(self,stockvalues=0,step=1):

        for key in self.graphrangeoptions:
            condensefactor = self.condensefacs[key]
            for i in range(step):
                self.graphfillvar[key] += 1
                if self.graphfillvar[key] == int(condensefactor):#if enough points have passed to add a point to the graph (condensefactor is how many points must go by to add 1 point to the graph)
                    #add the last point to the list
                    self.graphfillvar[key] = 0
                    if type(self) == Stock:
                        # self.graphs[key] = np.append(self.graphs[key],self.price)
                        self.graphs[key].append(self.price)
                    else:
                        # self.graphs[key] = np.append(self.graphs[key],stockvalues)
                        self.graphs[key].append(stockvalues)
            
            # if len(self.graphs[key]) > POINTSPERGRAPH:
            #     # print('deleting',key,len(self.graphs[key]))
            #     self.graphs[key] = np.delete(self.graphs[key],0)

    def update_price(self,gamespeed,PlayerClass,step=1):
        # if self.bankrupcy(False):#if stock is not bankrupt
        #     pass
        
        if type(self) == Stock:#making sure that it is a Stock object and that update is true
            self.price,step = self.addpoint(self.price,multiplier=gamespeed)#updates the price of the stock
            # self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable
            for _ in range(0,gamespeed,step):
                self.update_range_graphs(step=step)
            # for _ in range(gamespeed):
            #     self.update_range_graphs()
            self.price = self.graphs[MINRANGE][-1]
            return step
        elif type(self) == PlayerClass:# if Player object

            # stockvalues = sum([stock[0].price*stock[2] for stock in self.stocks])
            self.price = self.getNetworth()
            # for _ in range(gamespeed):
            for _ in range(0,gamespeed,step):
                self.update_range_graphs(self.getNetworth(),step=step)#updates the range graphs
    
