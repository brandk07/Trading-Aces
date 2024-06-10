import pygame
from random import randint
from pygame import gfxdraw
from Defs import *
import numpy as np
import json
from Classes.imports.Graph import Graph
from datetime import datetime,timedelta
from Classes.StockVisualizer import StockVisualizer,POINTSPERGRAPH


class Stock():
    """Class contains the points and ability to modify the points of the stock"""

    def __init__(self,name,volatility,color) -> None:
        self.color,self.name = color,name

        #variables for graphing the stock 
        #make graphingrangeoptions a dict with the name of the option as the key and the value as the amount of points to show
        self.graphrangeoptions = {"1H":3600,"1D":23_400,"1W":117_000,"1M":489_450,"3M":1_468_350,"1Y":5_873_400}
        self.condensefacs = {key:value/POINTSPERGRAPH for key,value in self.graphrangeoptions.items()}#the amount of points that each index of the graph has
        # self.graphrange = '1H' # H, D, W, M, 3M, Y
        self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphfillvar = {key:0 for key in self.graphrangeoptions.keys()}# used to see when to add a point to a graph
        
        # self.bonustrendranges = [[(-1*i,i),(100000-(i*8325),500000-(i*41400))] for i in range(12)]
        self.bonustrendranges = [[(-i,i),(randint(1,12000),randint(12001,1_500_000))] for i in range(12)]
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]

        self.datafromfile()# Retrieves the data from the file
        self.price = self.graphs['1H'][-1]# the price of the stock at the last graphed point
        
        self.volatility = volatility
        self.recentrenders = {}# a dict of the renders of the recent prices

        self.graph = Graph()
    

    def __str__(self) -> str:
        return f'{self.name}'
    
    def reset_trends(self):
        """Sets/resets the trends for the stock"""
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]#resets the trends for each bonus trend

    def getPercent(self,graphrange):
        """Returns the percent change of the stock"""
        return ((self.graphs[graphrange][-1]/self.graphs[graphrange][0])-1)*100
    
    def getPercentDate(self,date:datetime,gametime:datetime):
        """Returns the percent change from a specific date to today"""
        def getClosestDate(secondsAgo):
            """Returns the point closest to the number of seconds ago a date was"""
            key = list(self.graphrangeoptions)[-1]# sets it to the last key	"1Y"
            for k,value in (self.graphrangeoptions.items()):
                if value > secondsAgo:
                    key = k
                    break
            secondsPerPoint = self.graphrangeoptions[key]/POINTSPERGRAPH
            closestIndex = int(secondsAgo/secondsPerPoint)
            if closestIndex >= len(self.graphs[key]):
                closestIndex = len(self.graphs[key])-1
            return self.graphs[key][closestIndex]
        diff = gametime-date
        return ((self.price/getClosestDate(diff.total_seconds()))-1)*100

        
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
                self.reset_trends()

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
        while multiplier > 0:
            step = multiplier % maxstep if multiplier < maxstep else maxstep# how much to multiply the movement by

            for i, bonustrend in enumerate(self.bonustrends):# for each bonus trend
                if bonustrend[1] <= 0:  # if the time is out
                    self.bonustrends[i] = [randint(*self.bonustrendranges[i][0]), randint(*self.bonustrendranges[i][1])]
                else:
                    bonustrend[1] -= step

            total_trend = sum(trend[0] for trend in self.bonustrends)# the total trend of all the bonus trends
            total_trend = total_trend if total_trend >= 0 else -1 * (total_trend // 2)# if the total trend is negative, then divide it by 2
            highvolitity = self.volatility + total_trend# the highest volitility that the stock can have
            lowvolitity = -self.volatility + total_trend# the lowest volitility that the stock can have
            
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
    
