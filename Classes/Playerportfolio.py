import pygame
from random import randint
import time
from Classes.Stockprice import Stock
from Defs import *
from pygame import gfxdraw


class Player(Stock):
    def __init__(self,startingpos,endingpos,window_offset) -> None:
        name = 'Net Worth'
        super().__init__(name,startingpos,endingpos,(2500,2500),0,Player,window_offset)
        self.name = name
        self.startingpos = (startingpos[0] - self.winset[0], startingpos[1] - self.winset[1])
        self.endingpos = (endingpos[0] - self.winset[0], endingpos[1] - self.winset[1])
        self.cash = 2500
        self.stocks = []
        self.stockvalues = []
        self.pricepoints = [[startingpos[0]-5,self.cash]]
        self.messagedict = {}
        self.font = fonts(25)
        # self.recent_movementvar = (None,None,(180,180,180))
        
    def buy(self,name:str,price:int):
        if self.cash >= price:
            self.cash -= price
            self.stocks.append([name,price])
        self.messagedict[f'Purchased {round(price,2)} from {name}'] = (time.time(),(0,200,0))
        print(f'buying {name} for {price}')
        print('cash is',self.cash)
        print('stocks are',self.stocks)
        print('/'*20)
    def sell(self,name:str,price:int):
        self.cash += price
        originalprice = [stock[1] for stock in self.stocks if stock[0] == name][0]
        self.stocks.remove([name,originalprice])
        if price < originalprice:
            self.messagedict[f'Lost {round(price-originalprice,2)} from {name}'] = (time.time(),(200,0,0))
        else:
            self.messagedict[f'Profited {round(price-originalprice,2)} from {name}'] = (time.time(),(0,200,0))
        

        print(f'selling {name} for {price}')
        print('profited ',price-originalprice)
        print('cash is',self.cash)
        print('stocks are',self.stocks)
        print('/'*20)

    def message(self,screen:pygame.Surface):
        """displays everything in the self.messagedict, key is the text, value is (time,color))]"""
        keys_to_delete = []
        for i,(text,(starttime,color)) in enumerate(self.messagedict.items()):
            if i < 8 and time.time() < starttime+15:
                text = self.font.render(text,True,(255,255,255))
                #draw a box around the text using gfxdraw filled polygon
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.endingpos[1]+35+(i*40)),(self.startingpos[0],self.endingpos[1]+35+(i*40)),(self.startingpos[0]+10,self.endingpos[1]+65+(i*40)),(self.endingpos[0]+10,self.endingpos[1]+65+(i*40))],color)
                screen.blit(text,(self.endingpos[0]+10,self.endingpos[1]+40+(i*40)))
            else:
                if list(self.messagedict.keys())[0] not in keys_to_delete:
                    keys_to_delete.append(list(self.messagedict.keys())[0])

        for key in keys_to_delete:
            del self.messagedict[key]

    def graph(self,stocklist:list):
        self.stockvalues.clear()
        if self.stocks:#if there are stocks
            bankruptamounts = []#list containing the amount of money lost from each bankrupt stocks - all in 1 message so it doesn't spam the message box
            for stock in self.stocks:
                if isinstance([stockobj.pricereset_time for stockobj in stocklist if stockobj.name == stock[0]][0],float):#checking to see if the stockobj has a pricereset_time (if it's bankrupt)
                    if not bankruptamounts:#if there are no amounts in bankruptamounts yet
                        bankruptamounts.append(f'{stock[0]} went bankrupt')#only 1 of these messages
                    bankruptamounts += [stock[1]]#add the amount of money lost from the bankrupt stock to the list

                    self.stocks.remove(stock)
                self.stockvalues.append([stockobj for stockobj in stocklist if stockobj.name == stock[0]][0].pricepoints[-1][1])
            if bankruptamounts:
                self.messagedict[bankruptamounts[0]] = (time.time(),(200,0,0))#add the bankrupt message to the message dict
                bankruptamounts.remove(bankruptamounts[0])#remove the bankrupt message from bankruptamounts
                self.messagedict[f'Lost {round(sum(bankruptamounts),2)} from bankrupt stocks'] = (time.time(),(200,0,0))#add the total amount of money lost from bankrupt stocks to the message dict
            #Make for multiple stocks not just one---------------------------------------------------------------------  probably need a dict instead of banruptamounts list
            
            self.pricepoints.append([self.startingpos[0]-5,sum(self.stockvalues)+self.cash])
        else:
            self.pricepoints.append([self.startingpos[0]-5,self.cash])
        