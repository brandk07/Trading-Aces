import pygame
from random import randint
import statistics
from pygame import gfxdraw
import time
from Defs import *
import numpy as np
import timeit
POINTSPERGRAPH = 500

class Stock():
    def __init__(self,name,startingvalue_range,volatility,Playerclass,window_offset,stocknames,currenttime) -> None:
        
        self.winset = window_offset
        self.pricepoints = [[randint(*startingvalue_range),currenttime]]
        self.pricepoints = np.array(self.pricepoints,dtype=object)
        self.startingpos,self.endingpos = (0,0),(0,0)
        self.Playerclass = Playerclass
        self.starting_value_range = startingvalue_range
        self.name = name
        self.pricereset_time = None
        self.stocknames = stocknames
        #variables for graphing the stock 
        #make graphingrangeoptions a dict with the name of the option as the key and the value as the amount of points to show
        self.graphrangeoptions = {'recent':500,'hour':10800,'day':70200,'week':351000,'month':1_404_000,'year':16_884_000}
        # self.gra phrangeoptions = (('recent',466),('hour',10800),('day',70200),('week',351000),('month',1_404_000),('year',16_884_000),('all',None))
        self.graphrange = 'hour' #
        self.graphrangelists = {key:np.array([self.pricepoints[-1][0]],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        
        #yvaluefinder is a function that takes a value and returns the y value of the point - look in assets for pic of equation
        # x,graphheight,medianpoint,graphsize,startingpos
        # self.yvaluefinder = lambda vars: int(vars[1]+(((vars[2]-vars[0])/vars[3])*vars[1])+vars[4][1])
        #  vars = [point,minpoint,maxpoint,graphheight]
        # self.yvaluefinder = lambda point,minpoint,maxpoint,graphheight: int(vars[0]*((vars[1]-vars[2])/vars[3]))
        # self.yvaluefinder = lambda point,minpoint,maxpoint,graphheight: int((point-minpoint)*graphheight/(maxpoint-minpoint))
        # self.yvaluefinder = lambda point,minpoint,maxpoint,graphheight: int((graphheight)*point/(maxpoint-minpoint))
        # self.yvaluefinder = lambda point,minpoint,maxpoint,graphheight,startingpos: int((point-minpoint)*((graphheight/(maxpoint-minpoint)))+startingpos[1])
        # self.yvaluefinder = lambda point,minpoint,newgraph,startingpos: int(((point-minpoint)*newgraph)+startingpos[1])
        self.yvaluefinder = lambda point,minpoint,newgraph,graphheight,startingpos: int(((point-minpoint)*newgraph)+startingpos[1]+graphheight-30)
        
        # self.yvaluefinder = lambda point,minpoint,maxpoint,graphheight: int(point*((maxpoint-minpoint)/(graphheight)))
        #variables for the stock price+
        self.volatility = volatility
        self.periodbonus = [randint(-5,5)/1000,randint(140_400,421_200)]# [%added to each movement, time up to 6 days for the period bonus (low as 2 days)]
        self.daybonus = [randint(-5,5)/1000,randint(59400,81000)]# [%added to each movement, time low as 5.5 hours high as 7.5 (remember 6.5 hours is 1 day)]
        self.hourlytrend = [randint(-20,20),randint(8100,21600)]# added to the volitility each movement,time low as 45 minutes, high as 2 hours
        self.minutetrend = [randint(-10,10),randint(150,3600)]# added to the volitility each movement, time low as 50 seconds, high as 20 minutes 
        self.bonustrends = [self.periodbonus,self.daybonus,self.hourlytrend,self.minutetrend]#this is used to make seeing if the time is out easier
        self.bonustrendranges = [(140_400,421_200),(59400,81000),(8100,21600),(150,3600)]#the ranges for the time for each bonus trend

            
    def __str__(self) -> str:
        return f'{self.name}'
    
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
            newpoint = np.array([newprice, gametime],dtype=object)
            # self.pricepoints.append([newprice,gametime])#if update is true then add a new point to the graph
            self.pricepoints = np.vstack([self.pricepoints, newpoint])
            # self.pricepoints = np.append(self.pricepoints,np.array([newprice,np.array(gametime)]),dtype=object)#if update is true then add a new point to the graph
            # self.pricepoints = np.vstack([self.pricepoints, [newprice, gametime]]) # vfertically stack the new price and gametime values as a new row in the self.pricepoints array
            # print(self.pricepoints)
            self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable
            self.update_range_graphs()#updates the range graphs


    def rangecontrols(self,screen:pygame.Surface,player:object,stocklist):
        #draw 4 25/25 filled polygons
        for i in range(4):
            gfxdraw.filled_polygon(screen,[(self.startingpos[0]+i*25,self.startingpos[1]),(self.startingpos[0]+i*25,self.endingpos[1]),(self.startingpos[0]+i*25+25,self.endingpos[1]),(self.startingpos[0]+i*25+25,self.startingpos[1])],(0,0,0))
    
    def update_range_graphs(self):

        for key,value in self.graphrangeoptions.items():
            # print(value,'is the value')
            # print(graphxsize,'is the graphxsize')
            condensefactor = value/POINTSPERGRAPH
            # print(condensefactor,'is the condensefactor')
            # print(len(self.pricepoints),'is the len of pricepoints')
            # print(len(self.graphrangelists[key]),'is the len of graphrangelists')
            # print(condensefactor,'is the condensefactor')
            # print((len(self.pricepoints)/condensefactor),len(self.graphrangelists[key]), (len(self.pricepoints)/condensefactor) > len(self.graphrangelists[key]))
            if (len(self.pricepoints)/condensefactor) > len(self.graphrangelists[key]):#if the amount of points that should be in the list is greater than the amount of points in the list
                # self.graphrangelists[key].append(self.pricepoints[-1][0])#add the last point to the list
                self.graphrangelists[key] = np.vstack([self.graphrangelists[key], self.pricepoints[-1][0]])
            if len(self.graphrangelists[key]) > POINTSPERGRAPH:
                # print('deleting',key,len(self.graphrangelists[key]))
                self.graphrangelists[key] = np.delete(self.graphrangelists[key],0)
                # self.graphrangelists[key].pop(0)

    def draw(self,screen:pygame.Surface,player:object,startingpos,endingpos,stocklist):
        start_time = timeit.default_timer()
        if startingpos != self.startingpos or endingpos != self.endingpos:#if the starting or ending positions have changed
            #setting the starting and ending positions - where the graphs are located is constantly changing
            self.startingpos = (startingpos[0] - self.winset[0], startingpos[1] - self.winset[1])
            self.endingpos = (endingpos[0] - self.winset[0], endingpos[1] - self.winset[1])
        
        if type(self) == self.Playerclass:#if it is a Player object
            self.graph(stocklist)#graph the player networth
            self.message(screen)#display the messages
        

        if self.bankrupcy(True,screen=screen):#if stock is not bankrupt, first argument is drawn
            gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(60,60,60))#draws the background of the graph

        # self.rangecontrols(screen,player,stocklist)#draws the range controls

        graphheight = (self.endingpos[1]-self.startingpos[1])/2# graphheight is the height of the graph
        graphwidth = (self.startingpos[0]-self.endingpos[0])

        #first need to find the x values that we want to graph (the points that are in the range of the graph and then reduce it to fit on the graph)
    
        
        graphingpoints = self.graphrangelists[self.graphrange]
        end_time = timeit.default_timer()
        # print(f"Execution times first one: {end_time - start_time} seconds")
        print(len(graphingpoints))
        start_time = timeit.default_timer()
        # finding the min and max values of the graphingpoints
        minpoint = (np.amin(self.graphrangelists[self.graphrange]))
        maxpoint = (np.amax(self.graphrangelists[self.graphrange]))
        end_time = timeit.default_timer()
        # print(f"Execution times 3: {end_time - start_time} seconds")
        start_time = timeit.default_timer()
        if minpoint != maxpoint:#prevents divide by zero error
            # [point,minpoint,maxpoint,graphheight,startingpos]
            if int(num:=graphheight/(maxpoint-minpoint)) > graphheight:
                newgraph = graphheight/2
            else:
                newgraph = num
            end_time = timeit.default_timer()
            # print(f"Execution times first section: {end_time - start_time} seconds")

            start_time = timeit.default_timer()
            # graphingpoints = [int(self.yvaluefinder(point,minpoint,newgraph,graphheight,self.startingpos)) for point in graphingpoints]
            addedvalue = (self.startingpos[1]+graphheight-30)
            # graphingpoints = [int(((point-minpoint)*newgraph)+addedvalue) for point in graphingpoints]

            graphingpoints = np.array(graphingpoints)
            graphingpoints = ((graphingpoints - minpoint) * newgraph) + addedvalue
            # graphingpoints = graphingpoints.astype(int)
            # Execution times 2ed section: 0.0034706999999940535 seconds
            end_time = timeit.default_timer()
            # print(f"Execution times 2ed section: {end_time - start_time} seconds")
        start_time = timeit.default_timer()
        if len(self.graphrangelists[self.graphrange]) > 0 and len(self.graphrangelists[self.graphrange]) < graphwidth:
            spacing = graphwidth/len(self.graphrangelists[self.graphrange])
        else:
            spacing = 1

        end_time = timeit.default_timer()
        # print(f"Execution times last section: {end_time - start_time} seconds")
        start_time = timeit.default_timer()

        # 
        if len(self.pricepoints) % 100 == 0:
            print(len(self.pricepoints))
        graphpointlen = len(graphingpoints)
        for i,value in enumerate(graphingpoints):
            if i >= graphpointlen-1:
                # print(i)
                pass#if last one in list or i is too great then don't draw line
            else:

                nextvalue = graphingpoints[i+1]
                xpos = self.endingpos[0]

                gfxdraw.line(screen,xpos+int(i*spacing),int(value),xpos+int((i+1)*spacing),int(nextvalue),(255,255,255))
        end_time = timeit.default_timer()
        # print(f"Execution times last: {end_time - start_time} seconds")

                
        #Everything below is after the graph is drawn
        gfxdraw.rectangle(screen,pygame.Rect(self.endingpos[0],self.startingpos[1],(self.startingpos[0]-self.endingpos[0]),(self.endingpos[1]-self.startingpos[1])),(0,0,0))#draws the perimeter around graphed values

        #draws the text that displays the price of the stock
        text = bold40.render(f' {self.name}',(255,255,255))[0]
        screen.blit(text,(self.endingpos[0]+15,self.startingpos[1]+15))
        screen.blit(fontlist[40].render(f' ${round(self.pricepoints[-1][0],2)}',(255,255,255))[0],(self.endingpos[0]+10,self.endingpos[1]-40))    

        #Below is the price change text
        if self.graphrangeoptions[self.graphrange] > len(self.pricepoints):#if the amount of points we have in self.pricepoints is less than the amount needed for our graphing range then just use all of our points
            percentchange = round(self.pricepoints[-1][0]-self.pricepoints[0][0],2)

        else:#if the amount of points we have in self.pricepoints is greater than the amount needed for our graphing range then use the amount needed
            percentchange = round(self.pricepoints[-1][0]-self.pricepoints[-self.graphrangeoptions[self.graphrange]][0],2)
       
        color = (0,200,0) if percentchange >= 1 else (200,0,0)
        if type(self) == Stock:
            screen.blit(fontlist[40].render(f"{'+' if percentchange >= 0 else '-'}{percentchange}%",color)[0],(self.endingpos[0]+15,self.startingpos[1]+45))
        elif type(self) == self.Playerclass:
            screen.blit(fontlist[40].render(f"{'+' if percentchange >= 0 else '-'}{percentchange}%",color)[0],(self.endingpos[0]+15,self.startingpos[1]+80))

        if type(self) == self.Playerclass:#text displaying the cash
            screen.blit(fontlist[40].render(f'Cash ${round(self.cash,2)}',(255,255,255))[0],(self.endingpos[0]+15,self.startingpos[1]+50))
    
        
