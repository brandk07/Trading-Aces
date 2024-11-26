from Defs import *
import numpy as np
import pygame
from random import randint
from Classes.BigClasses.Stock import Stock


class TotalMarket(Stock):
    def __init__(self,gametime,stocklist) -> None:
        # name,volatility,color,gametime
        super().__init__('Total',(213, 219, 44),gametime,0)
        self.stocks = stocklist.copy()
        self.combinStocks = stocklist.copy()# the stocks that are combined to make the total market
        # self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
    # def getDividendYield(self):
    #     """returns the dividend yield of the stock"""
    #     return round(sum([s.dividendYield for s in self.combinStocks])/len(self.combinStocks),3)
    def getDividendYield(self):
        """returns the dividend yield of the stock"""
        percents = self.getStockPercentages()
        return round(sum([s.dividendYield*percents[s.name] for s in self.combinStocks]),3)
    def getStockPercentages(self):
        """returns a dictionary with the stock name as the key and the percentage of the stock in the index fund as the value"""
        return {stock.name:stock.price/(self.price*len(self.combinStocks)) for stock in self.combinStocks}
    
    def datafromfile(self,gametime):
        # this child class does not need to read data from a file
        # self.graphs = {key:np.array([100],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphs = {key:deque([100],maxlen=POINTSPERGRAPH) for key in self.graphrangeoptions.keys()}#the lists for each graph range
    def fill_graphs(self):
        """Fills the graphs with the stock's prices"""
        # equivalent to the datafromfile method, but it wasn't necessary to store stuff in a file since it can be loaded fast 
        for key in self.graphrangeoptions:
            # self.graphs[key] = np.array([],dtype=object)
            self.graphs[key] = deque(maxlen=POINTSPERGRAPH)
            for point in range(len(self.stocks[0].graphs[key])):
                
                value = sum([stock.graphs[key][point] for stock in self.stocks])/9
                # self.graphs[key] = np.append(self.graphs[key],value)
                self.graphs[key].append(value)
        self.price = self.graphs[MINRANGE][-1]
            

    def update_range_graphs(self,value,step=1):
        
        for key in self.graphrangeoptions:
            condensefactor = self.condensefacs[key]
            for i in range(step):
                self.graphfillvar[key] += 1
                if self.graphfillvar[key] == int(condensefactor):#if enough points have passed to add a point to the graph (condensefactor is how many points must go by to add 1 point to the graph)
                    #add the last point to the list
                    self.graphfillvar[key] = 0
                    # self.graphs[key] = np.append(self.graphs[key],value)
                    self.graphs[key].append(value)

            
            # if len(self.graphs[key]) > POINTSPERGRAPH:
                # print('deleting',key,len(self.graphs[key]))
                # self.graphs[key] = np.delete(self.graphs[key],0)

        self.price = value

    def updategraphs(self,gameplay_speed:int,step):
        """Updates the graphs for the stocks"""
        # for i in range(gameplay_speed):
        for i in range(0,gameplay_speed,step):
            value = 0
            for stock in self.stocks:
                value += stock.graphs[MINRANGE][-1]# adds the last value of the stock to the value
            
            value = value/len(self.stocks)# gets the average value of the stocks
            # self.graphs["1H"] = np.append(self.graphs["1H"],value)# adds the value to the graph

            self.update_range_graphs(value,step=step)
            
from collections import deque

class IndexFund(Stock):
    def __init__(self,gametime,fundName:str,color:tuple,combinationStocks:list) -> None:
        # name,volatility,color,gametime
        super().__init__(fundName,color,gametime,0)
        # self.stocks = stocks
        self.combinStocks = combinationStocks# the stocks that are combined to make the index Fund
        # self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
    def getDividendYield(self):
        """returns the dividend yield of the stock"""
        percents = self.getStockPercentages()
        return round(sum([s.dividendYield*percents[s.name] for s in self.combinStocks]),3)
    def getStockPercentages(self):
        """returns a dictionary with the stock name as the key and the percentage of the stock in the index fund as the value"""
        return {stock.name:stock.price/(self.price*len(self.combinStocks))for stock in self.combinStocks}
    def datafromfile(self,gametime):
        # this child class does not need to read data from a file
        # self.graphs = {key:np.array([100],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphs = {key:deque([100],maxlen=POINTSPERGRAPH) for key in self.graphrangeoptions.keys()}#the lists for each graph range

    def fill_graphs(self):
        """Fills the graphs with the stock's prices"""
        # equivalent to the datafromfile method, but it wasn't necessary to store stuff in a file since it can be loaded fast 
        for key in self.graphrangeoptions:
            self.graphs[key] = deque(maxlen=POINTSPERGRAPH)
            # for point in range(self.combinStocks[0].graphs[key].size):
            for point in range(len(self.combinStocks[0].graphs[key])):
                
                value = sum([stock.graphs[key][point] for stock in self.combinStocks])/len(self.combinStocks)
 
                # self.graphs[key] = self.graphs[key].append(value)
                self.graphs[key].append(value)
        self.price = self.graphs[MINRANGE][-1]
            

    def update_range_graphs(self,value,step=1):
        
        for key in self.graphrangeoptions:
            condensefactor = self.condensefacs[key]
            for i in range(step):
                self.graphfillvar[key] += 1
                if self.graphfillvar[key] == int(condensefactor):#if enough points have passed to add a point to the graph (condensefactor is how many points must go by to add 1 point to the graph)
                    #add the last point to the list
                    self.graphfillvar[key] = 0
                    # self.graphs[key] = np.append(self.graphs[key],value)
                    
                    self.graphs[key].append(value)

            
            # if len(self.graphs[key]) > POINTSPERGRAPH:
            #     # print('deleting',key,len(self.graphs[key]))
            #     # self.graphs[key] = np.delete(self.graphs[key],0)
            #     self.graphs[key].popleft()
        self.price = value

    def updategraphs(self,gameplay_speed:int,step):
        """Updates the graphs for the stocks"""
        for i in range(0,gameplay_speed,step):
            value = 0
            # for stock in self.combinStocks:
                # value += stock.graphs[MINRANGE][-1]# adds the last value of the stock to the value
            value = sum([stock.graphs[MINRANGE][-1] for stock in self.combinStocks])/len(self.combinStocks)
            # value = value/len(self.combinStocks)# gets the average value of the stocks
            # self.graphs["1H"] = np.append(self.graphs["1H"],value)# adds the value to the graph

            self.update_range_graphs(value,step=step)