import pygame
from random import randint
import time
from Classes.Stockprice import Stock


class Player(Stock):
    def __init__(self,startingpos,endingpos) -> None:
        name = 'Net Worth'
        super().__init__(name,startingpos,endingpos,(2500,2500),0)
        self.name = name
        self.startingpos = startingpos
        self.endingpos = endingpos
        self.cash = 2500
        self.stocks = []
        self.stockvalues = []
        self.pricepoints = [[startingpos[0]-5,self.cash]]
        # self.recent_movementvar = (None,None,(180,180,180))
        
    def buy(self,name:str,price:int):
        if self.cash >= price:
            self.cash -= price
            self.stocks.append([name,price])
        print(f'buying {name} for {price}')
        print('cash is',self.cash)
        print('stocks are',self.stocks)
        print('/'*20)
    def sell(self,name:str,price:int):
        self.cash += price
        originalprice = [stock[1] for stock in self.stocks if stock[0] == name][0]
        self.stocks.remove([name,originalprice])
        print(f'selling {name} for {price}')
        print('profited ',price-originalprice)
        print('cash is',self.cash)
        print('stocks are',self.stocks)
        print('/'*20)

    def graph(self,stocklist:list):
        self.stockvalues.clear()
        if self.stocks:#if there are stocks
            for stock in self.stocks:
                self.stockvalues.append([stockobj for stockobj in stocklist if stockobj.name == stock[0]][0].pricepoints[-1][1])
            # print('cash is',self.cash)

            # print(sum(self.stockvalues)+self.cash)
            
            self.pricepoints.append([self.startingpos[0]-5,sum(self.stockvalues)+self.cash])
        else:
            self.pricepoints.append([self.startingpos[0]-5,self.cash])
        