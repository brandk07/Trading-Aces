import pygame
from random import randint
import statistics
from pygame import gfxdraw
import time
from Defs import *
import numpy as np
import timeit

class Stock():
    def __init__(self,name,startingvalue_range,volatility,Playerclass,window_offset,stocknames,currenttime) -> None:
        
        self.winset = window_offset
        self.pricepoints = [[randint(*startingvalue_range),currenttime]]
        self.startingpos,self.endingpos = (0,0),(0,0)
        self.Playerclass = Playerclass
        self.starting_value_range = startingvalue_range
        self.name = name
        self.pricereset_time = None
        self.stocknames = stocknames
        #variables for graphing the stock 
        self.graphrangeoptions = (('hour',10800),('day',70200),('week',351000),('month',1_404_000),('year',16_884_000),('all',None))
        self.graphrange = 0 #
        #variables for the stock price
        self.volatility = volatility
        self.periodbonus = [randint(-5,5)/1000,randint(140_400,421_200)]# [%added to each movement, time up to 6 days for the period bonus (low as 2 days)]
        self.daybonus = [randint(-5,5)/1000,randint(59400,81000)]# [%added to each movement, time low as 5.5 hours high as 7.5 (remember 6.5 hours is 1 day)]
        self.hourlytrend = [randint(-20,20),randint(8100,21600)]# added to the volitility each movement,time low as 45 minutes, high as 2 hours
        self.minutetrend = [randint(-10,10),randint(150,3600)]# added to the volitility each movement, time low as 50 seconds, high as 20 minutes 
        self.bonustrends = [self.periodbonus,self.daybonus,self.hourlytrend,self.minutetrend]#this is used to make seeing if the time is out easier
        self.bonustrendranges = [(140_400,421_200),(59400,81000),(8100,21600),(150,3600)]#the ranges for the time for each bonus trend
    def resize_graph(self):
        if len(self.pricepoints) > (numrange:=self.graphrangeoptions[self.graphrange][1]):#if the amount of points we already have is greater than the amount needed
            medianpoint = statistics.median([point[0] for point in self.pricepoints[-numrange:]])
        else:
            medianpoint = statistics.median([point[0] for point in self.pricepoints])
        #below we are checking if the max or min is further away from the median point, and then returning the distance from the median point
        if abs(min(self.pricepoints, key=lambda x: x[0])[0]-medianpoint) > abs(max(self.pricepoints, key=lambda x: x[0])[0]-medianpoint):
            return (abs(min(self.pricepoints, key=lambda x: x[0])[0]-medianpoint)+30)#can add a multiplier to make the graph more towards the middle (*1.5)
        return (abs(max(self.pricepoints, key=lambda x: x[0])[0]-medianpoint)+30)
    
    def bankrupcy(self,drawn,screen:pygame.Surface=None):
        """returns False if stock is not bankrupt,don't need screen if drawn is False"""	
        if self.pricepoints[-1][0] < 0 and self.pricereset_time == None:#if stock goes bankrupt, and no time has been set
            self.pricereset_time = time.time()
            return False
        elif self.pricereset_time != None and time.time() > self.pricereset_time+5:#if stock goes bankrupt and 5 seconds have passed
            self.pricepoints[-1][0] = randint(*self.starting_value_range)
            self.temporary_movement = randint(-1*(self.volatility-1),self.volatility)
            self.movement_length = randint(60,360); self.pricereset_time = None
            if drawn:
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(200,0,0))#draws the background of the graph red
            return False
        elif self.pricereset_time != None and time.time() < self.pricereset_time+5:#if stock goes bankrupt and less then 5 seconds have passed
            if drawn:
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(200,0,0))#draws the background of the graph red
                screen.blit(fontlist[40].render(f'BANKRUPT',(255,255,255))[0],(self.endingpos[0]+15,self.startingpos[1]+15))
            return False
        return True
    
    def stock_split(self,player:object):
        if self.pricepoints[-1][0] >= 2500:
            player.messagedict[f'{self.name} has split'] = (time.time(),(0,0,200))
            for point in self.pricepoints:
                point[0] *= 0.5
            stock_quantity = len([stock for stock in player.stocks if stock[0] == self.name])
            if stock_quantity > 0:
                player.messagedict[f'You now have {stock_quantity*2} shares of {self.name}'] = (time.time(),(0,0,200))
                for stock in player.stocks.copy():
                    if stock[0] == self.name:
                        player.stocks.remove(stock)
                        player.stocks.append([stock[0]*0.5,stock[1]])
                        player.stocks.append([stock[0]*0.5,stock[1]])
                print('stocks are',player.stocks)

    def addpoint(self,lastprice):
        """returns the new price of the stock"""
        #Realize that 3 seconds of real time is 1 minute of game time (at x1 speed)
        self.periodbonus = [randint(-5,5)/1000,randint(140_400,421_200)]# [%added to each movement, time up to 6 days for the period bonus (low as 2 days)]
        self.daybonus = [randint(-5,5)/1000,randint(59400,81000)]# [%added to each movement, time low as 5.5 hours high as 7.5 (remember 6.5 hours is 1 day)]
        self.hourlytrend = [randint(-20,20),randint(8100,21600)]# added to the volitility each movement,time low as 45 minutes, high as 2 hours
        self.minutetrend = [randint(-10,10),randint(150,3600)]# added to the volitility each movement, time low as 50 seconds, high as 20 minutes 
        self.bonustrends = [self.periodbonus,self.daybonus,self.hourlytrend,self.minutetrend]#this is used to make seeing if the time is out easier

        for i,bonustrend in enumerate(self.bonustrends):
            if bonustrend[1] <= 0:
                bonustrend[1] = randint(*self.bonustrendranges[i])
            else:
                bonustrend[1] -= 1
        toltal_bonus = self.periodbonus[0]+self.daybonus[0]
        total_trend = self.hourlytrend[0]+self.minutetrend[0]
        highvolitity = self.volatility+(total_trend if total_trend >= 0 else 0)
        lowvolitity = -self.volatility+(total_trend if total_trend < 0 else 0)
        return lastprice * 1+(randint(lowvolitity,highvolitity)/100) + toltal_bonus#returns the new price of the stock
    
    def update_price(self,player:object,gametime):
        if self.bankrupcy(False):#if stock is not bankrupt
            pass

        if type(self) == Stock:#making sure that it is a Stock object and that update is true
            newprice = self.addpoint(self.pricepoints[-1][0])
            self.pricepoints.append([newprice,gametime])#if update is true then add a new point to the graph
            self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable

    def rangecontrols(self,screen:pygame.Surface,player:object,stocklist):
        #draw 4 25/25 filled polygons
        for i in range(4):
            gfxdraw.filled_polygon(screen,[(self.startingpos[0]+i*25,self.startingpos[1]),(self.startingpos[0]+i*25,self.endingpos[1]),(self.startingpos[0]+i*25+25,self.endingpos[1]),(self.startingpos[0]+i*25+25,self.startingpos[1])],(0,0,0))

    def draw(self,screen:pygame.Surface,player:object,startingpos,endingpos,stocklist,currenttime):
        if startingpos != self.startingpos or endingpos != self.endingpos:#if the starting or ending positions have changed
            xdif = self.startingpos[0]-startingpos[0]
            self.pricepoints = [[point[0]-xdif,point[1]] for point in self.pricepoints]
            #setting the starting and ending positions - where the graphs are located is constantly changing
            self.startingpos = (startingpos[0] - self.winset[0], startingpos[1] - self.winset[1])
            self.endingpos = (endingpos[0] - self.winset[0], endingpos[1] - self.winset[1])
        
        if type(self) == self.Playerclass:#if it is a Player object
            # self.graph(stocklist,currenttime)#graph the player networth
            self.message(screen)#display the messages

        if self.bankrupcy(True,screen=screen):#if stock is not bankrupt, first argument is drawn
            gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(60,60,60))#draws the background of the graph
        
        self.rangecontrols(screen,player,stocklist)#draws the range controls

        graphsize = self.resize_graph()# gets the size of the graph
        if graphsize <= 0: graphsize = 1#graphsize is the distance from the median point to the max or min point

        if len(self.pricepoints) > (numrange:=self.graphrangeoptions[self.graphrange][1]):#if the amount of points we already have is greater than the amount needed
            medianpoint = statistics.median([point[0] for point in self.pricepoints[-numrange:]])# the median point of the graphed points
        else:#if the amount of points we already have is less than the amount needed
            medianpoint = statistics.median([point[0] for point in self.pricepoints])# the median point of all the points we have

        graphheight = (self.endingpos[1]-self.startingpos[1])/2# graphheight is the height of the graph
        graphwidth = (self.startingpos[0]-self.endingpos[0])

        #yvaluefinder is a function that takes a value and returns the y value of the point - look in assets for pic of equation
        yvaluefinder = lambda x: int(graphheight+(((medianpoint-x)/graphsize)*graphheight)+self.startingpos[1])

        #first need to find the x values that we want to graph (the points that are in the range of the graph and then reduce it to fit on the graph)
        pointlen = len(self.pricepoints)
        if pointlen > graphwidth:#if we need to reduce the amount of points
            if pointlen > self.graphrangeoptions[self.graphrange][1]:#if we need to reduce the amount of points
                divisible_by = self.graphrangeoptions[self.graphrange][1]/(graphwidth)# find out how many points we need to remove from the list from the points we can graph
                graphingpoints = np.arange(0, self.graphrangeoptions[self.graphrange][1], divisible_by)

                spacing = (graphwidth)/pointlen
                print('smaller',len(graphingpoints))
            else:# if we still need to reduce the points but we don't have the full data set
                divisible_by = pointlen/(graphwidth)# find out how many points we need to remove from the list from the points that are in our list
                if divisible_by < 1: divisible_by = 1
                graphingpoints = []
                for i in range(int(graphwidth/2)):
                    newlist = []
                    for x in range(int(divisible_by*2)):
                        newlist.append(self.pricepoints[int(i*divisible_by)+x][0])

                    graphingpoints.append(yvaluefinder(int(sum(newlist)/len(newlist))))
                # graphingpoints = np.arange(0, pointlen, divisible_by*2)
                spacing = 2
                print('elsed',len(graphingpoints),len(self.pricepoints))


        else:#if we don't have enough points to fil the graph
            #figure out how much space needs to be between each point

            spacing = (graphwidth)/pointlen
            graphingpoints = list(map(yvaluefinder,[int(point[0]) for i,point in enumerate(self.pricepoints)]))
            # graphingpoints = np.arange(0, pointlen, 1)
            # print('else',len(graphingpoints))

                
        
        # going to have to limit the pricepoints list for y values
        #new_y_values is a list of all the y values of the points in the graph - had to use so I could access all of the y values for lines in the for loop

        # new_y_values = list(map(yvaluefinder,[point[0] for i,point in enumerate(self.pricepoints) if i in range(len(graphingpoints))]))

        # 
        if pointlen % 100 == 0:
            print(pointlen)
        # print(len(new_y_values),len(graphingpoints),len(self.pricepoints))
        myinterated = 0
        for i,value in enumerate(graphingpoints):
            if i >= len(graphingpoints)-1:
                print('passing',myinterated)
                pass#if last one in list or i is too great then don't draw line
            else:

                # nextvalue = yvaluefinder(self.pricepoints[int(graphingpoints[i+1])][0])
                # value = yvaluefinder(self.pricepoints[int(value)][0])

                nextvalue = int(graphingpoints[i+1])
                # value = int(value)
                xpos = self.endingpos[0]
                myinterated+=1
                # soemthign to do with y new_y_values[value] running out of indexing
                # gfxdraw.line(screen,xpos+int(i*spacing),(new_y_values[value]),xpos+int((i+1)*spacing),new_y_values[nextvalue],(255,255,255))

                gfxdraw.line(screen,xpos+int(i*spacing),(value),xpos+int((i+1)*spacing),nextvalue,(255,255,255))
        
        

                
                # your code here
                
        #Everything below is after the graph is drawn
        gfxdraw.rectangle(screen,pygame.Rect(self.endingpos[0],self.startingpos[1],(self.startingpos[0]-self.endingpos[0]),(self.endingpos[1]-self.startingpos[1])),(0,0,0))#draws the perimeter around graphed values

        #draws the text that displays the price of the stock
        text = bold40.render(f' {self.name}',(255,255,255))[0]
        screen.blit(text,(self.endingpos[0]+15,self.startingpos[1]+15))
        screen.blit(fontlist[40].render(f' ${round(self.pricepoints[-1][0],2)}',(255,255,255))[0],(self.endingpos[0]+10,self.endingpos[1]-40))    

        #Below is the price change text
        if self.graphrangeoptions[self.graphrange][1] > len(self.pricepoints):#if the amount of points we have in self.pricepoints is less than the amount needed for our graphing range then just use all of our points
            percentchange = round(self.pricepoints[-1][0]-self.pricepoints[0][0],2)

        else:#if the amount of points we have in self.pricepoints is greater than the amount needed for our graphing range then use the amount needed
            percentchange = round(self.pricepoints[-1][0]-self.pricepoints[-self.graphrangeoptions[self.graphrange][1]][1],2)
       
        color = (0,200,0) if percentchange >= 1 else (200,0,0)
        if type(self) == Stock:
            screen.blit(fontlist[40].render(f"{'+' if percentchange >= 0 else '-'}{percentchange}%",color)[0],(self.endingpos[0]+15,self.startingpos[1]+45))
        elif type(self) == self.Playerclass:
            screen.blit(fontlist[40].render(f"{'+' if percentchange >= 0 else '-'}{percentchange}%",color)[0],(self.endingpos[0]+15,self.startingpos[1]+80))

        if type(self) == self.Playerclass:#text displaying the cash
            screen.blit(fontlist[40].render(f'Cash ${round(self.cash,2)}',(255,255,255))[0],(self.endingpos[0]+15,self.startingpos[1]+50))