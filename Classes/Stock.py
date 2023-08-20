import pygame
from random import randint
import statistics
from pygame import gfxdraw
import time
from Defs import *
import numpy as np
import os
import timeit
import json
POINTSPERGRAPH = 100

class Stock():
    def __init__(self,name,startingvalue_range,volatility,Playerclass,window_offset,stocknames) -> None:
        
        self.winset = window_offset
        self.startingpos,self.endingpos = (0,0),(0,0)
        self.Playerclass = Playerclass
        self.starting_value_range = startingvalue_range
        self.name = name
        self.price = randint(*self.starting_value_range)#not used if there are points in any graph
        self.pricereset_time = None
        self.stocknames = stocknames
        #variables for graphing the stock 
        #make graphingrangeoptions a dict with the name of the option as the key and the value as the amount of points to show
        self.graphrangeoptions = {'recent':POINTSPERGRAPH*5,'hour':10800,'day':70200,'week':351000,'month':1_404_000,'year':16_884_000}
        # self.gra phrangeoptions = (('recent',466),('hour',10800),('day',70200),('week',351000),('month',1_404_000),('year',16_884_000),('all',None))
        self.graphtext = [fontlist[30].render(f'{text}',(200,0,0))[0] for text in ['R','H', 'D', 'W', 'M', 'Y', 'A']]
        self.graphrange = 'hour' #
        self.graphrangelists = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphfillvar = {key:0 for key in self.graphrangeoptions.keys()}# used to see when to add a point to a graph
        self.datafromfile()
        self.price = self.graphrangelists['recent'][-1]
        #yvaluefinder is a function that takes a value and returns the y value of the point - look in assets for pic of equation
        self.yvaluefinder = lambda point,minpoint,newgraph,graphheight,startingpos: int(self.endingpos[1]+((point-minpoint)*newgraph)-graphheight+30)
        
        #variables for the stock price+
        self.volatility = volatility
        self.bonustrendranges = [(140_400,421_200),(59400,81000),(8100,21600),(150,3600)]#the ranges for the time for each bonus trend
        # self.fill_graphs()
    
    def __str__(self) -> str:
        return f'{self.name}'
    def reset_trends(self):
        """Sets/resets the trends for the stock"""
        self.periodbonus = [randint(-5,5)/1000,randint(140_400,421_200)]# [%added to each movement, time up to 6 days for the period bonus (low as 2 days)]
        self.daybonus = [randint(-5,5)/1000,randint(59400,81000)]# [%added to each movement, time low as 5.5 hours high as 7.5 (remember 6.5 hours is 1 day)]
        self.hourlytrend = [randint(-20,20),randint(8100,21600)]# added to the volitility each movement,time low as 45 minutes, high as 2 hours
        self.minutetrend = [randint(-10,10),randint(150,3600)]# added to the volitility each movement, time low as 50 seconds, high as 20 minutes 
        self.bonustrends = [self.periodbonus,self.daybonus,self.hourlytrend,self.minutetrend]#this is used to make seeing if the time is out easier
    def datafromfile(self):
        """gets the data from each file and puts it into the graphlist"""
        for grange in self.graphrangelists.keys():# for each graph range, [recent,hour,day,week,month,year]
            with open(f'Assets/Stockdata/{self.name}/{grange}.json','r') as file:
                file.seek(0)# go to the start of the file
                contents = json.load(file)# load the contents of the file
                if contents:# if the file is not empty
                    self.graphrangelists[grange] = np.array(contents)# add the contents to the graphrangelists
                else:
                    self.graphrangelists[grange] = np.array([self.price])# if the file is empty then make the only data the current price
        with open(f'Assets/Stockdata/{self.name}/trends.json','r') as file:#get the trends from the trend file
            file.seek(0)
            contents = json.load(file)
            if contents:
                self.periodbonus,self.daybonus,self.hourlytrend,self.minutetrend = contents
            else:
                self.reset_trends()
    def save_data(self):
        for grange in self.graphrangelists.keys():# for each graph range, [recent,hour,day,week,month,year]
            with open(f'Assets/Stockdata/{self.name}/{grange}.json','w') as file:
                file.seek(0)# go to the start of the file
                file.truncate()# clear the file
                json.dump(self.graphrangelists[grange].tolist(),file)# write the new data to the file
        
        with open(f'Assets/Stockdata/{self.name}/trends.json','w') as file:
            file.seek(0)
            file.truncate()
            json.dump([self.periodbonus,self.daybonus,self.hourlytrend,self.minutetrend],file)



    def bankrupcy(self,drawn,screen:pygame.Surface=None):
        """returns False if stock is not bankrupt,don't need screen if drawn is False"""	
        if self.price < 0 and self.pricereset_time == None:#if stock goes bankrupt, and no time has been set
            self.pricereset_time = time.time()
            return False
        elif self.pricereset_time != None and time.time() > self.pricereset_time+5:#if stock goes bankrupt and 5 seconds have passed
            self.price = randint(*self.starting_value_range)
            self.reset_trends(); self.pricereset_time = None#reset the trends and the pricereset_time
            if drawn:
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(200,0,0))#draws the background of the graph red
            return False
        elif self.pricereset_time != None and time.time() < self.pricereset_time+5:#if stock goes bankrupt and less then 5 seconds have passed
            if drawn:
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(200,0,0))#draws the background of the graph red
                screen.blit(fontlist[40].render(f'BANKRUPT',(255,255,255))[0],(self.endingpos[0]+15,self.startingpos[1]+15))
            return False
        return True
    
    def stock_split(self,player):
        if self.price >= 2500:
            player.messagedict[f'{self.name} has split'] = (time.time(),(0,0,200))
            for grange in self.graphrangelists.keys():# for each graph range, [recent,hour,day,week,month,year]
                self.graphrangelists[grange] = np.array([point*0.5 for point in self.graphrangelists[grange]])
            self.price = self.price*0.5
            stock_quantity = len([stock for stock in player.stocks if stock[0] == self.name])
            if stock_quantity > 0:
                player.messagedict[f'You now have {stock_quantity*2} shares of {self.name}'] = (time.time(),(0,0,200))
                for stock in player.stocks.copy():
                    print(stock)
                    if stock[0] == self.name:
                        player.stocks.remove(stock)
                        player.stocks.append([stock[0],stock[1]*0.5,stock[2]])
                        player.stocks.append([stock[0],stock[1]*0.5,stock[2]])
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
    
    def update_price(self,player:object):
        if self.bankrupcy(False):#if stock is not bankrupt
            pass
        
        if type(self) == Stock:#making sure that it is a Stock object and that update is true
            self.price = self.addpoint(self.price)
            self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable
            self.update_range_graphs()
        else:
            stockvalues = sum([stock[2].price for stock in self.stocks])
            self.update_range_graphs(stockvalues)#updates the range graphs


    def rangecontrols(self,screen:pygame.Surface,player:object,stocklist, Mousebuttons):
        #draw 4 25/25 filled polygons in the top left corner of the graph with the last one's x pos being startingpos[0]-5
       for i in range(4):
    # add a small gap in between each button
            y1 = self.startingpos[1] + (i * 30)
            y2 = self.startingpos[1] + 25 + (i * 30)
            gfxdraw.filled_polygon(screen, [(self.startingpos[0], y1), self.startingpos, (self.startingpos[0], y2), (self.startingpos[0] - 25, y2), (self.startingpos[0] - 25, y1)], (0, 0, 0))
            # check for collisions on each using mousebuttons
            text = self.graphtext[i]
            text_rect = text.get_rect(center=((self.startingpos[0]+self.startingpos[0] - 25) // 2, (y1 + y2) // 2))
            screen.blit(text, text_rect)
            mousex,mousey = pygame.mouse.get_pos()
            if mousex > (self.startingpos[0]-5)-25 and mousex < (self.startingpos[0]-5) and mousey > (self.startingpos[1]+(i*25)) and mousey < (self.startingpos[1]+25+(i*25)):
                if Mousebuttons == 1:
                    self.graphrange = list(self.graphrangeoptions.keys())[i]
                    print('clicked',i)
    
    def update_range_graphs(self,stockvalues=0):

        for key,value in self.graphrangeoptions.items():
            condensefactor = value/POINTSPERGRAPH
            self.graphfillvar[key] += 1
            if self.graphfillvar[key] == int(condensefactor):#if enough points have passed to add a point to the graph (condensefactor is how many points must go by to add 1 point to the graph)
                #add the last point to the list
                self.graphfillvar[key] = 0
                self.graphrangelists[key] = np.append(self.graphrangelists[key],self.price+stockvalues)
            
            if len(self.graphrangelists[key]) > POINTSPERGRAPH:
                # print('deleting',key,len(self.graphrangelists[key]))
                self.graphrangelists[key] = np.delete(self.graphrangelists[key],0)

    def draw(self,screen:pygame.Surface,player:object,startingpos,endingpos,stocklist,Mousebuttons):

        if startingpos != self.startingpos or endingpos != self.endingpos:#if the starting or ending positions have changed
            #setting the starting and ending positions - where the graphs are located is constantly changing
            self.startingpos = (startingpos[0] - self.winset[0], startingpos[1] - self.winset[1])
            self.endingpos = (endingpos[0] - self.winset[0], endingpos[1] - self.winset[1])
        
        if type(self) == self.Playerclass:#if it is a Player object
            self.graph(stocklist)#graph the player networth
            self.message(screen)#display the messages
        

        if self.bankrupcy(True,screen=screen):#if stock is not bankrupt, first argument is drawn
            gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(60,60,60))#draws the background of the graph

        self.rangecontrols(screen,player,stocklist,Mousebuttons)#draws the range controls

        graphheight = (self.endingpos[1]-self.startingpos[1])/2# graphheight is the height of the graph
        graphwidth = (self.startingpos[0]-self.endingpos[0])

        #first need to find the x values that we want to graph (the points that are in the range of the graph and then reduce it to fit on the graph)
    
        
        graphingpoints = self.graphrangelists[self.graphrange]# putting the points for the current graph we are using in the graphingpoints

        # finding the min and max values of the graphingpoints
        minpoint = (np.amin(self.graphrangelists[self.graphrange]))
        maxpoint = (np.amax(self.graphrangelists[self.graphrange]))


        if minpoint != maxpoint:#prevents divide by zero error
            if int(num:=graphheight/(maxpoint-minpoint)) > graphheight:#if the newgraph is greater than the graphheight then set it to half the graphheight
                newgraph = graphheight/2
            else:
                newgraph = num

            addedvalue = (self.startingpos[1]+graphheight-30)# the value that is added to the y value of the point to make it fit on the graph
            # graphingpoints = np.array(graphingpoints)# makes the graphingpoints a numpy array - MIGHT BE ABLE TO REMOVE ------------------------------------------------------
            graphingpoints = (((graphheight)-((graphingpoints - minpoint)) * newgraph)) + addedvalue# Doing the math to make the points fit on the graph 

        # creating the spacing for the graph
        if len(self.graphrangelists[self.graphrange]) > 0 and len(self.graphrangelists[self.graphrange]) < graphwidth:
            spacing = graphwidth/len(self.graphrangelists[self.graphrange])
        else:
            spacing = 1

        graphpointlen = len(graphingpoints)# doing this before the iteration to save time
        for i,value in enumerate(graphingpoints):
            if i >= graphpointlen-1:
                # print(i)
                pass#if last one in list or i is too great then don't draw line
            else:

                nextvalue = graphingpoints[i+1]
                xpos = self.endingpos[0]

                gfxdraw.line(screen,xpos+int(i*spacing),int(value),xpos+int((i+1)*spacing),int(nextvalue),(255,255,255))


                
        #Everything below is after the graph is drawn
        gfxdraw.rectangle(screen,pygame.Rect(self.endingpos[0],self.startingpos[1],(self.startingpos[0]-self.endingpos[0]),(self.endingpos[1]-self.startingpos[1])),(0,0,0))#draws the perimeter around graphed values

        #draws the text that displays the price of the stock
        
        
        if type(self) == Stock:#text displaying the price, and the net worth
            screen.blit(fontlist[40].render(f' ${round(self.price,2)}',(255,255,255))[0],(self.endingpos[0]+10,self.endingpos[1]-40))    
            text = bold40.render(f' {self.name}',(255,255,255))[0]
        else:
            screen.blit(fontlist[40].render(f' Net Worth ${round(self.price+sum([stock[2].price for stock in player.stocks]),2)}',(255,255,255))[0],(self.endingpos[0]+10,self.endingpos[1]-40)) 
            text = bold40.render(f'Portfolio',(255,255,255))[0]

        screen.blit(text,(self.endingpos[0]+15,self.startingpos[1]+15))#draws the text that displays the name of the stock or the player

        #Below is the price change text
        # percentchange = round(((self.price - self.graphrangelists[self.graphrange][-2])/self.graphrangelists[self.graphrange][-2])*100,2)
        percentchange = round((1-(self.graphrangelists[self.graphrange][0]/self.graphrangelists[self.graphrange][-1]))*100,2)
       
        color = (0,200,0) if percentchange >= 1 else (200,0,0)
        if type(self) == Stock:
            screen.blit(fontlist[40].render(f"{'+' if percentchange >= 0 else '-'}{percentchange}%",color)[0],(self.endingpos[0]+15,self.startingpos[1]+45))
        elif type(self) == self.Playerclass:
            screen.blit(fontlist[40].render(f"{'+' if percentchange >= 0 else '-'}{percentchange}%",color)[0],(self.endingpos[0]+15,self.startingpos[1]+80))

        if type(self) == self.Playerclass:#text displaying the price
            screen.blit(fontlist[40].render(f'Cash ${round(self.price,2)}',(255,255,255))[0],(self.endingpos[0]+15,self.startingpos[1]+50))
    
        
