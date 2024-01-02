import pygame
from random import randint
import time
from Classes.Stock import Stock
from Defs import *
from pygame import gfxdraw
import numpy as np

class Player(Stock):
    

    def __init__(self,window_offset,stocknames,color) -> None:
        name = 'Net Worth'
        super().__init__(name,(2500,2500),0,Player,window_offset,stocknames,color)
        self.name = name
        self.window_offset = window_offset
        self.cash = 2500
        self.stocks = []# list of lists containing the stock object, the price bought at, and the quantity
        # self.pricepoints = np.array([[self.cash]],dtype=object)
        self.options = []#list of option objects
        self.stockvalues = []
        self.messagedict = {}

        self.optioncolors = [(211, 160, 147),(147, 196, 125),(227, 192, 198),(248, 150, 143),(252, 216, 60), (128, 189, 152),(162, 195, 243),(143, 134, 130),(248, 185, 173),(202, 80, 30),  (128, 128, 0),  (135, 206, 235),(145, 184, 106),(200, 162, 200),(255, 213, 148),(242, 201, 76), (112, 161, 151),(156, 51, 66),  (51, 51, 51),   (194, 178, 169),]


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

            # check if the stock is already in the list
            if [obj,price] in [[stock[0],stock[1]] for stock in self.stocks]:
                for stock in self.stocks:
                    if stock[0] == obj and stock[1] == price:
                        stock[2] += quantity
                        break
            else:     
                self.stocks.append([obj,price,quantity])

            # self.messagedict[f'Purchased {quantity} shares of {name} for {round(price*quantity,2)}'] = (time.time(),(0,200,0))
            print(f'buying {obj} for {price}')
            print('cash is',self.cash)
            print('stocks are',self.stocks)
            print('/'*20)

    def sell(self,obj,ogprice,quantity:int=1):

        stockindex = [(stock[0],stock[1]) for stock in self.stocks].index((obj,ogprice))
        if quantity > (quant:=self.stocks[stockindex][2]):
            quantity = quant
        
        self.cash += obj.price*quantity
        if quantity == self.stocks[stockindex][2]:
            self.stocks.remove(self.stocks[stockindex])
        else:
            self.stocks[stockindex][2] -= quantity
                        
        print(f'selling {obj} for {obj.price}')
        print(f"Profited ${(ogprice)-obj.price:.2f} per share")
        print(f"Total profit: ${(ogprice-obj.price)*quantity:.2f}")
        print('cash is',self.cash)
        print('stocks are',self.stocks)
        print('/'*20)

    def buyOption(self,optionobj):
        if self.cash >= optionobj.get_value(bypass=True):

            self.cash -= optionobj.get_value(True)
            inoptions = False
            for option in self.options:
                inoptions = option.combine(optionobj)
                if inoptions:break

            if not inoptions:
                self.options.append(optionobj)
                optionobj.color = self.optioncolors[len(self.options)-1 if len(self.options)-1 < len(self.optioncolors) else randint(0,len(self.optioncolors)-1)]
                print(optionobj.color)

            print(f'buying {optionobj} for {optionobj.get_value(True):.2f}')
            print('cash is',self.cash)
            print('options are',self.options)
            print('/'*20)

    def sellOption(self,optionobj):
        # optionindex = self.options.index(optionobj)
        self.cash += optionobj.get_value(True)
        self.options.remove(optionobj)
        print(f'selling {optionobj} for {optionobj.get_value(True):.2f}')
        print('cash is',self.cash)

    def get_Networth(self):
        """returns the networth of the player"""
        return self.cash + sum([stock[0].price*stock[2] for stock in self.stocks]) + sum([option.get_value() for option in self.options])

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
            
        