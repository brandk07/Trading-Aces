import pygame
from random import randint
import time
from Classes.Stock import Stock
from Defs import *
from pygame import gfxdraw
import numpy as np
from datetime import datetime, timedelta

class Player(Stock):
    

    def __init__(self,stocknames,color,transact,gametime) -> None:
        """Player class is a child of the Stock class price is the networth of the player"""
        name = 'Net Worth'
        super().__init__(name,color,gametime)
        
        self.name = name
        
        self.cash = 25000
        if self.graphs[MINRANGE].size == 1:
            print('cash is',self.cash)
            self.graphs = {key:np.array([self.cash],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        # for (key,graph) in self.graphs.items():
        #     if graph.size == 1:
        #         self.graphs[key] = np.array([self.cash],dtype=object)
        self.stocks = []# list of lists containing the stockAsset objects
        self.options = []#list of option objects
        self.stockvalues = []
        self.messagedict = {}
        self.taxrate = 0.15
        self.transact = transact
        self.assetText = {
            StockAsset:'Share',
            OptionAsset:'Option'
        }
        self.gametime = gametime
        self.updateOptions = 0# used to update the options every 120 frames

        # self.recent_movementvar = (None,None,(180,180,180)
    def newDay(self,gametime:datetime):
        """Called at the start of a new day"""
        self.updateOptions = 0
        for option in self.options:
            option.getValue(bypass=True)
        for i in range(len(self.options)-1,-1,-1):
            # print(self.options[i].name,self.options[i].daysToExpiration(gametime.time))
            if self.options[i].daysToExpiration() <= 0:
                self.options[i].option.t = 0
                self.cash += self.options[i].option.getPrice(method="BSM",iteration=1)*self.options[i].quantity
                self.options.pop(i)
        # print('new day')
        

    def gameTick(self,gamespeed:int):
        """Used to update the options every 120 frames"""
        self.updateOptions += gamespeed
        if self.updateOptions >= 512:
            self.updateOptions = 0
            for option in self.options:
                option.getValue(bypass=True)

        self.update_price(gamespeed,Player)

    def buyAsset(self,newasset):
        
        if newasset.quantity <= 0:
            return
        if isinstance(newasset,StockAsset):
            assetlist = self.stocks 
        elif isinstance(newasset,OptionAsset):
            assetlist = self.options

        if self.cash >= newasset.getValue(bypass=True):
            # ["Sold 39 Shares of","KSTON for $5,056.93","Balance $26,103.18"]
            text = [
                f"Added {newasset.quantity} {newasset.getStockObj().name} {'' if type(newasset) == StockAsset else newasset.getType()} {self.assetText[type(newasset)]+('s' if newasset.quantity > 1 else '')}",
                f"{self.gametime.getDate()}",
                f"${limit_digits(newasset.getValue(bypass=True,fullvalue=False),12)} Per Share",
                f"Cost -${limit_digits(newasset.getValue(bypass=True),12)}",
                f"Balance ${limit_digits(self.cash-newasset.getValue(bypass=True),12)}"
            ]
            self.transact.addTransaction(*text)
            self.cash -= newasset.getValue()# fullvalue is True by default
            for a in assetlist:# if the asset is already in the list, add the new asset to the old one
                if newasset == a:# use the __eq__ method to compare the assets
                    a += newasset# use the __iadd__ method to add the assets together
                    return# return if the asset is already in the list``
            
            assetlist.append(newasset.copy())# if the asset is not in the list, add it to the list
            # print(asset.quantity)
            # print(asset.getValue())
            # print(f'buying {asset} for {asset.getValue(True):.2f}')
            soundEffects['buy'].play()
            print('cash is',self.cash)

    def sellAsset(self,asset,quantity):
        """sells the quantity number of the asset object given
        won't sell more than the quantity of the asset"""
        quantity = int(quantity)
        if isinstance(asset,StockAsset):
            assetlist = self.stocks 
        elif isinstance(asset,OptionAsset):
            assetlist = self.options

        if quantity > (quant:=assetlist[assetlist.index(asset)].quantity):# if the quantity is greater than the quantity of the asset
            quantity = quant
        # text = [
        #     f"Sold {quantity} {self.assetText[type(asset)]+('s' if quantity > 1 else '')} of",
        #     f"{asset.getStockObj().name} for ${limit_digits(asset.getValue(bypass=True,fullvalue=False),12)}",
        #     f"Balance ${limit_digits(self.cash+asset.getValue(bypass=True,fullvalue=False),12)}"
        # ]
        loss_gain = asset.getValue(bypass=True,fullvalue=False)*quantity-asset.getOgVal()*quantity
        taxes = loss_gain*self.taxrate if loss_gain > 0 else 0
        loss_gain = loss_gain if loss_gain <= 0 else loss_gain*(1-self.taxrate)
        value = (asset.getValue(bypass=True,fullvalue=False)*quantity)-taxes
        text = [
            f"Sold {quantity} {asset.name} {self.assetText[type(asset)]+('s' if quantity > 1 else '')}",
            f"{self.gametime.getDate()}",
            f"{'Lost' if loss_gain < 0 else 'Profited'} ${limit_digits(abs(loss_gain),12) if loss_gain != 0 else '0'}",
            f"Value +${limit_digits(value,12)}",
            f"Balance ${limit_digits(self.cash+value,12)}"
        ]
        self.transact.addTransaction(*text)
        
        self.cash += asset.getValue(bypass=True,fullvalue=False)*quantity# add the value of the asset to the cash

        assetlist[assetlist.index(asset)].quantity -= quantity# subtract the quantity from the asset

        if assetlist[assetlist.index(asset)].quantity <= 0:# if the quantity of the asset is 0 or less, remove the asset from the list
            assetlist.remove(asset)
    def exerciseOption(self,optionasset:OptionAsset):
        """Exercises the option"""
        print(f"Exercising Option {optionasset.name} for {optionasset.option.k} at {optionasset.option.s0}, value of ${optionasset.option.getPrice(method='BSM',iteration=1)}")
        self.cash += optionasset.option.getPrice(method="BSM",iteration=1)*optionasset.quantity
        self.options.remove(optionasset)

        

        
    def getNetworth(self):
        """returns the networth of the player"""
        allassets = self.stocks + self.options
        return self.cash + sum([asset.getValue() for asset in allassets])
        # return self.cash + sum([stock[0].cash*stock[2] for stock in self.stocks]) + sum([option.get_value() for option in self.options])
    def getAssets(self,amount:int=0):
        """returns the assets of the player, returns all of them if amount is 0 else returns the top [amount] assets"""
        if amount == 0:
            return self.stocks + self.options

        allassets = self.stocks + self.options
        allassets.sort(key=lambda x:x.getValue(),reverse=True)
    
        return allassets[:amount]
        
    
    # def message(self,screen:pygame.Surface):
    #     """displays everything in the self.messagedict, key is the text, value is (time,color))]"""
    #     keys_to_delete = []
    #     for i,(text,(starttime,color)) in enumerate(self.messagedict.items()):
    #         if i < 8 and time.time() < starttime+15:
    #             #draw a box around the text using gfxdraw filled polygon
    #             gfxdraw.filled_polygon(screen,[(self.endpos[0],self.endpos[1]+35+(i*40)),(self.startpos[0],self.endpos[1]+35+(i*40)),(self.startpos[0]+10,self.endpos[1]+65+(i*40)),(self.endpos[0]+10,self.endpos[1]+65+(i*40))],color)
    #             screen.blit(fontlist[25].render(text,(255,255,255))[0],(self.endpos[0]+10,self.endpos[1]+40+(i*40)))
    #         else:
    #             if list(self.messagedict.keys())[0] not in keys_to_delete:
    #                 keys_to_delete.append(list(self.messagedict.keys())[0])

    #     for key in keys_to_delete:
    #         del self.messagedict[key]


    # def graph(self,stocklist:list):
    #     # print(self.cash,'cash')
    #     self.stockvalues.clear()
    #     if self.stocks:#if there are stocks
    #         bankruptamounts = []#list containing the amount of money lost from each bankrupt stocks - all in 1 message so it doesn't spam the message box
    #         for stock in self.stocks:
    #             if isinstance([getStockObj().pricereset_time for getStockObj() in stocklist if getStockObj() == stock[0]][0],float):#checking to see if the getStockObj() has a pricereset_time (if it's bankrupt)
    #                 if not bankruptamounts:#if there are no amounts in bankruptamounts yet
    #                     bankruptamounts.append(f'{stock[0]} went bankrupt')#only 1 of these messages
    #                 bankruptamounts += [stock[1]]#add the amount of money lost from the bankrupt stock to the list

    #                 self.stocks.remove(stock)
    #             self.stockvalues.append([getStockObj() for getStockObj() in stocklist if getStockObj() == stock[0]][0].price)
    #         if bankruptamounts:
    #             self.messagedict[bankruptamounts[0]] = (time.time(),(200,0,0))#add the bankrupt message to the message dict
    #             bankruptamounts.remove(bankruptamounts[0])#remove the bankrupt message from bankruptamounts
    #             self.messagedict[f'Lost {round(sum(bankruptamounts),2)} from bankrupt stocks'] = (time.time(),(200,0,0))#add the total amount of money lost from bankrupt stocks to the message dict
    #         #Make for multiple stocks not just one---------------------------------------------------------------------  probably need a dict instead of banruptamounts list
            
        