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
        self.window_offset = window_offset
        self.cash = 1000
        self.stocks = []
        # self.pricepoints = np.array([[self.cash]],dtype=object)

        self.stockvalues = []
        self.messagedict = {}
        # self.recent_movementvar = (None,None,(180,180,180))
        
    def buy(self,obj,price:int,quantity:int=1):
        """will add stocks until out of cash"""
        if quantity > 0:
            quant = 0
            for _ in range(quantity):
                if self.cash >= price:
                    self.cash -= price
                    quant += 1
            quantity = quant# the quantity of stocks that were bought
            self.stocks.append([obj,price,quantity])

            # self.messagedict[f'Purchased {quantity} shares of {name} for {round(price*quantity,2)}'] = (time.time(),(0,200,0))
            print(f'buying {obj} for {price}')
            print('cash is',self.cash)
            print('stocks are',self.stocks)
            print('/'*20)

    def sell(self,obj,newprice:int,quantity:int=1):
        stockquant = sum([stock[2] for stock in self.stocks if stock[0] == obj])
        print(stockquant,'stockquant')
        if quantity > stockquant:
            quantity = stockquant
        
        self.cash += newprice*quantity
        ogprices = []# list of the original prices of the stocks being sold
        while quantity >= 0:
            for stock in self.stocks:
                if stock[0] == obj:# if the stock is the same as the one being sold
                    if stock[2] > quantity:# if the stock has more than the quantity
                        ogprices.append(stock[1] for _ in range(quantity))
                        stock[2] -= quantity# remove the quantity from the stock
                        break
                    elif stock[2] == quantity:# if the stock has the same amount as the quantity
                        ogprices.append(stock[1] for _ in range(quantity))
                        self.stocks.remove(stock)
                        break
                    else:
                        ogprices.append(stock[1] for _ in range(stock[2]))
                        quantity -= stock[2]
                        self.stocks.remove(stock)
                        
        print(f'selling {obj} for {newprice}')
        print(f"Profited ${(sum(ogprices)/len(ogprices))-newprice:.2f} per share")
        print(f"Total profit: ${sum(ogprices)-newprice*len(ogprices):.2f}")
        print('cash is',self.cash)
        print('stocks are',self.stocks)
        print('/'*20)
        
        # if quantity > sum([stock[2] for stock in self.stocks if stock[0] == name]):
        #     quantity = sum([stock[1] for stock in self.stocks if stock[0] == name])
        # self.cash += price*quantity
        # print(self.stocks)
        # self.messagedict[f'Sold {quantity} shares of {name} for {round(price*quantity,2)}'] = (time.time(),(0,200,0))
        # if price*quantity < sum([stock[1] for stock in self.stocks if stock[0] == name]):
        #     self.messagedict[f'Lost {round((price*quantity)-sum([self.stocks[i][1] for i in range(quantity) if self.stocks[i][0] == name]),2)} from {name}'] = (time.time(),(200,0,0))
        # else:
        #     self.messagedict[f'Profited {round((price*quantity)-sum([self.stocks[i][1] for i in range(quantity) if self.stocks[i][0] == name]),2)} from {quantity} {name} shares'] = (time.time(),(0,200,0))
        # for _ in range(quantity):
        #     # originalprice = [stock[1] for stock in self.stocks if stock[0] == name][0]
        #     print([stock[0] for stock in self.stocks],'stocks')
        #     originalprice = self.stocks[[stock[0] for stock in self.stocks].index(name)][1]
        #     print(self.stocks)
        #     print(originalprice)
        #     self.stocks.remove([name,originalprice,obj])
        #     # if price < originalprice:
        #     #     self.messagedict[f'Lost {round(price-originalprice,2)} from {name}'] = (time.time(),(200,0,0))
        #     # else:
        #     #     self.messagedict[f'Profited {round(price-originalprice,2)} from {name}'] = (time.time(),(0,200,0))
        
        
        

    def message(self,screen:pygame.Surface):
        """displays everything in the self.messagedict, key is the text, value is (time,color))]"""
        keys_to_delete = []
        for i,(text,(starttime,color)) in enumerate(self.messagedict.items()):
            if i < 8 and time.time() < starttime+15:
                #draw a box around the text using gfxdraw filled polygon
                gfxdraw.filled_polygon(screen,[(self.endpos[0],self.endpos[1]+35+(i*40)),(self.startpos[0],self.endpos[1]+35+(i*40)),(self.startpos[0]+10,self.endpos[1]+65+(i*40)),(self.endpos[0]+10,self.endpos[1]+65+(i*40))],color)
                screen.blit(fontlist[25].render(text,(255,255,255))[0],(self.endpos[0]+10,self.endpos[1]+40+(i*40)))
            else:
                if list(self.messagedict.keys())[0] not in keys_to_delete:
                    keys_to_delete.append(list(self.messagedict.keys())[0])

        for key in keys_to_delete:
            del self.messagedict[key]

    def graph(self,stocklist:list):
        # print(self.cash,'cash')
        self.stockvalues.clear()
        if self.stocks:#if there are stocks
            bankruptamounts = []#list containing the amount of money lost from each bankrupt stocks - all in 1 message so it doesn't spam the message box
            for stock in self.stocks:
                if isinstance([stockobj.pricereset_time for stockobj in stocklist if stockobj == stock[0]][0],float):#checking to see if the stockobj has a pricereset_time (if it's bankrupt)
                    if not bankruptamounts:#if there are no amounts in bankruptamounts yet
                        bankruptamounts.append(f'{stock[0]} went bankrupt')#only 1 of these messages
                    bankruptamounts += [stock[1]]#add the amount of money lost from the bankrupt stock to the list

                    self.stocks.remove(stock)
                self.stockvalues.append([stockobj for stockobj in stocklist if stockobj == stock[0]][0].price)
            if bankruptamounts:
                self.messagedict[bankruptamounts[0]] = (time.time(),(200,0,0))#add the bankrupt message to the message dict
                bankruptamounts.remove(bankruptamounts[0])#remove the bankrupt message from bankruptamounts
                self.messagedict[f'Lost {round(sum(bankruptamounts),2)} from bankrupt stocks'] = (time.time(),(200,0,0))#add the total amount of money lost from bankrupt stocks to the message dict
            #Make for multiple stocks not just one---------------------------------------------------------------------  probably need a dict instead of banruptamounts list
            
        