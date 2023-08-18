import pygame
from random import randint
import time
from Classes.Stock import Stock
from Defs import *
from pygame import gfxdraw
import numpy as np


class Player(Stock):
    def __init__(self,window_offset,stocknames) -> None:
        name = 'Net Worth'
        super().__init__(name,(2500,2500),0,Player,window_offset,stocknames)
        self.name = name
        self.price = 2500
        self.stocks = []
        # self.pricepoints = np.array([[self.price]],dtype=object)

        self.stockvalues = []
        self.messagedict = {}
        # self.recent_movementvar = (None,None,(180,180,180))
        
    def buy(self,name:str,price:int,obj,quantity:int=1):
        for _ in range(quantity+1):
            if self.price >= price:
                self.price -= price
                self.stocks.append([name,price,obj])

        self.messagedict[f'Purchased {quantity} shares of {name} for {round(price*quantity,2)}'] = (time.time(),(0,200,0))
        print(f'buying {name} for {price}')
        print('cash is',self.price)
        print('stocks are',self.stocks)
        print('/'*20)
    def sell(self,name:str,price:int,obj,quantity:int=1):
        self.price += price*quantity
        print(self.stocks)
        self.messagedict[f'Sold {quantity} shares of {name} for {round(price*quantity,2)}'] = (time.time(),(0,200,0))
        if price*quantity < sum([stock[1] for stock in self.stocks if stock[0] == name]):
            self.messagedict[f'Lost {round((price*quantity)-sum([self.stocks[i][1] for i in range(quantity) if self.stocks[i][0] == name]),2)} from {name}'] = (time.time(),(200,0,0))
        else:
            self.messagedict[f'Profited {round((price*quantity)-sum([self.stocks[i][1] for i in range(quantity) if self.stocks[i][0] == name]),2)} from {quantity} {name} shares'] = (time.time(),(0,200,0))
        for _ in range(quantity):
            # originalprice = [stock[1] for stock in self.stocks if stock[0] == name][0]
            print([stock[0] for stock in self.stocks],'stocks')
            originalprice = self.stocks[[stock[0] for stock in self.stocks].index(name)][1]
            self.stocks.remove([name,originalprice,obj])
            # if price < originalprice:
            #     self.messagedict[f'Lost {round(price-originalprice,2)} from {name}'] = (time.time(),(200,0,0))
            # else:
            #     self.messagedict[f'Profited {round(price-originalprice,2)} from {name}'] = (time.time(),(0,200,0))
        
        
        print(f'selling {name} for {price}')
        print('profited ',price-originalprice)
        print('cash is',self.price)
        print('stocks are',self.stocks)
        print('/'*20)

    def message(self,screen:pygame.Surface):
        """displays everything in the self.messagedict, key is the text, value is (time,color))]"""
        keys_to_delete = []
        for i,(text,(starttime,color)) in enumerate(self.messagedict.items()):
            if i < 8 and time.time() < starttime+15:
                #draw a box around the text using gfxdraw filled polygon
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.endingpos[1]+35+(i*40)),(self.startingpos[0],self.endingpos[1]+35+(i*40)),(self.startingpos[0]+10,self.endingpos[1]+65+(i*40)),(self.endingpos[0]+10,self.endingpos[1]+65+(i*40))],color)
                screen.blit(fontlist[25].render(text,(255,255,255))[0],(self.endingpos[0]+10,self.endingpos[1]+40+(i*40)))
            else:
                if list(self.messagedict.keys())[0] not in keys_to_delete:
                    keys_to_delete.append(list(self.messagedict.keys())[0])

        for key in keys_to_delete:
            del self.messagedict[key]

    def graph(self,stocklist:list):
        # print(self.price,'cash')
        self.stockvalues.clear()
        if self.stocks:#if there are stocks
            bankruptamounts = []#list containing the amount of money lost from each bankrupt stocks - all in 1 message so it doesn't spam the message box
            for stock in self.stocks:
                if isinstance([stockobj.pricereset_time for stockobj in stocklist if stockobj.name == stock[0]][0],float):#checking to see if the stockobj has a pricereset_time (if it's bankrupt)
                    if not bankruptamounts:#if there are no amounts in bankruptamounts yet
                        bankruptamounts.append(f'{stock[0]} went bankrupt')#only 1 of these messages
                    bankruptamounts += [stock[1]]#add the amount of money lost from the bankrupt stock to the list

                    self.stocks.remove(stock)
                self.stockvalues.append([stockobj for stockobj in stocklist if stockobj.name == stock[0]][0].price)
            if bankruptamounts:
                self.messagedict[bankruptamounts[0]] = (time.time(),(200,0,0))#add the bankrupt message to the message dict
                bankruptamounts.remove(bankruptamounts[0])#remove the bankrupt message from bankruptamounts
                self.messagedict[f'Lost {round(sum(bankruptamounts),2)} from bankrupt stocks'] = (time.time(),(200,0,0))#add the total amount of money lost from bankrupt stocks to the message dict
            #Make for multiple stocks not just one---------------------------------------------------------------------  probably need a dict instead of banruptamounts list
            
        