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
POINTSPERGRAPH = 200

class Stock():
    def __init__(self,name,startingvalue_range,volatility,Playerclass,window_offset,stocknames,color) -> None:
        self.color = color
        self.winset = window_offset
        self.startpos,self.endpos = (0,0),(0,0)
        self.Playerclass = Playerclass
        self.starting_value_range = startingvalue_range
        self.name = name
        # self.price = randint(*self.starting_value_range)#not used if there are points in any graph
        self.price = 100#not used if there are points in any graph
        self.pricereset_time = None
        self.stocknames = stocknames
        #variables for graphing the stock 
        #make graphingrangeoptions a dict with the name of the option as the key and the value as the amount of points to show
        self.graphrangeoptions = {'recent':POINTSPERGRAPH*5,'hour':10800,'day':70200,'week':351000,'month':1_404_000,'year':16_848_000}
        # self.gra phrangeoptions = (('recent',466),('hour',10800),('day',70200),('week',351000),('month',1_404_000),('year',16_884_000),('all',None))
        self.graphtext = [[fontlist[30].render(f'{text}',(200,0,0))[0] for text in ['R','H', 'D', 'W', 'M', 'Y', 'A']],[fontlist[55].render(f'{text}',(200,0,0))[0] for text in ['R','H', 'D', 'W', 'M', 'Y', 'A']]]
        
        self.graphrange = 'hour' #
        self.graphrangelists = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphfillvar = {key:0 for key in self.graphrangeoptions.keys()}# used to see when to add a point to a graph
        
        # self.bonustrendranges = [[(-1*i,i),(100000-(i*8325),500000-(i*41400))] for i in range(12)]
        self.bonustrendranges = [[(-1,1),(1,3600)] for i in range(12)]
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]
        self.datafromfile()
        self.price = self.graphrangelists['recent'][-1]
        
        self.nametext = bold40.render(f' {self.name}',(255,255,255))[0] if type(self) == Stock else bold40.render(f' Portfolio',(255,255,255))[0]
        self.pricetext = fontlist[40].render(f'Price $',(255,255,255))[0]
        #variables for the stock price+
        self.volatility = volatility
        self.recentrenders = {}# a dict of the renders of the recent prices
        # self.reset_trends()
    

    def __str__(self) -> str:
        return f'{self.name}'
    
    def reset_trends(self):
        """Sets/resets the trends for the stock"""
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]#resets the trends for each bonus trend
    
    def reset_graphs(self):
        """resets the graphs to be empty"""
        for i in ['recent','hour','day','week','month','year','trends']:
            file_path = f"Assets/Stockdata/{self}/{i}.json"
            with open(file_path, "w+") as f:
                json.dump([], f)
        newprice = randint(*self.starting_value_range)
        for grange in self.graphrangelists.keys():# for each graph range, [recent,hour,day,week,month,year], assign the new price to each graph
            self.graphrangelists[grange] = np.array([newprice])
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
                self.bonustrends = contents
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
            json.dump(self.bonustrends,file)



    def bankrupcy(self,drawn,screen:pygame.Surface=None):
        """returns False if stock is not bankrupt,don't need screen if drawn is False"""	
        if self.price < 0 and self.pricereset_time == None:#if stock goes bankrupt, and no time has been set
            self.pricereset_time = time.time()
            return False
        elif self.pricereset_time != None and time.time() > self.pricereset_time+5:#if stock goes bankrupt and 5 seconds have passed
            self.price = randint(*self.starting_value_range)
            self.reset_trends(); self.pricereset_time = None#reset the trends and the pricereset_time
            self.reset_graphs()
            if drawn:
                gfxdraw.filled_polygon(screen,[(self.endpos[0],self.startpos[1]),self.endpos,(self.startpos[0],self.endpos[1]),self.startpos],(200,0,0))#draws the background of the graph red
            return False
        elif self.pricereset_time != None and time.time() < self.pricereset_time+5:#if stock goes bankrupt and less then 5 seconds have passed
            if drawn:
                gfxdraw.filled_polygon(screen,[(self.endpos[0],self.startpos[1]),self.endpos,(self.startpos[0],self.endpos[1]),self.startpos],(200,0,0))#draws the background of the graph red
                screen.blit(fontlist[40].render(f'BANKRUPT',(255,255,255))[0],(self.endpos[0]+15,self.startpos[1]+15))
            return False
        return True
    
    def stock_split(self,player):
        if self.price >= 2500:
            player.messagedict[f'{self.name} has split'] = (time.time(),(0,0,200))
            for grange in self.graphrangelists.keys():# for each graph range, [recent,hour,day,week,month,year]
                self.graphrangelists[grange] = np.array([point*0.5 for point in self.graphrangelists[grange]])
            self.price = self.price*0.5
            stock_quantity = len([stock for stock in player.stocks if stock[0] == self])
            if stock_quantity > 0:
                player.messagedict[f'You now have {stock_quantity*2} shares of {self.name}'] = (time.time(),(0,0,200))
                for stock in player.stocks.copy():
                    print(stock)
                    if stock[0] == self:
                        player.stocks.remove(stock)
                        player.stocks.append([stock[0],stock[1]*0.5,stock[2]])
                        player.stocks.append([stock[0],stock[1]*0.5,stock[2]])
                print('stocks are',player.stocks)

    def addpoint(self,lastprice):
        """returns the new price of the stock"""
 
        for i,bonustrend in enumerate(self.bonustrends):
            if bonustrend[1] <= 0:#if the time is out
                self.bonustrends[i] = [randint(*self.bonustrendranges[i][0]),randint(*self.bonustrendranges[i][1])]

            else:
                bonustrend[1] -= 1
        total_trend = int(sum([trend[0] for trend in self.bonustrends]))
        highvolitity = self.volatility+(total_trend if total_trend >= 0 else -1*(total_trend//2))
        lowvolitity = -self.volatility+(total_trend if total_trend < 0 else -1*(total_trend//2))
        
        return lastprice * (1+(randint(lowvolitity,highvolitity)/100000))#returns the new price of the stock
    
    def update_price(self,player:object):
        if self.bankrupcy(False):#if stock is not bankrupt
            pass
        
        if type(self) == Stock:#making sure that it is a Stock object and that update is true
            self.price = self.addpoint(self.price)#updates the price of the stock
            # self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable
            self.update_range_graphs()
        else:
            # stockvalues = sum([stock[0].price*stock[2] for stock in self.stocks])
            self.update_range_graphs(self.get_Networth())#updates the range graphs


    def rangecontrols(self,screen:pygame.Surface,Mousebuttons):
        """draws the range controls and checks for clicks"""
        
        #draw 4 25/25 filled polygons in the top left corner of the graph with the last one's x pos being startpos[0]-5
        # self.startpos[0]
        box_xy = (self.startpos[0]-self.endpos[0])//22.3#the x and y value of the box (dimensions of the box)
        leftshift = (self.startpos[0]-self.endpos[0])//10#the amount of blank space to be left on the left side of the graph
        for i in range(6):

            x1 = self.startpos[0] - leftshift-box_xy - 5 - (i * (box_xy+(box_xy//6)))#the x value of the top left corner of the box
            x2 = self.startpos[0] - leftshift - 5 - (i * (box_xy+(box_xy//6)))#the x value of the top right corner of the box
            y1 = self.startpos[1] + 10#the y value of the top left corner of the box
            y2 = self.startpos[1] + 10+box_xy#the y value of the bottom left corner of the box
            if self.graphrange == list(self.graphrangeoptions.keys())[i]:
                gfxdraw.filled_polygon(screen, [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], (200, 200, 200))
            else:
                gfxdraw.filled_polygon(screen, [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], (60, 60, 60))
            # check for collisions on each using mousebuttons
            if box_xy > 35:#if the box is big enough to fit the larger text
                text = self.graphtext[1][i]#use the larger text
            else:
                text = self.graphtext[0][i]#use the smaller text

            text_rect = text.get_rect(center=((x1+x2)//2,(y1+y2)//2))#the center of the text is the center of the box
            screen.blit(text, text_rect)
            mousex,mousey = pygame.mouse.get_pos()
            if pygame.Rect(x1,y1,box_xy,box_xy).collidepoint(mousex,mousey):#if the mouse is over the box
                if Mousebuttons == 1:
                    self.graphrange = list(self.graphrangeoptions.keys())[i]
                    print('clicked',i)
    def mouseover(self,screen:pygame.Surface,graphpoints,spacing,blnkspacey):
        """displays the price of the stock when the mouse is over the graph"""
        mousex,mousey = pygame.mouse.get_pos()
        if pygame.Rect(self.endpos[0],self.startpos[1],(self.startpos[0]-self.endpos[0]),(self.endpos[1]-self.startpos[1])).collidepoint(mousex,mousey):
            pos = (mousex-self.endpos[0])//spacing
            if pos < len(self.graphrangelists[self.graphrange]):
                text1 = fontlist[30].render(f'${self.graphrangelists[self.graphrange][int(pos)]:,.2f}',(255,255,255))[0]
                screen.blit(text1,(mousex,graphpoints[int(pos)]))
                percentchange = round(((self.graphrangelists[self.graphrange][int(pos)]/self.graphrangelists[self.graphrange][0])-1)*100,2)
                color = (0,205,0) if percentchange >= 0 else (205,0,0)
                if percentchange == 0: color = (205,205,205)
                screen.blit(fontlist[30].render(f'{percentchange:,.2f}%',color)[0], (mousex,graphpoints[int(pos)]+text1.get_height()+5))
                gfxdraw.line(screen,mousex,self.endpos[1]-blnkspacey,mousex,self.startpos[1],(255,255,255))


    def update_range_graphs(self,stockvalues=0):

        for key,value in self.graphrangeoptions.items():
            condensefactor = value/POINTSPERGRAPH
            self.graphfillvar[key] += 1
            if self.graphfillvar[key] == int(condensefactor):#if enough points have passed to add a point to the graph (condensefactor is how many points must go by to add 1 point to the graph)
                #add the last point to the list
                self.graphfillvar[key] = 0
                if type(self) == Stock:
                    self.graphrangelists[key] = np.append(self.graphrangelists[key],self.price)
                else:
                    self.graphrangelists[key] = np.append(self.graphrangelists[key],stockvalues)
            
            if len(self.graphrangelists[key]) > POINTSPERGRAPH:
                # print('deleting',key,len(self.graphrangelists[key]))
                self.graphrangelists[key] = np.delete(self.graphrangelists[key],0)

    def baredraw(self,screen,startpos,endpos,graphrange):
        """Draws only the graph of the stock - uses the graphrange,startpos, and endpos parameter, not self.graphrange,self.startpos, and self.endpos"""
        startpos = (int(startpos[0] - self.winset[0]), int(startpos[1] - self.winset[1]))
        endpos = (int(endpos[0] - self.winset[0]), int(endpos[1] - self.winset[1]))
        
        if self.bankrupcy(True,screen=screen):#if stock is not bankrupt, first argument is drawn
            percentchange = round(((self.graphrangelists[graphrange][-1]/self.graphrangelists[graphrange][0])-1)*100,2)
            color = (0,55,0) if percentchange >= 0 else (55,0,0)
            gfxdraw.filled_polygon(screen, [(endpos[0], startpos[1]), endpos, (startpos[0], endpos[1]), startpos],color)  # draws the perimeter around graphed values
            gfxdraw.filled_polygon(screen,[(endpos[0],startpos[1]),(endpos[0],endpos[1]),(startpos[0],endpos[1]),(startpos[0],startpos[1])],(15,15,15))#draws the background of the graph

        graphheight = ((endpos[1]-startpos[1])//2)
        graphwidth = (startpos[0]-endpos[0])
        graphingpoints = self.graphrangelists[graphrange]
        minpoint = (np.amin(self.graphrangelists[graphrange]))
        maxpoint = (np.amax(self.graphrangelists[graphrange]))        

        if minpoint != maxpoint:#prevents divide by zero error
            yScale = graphheight/(maxpoint-minpoint)#the amount of pixels per point with the y axis

            yOffset = (startpos[1]+graphheight)-10# slides the graph up on the screen to fit

            graphingpoints = (((graphheight)-((graphingpoints - minpoint)) * yScale)) + yOffset# Doing the math to make the points fit on the graph 

        spacing = graphwidth/len(self.graphrangelists[graphrange])#the spacing between each point

        graphpointlen = len(graphingpoints)# doing this before the iteration to save time
        for i,value in enumerate(graphingpoints):
            if i >= graphpointlen-1:
                pass#if last one in list or i is too great then don't draw line
            else:
                nextvalue = graphingpoints[i+1]
                xpos = endpos[0]
                gfxdraw.line(screen,xpos+int(i*spacing),int(value),xpos+int((i+1)*spacing),int(nextvalue),(255,255,255))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(endpos[0], startpos[1], (startpos[0] - endpos[0]),(endpos[1] - startpos[1])), 5)

    def draw(self,screen:pygame.Surface,player:object,startpos,endpos,stocklist,Mousebuttons,rangecontrols=True):
        """Draws the graph of the stock along with the range controls, price lines, and the name"""
        if startpos != self.startpos or endpos != self.endpos:#if the starting or ending positions have changed
            #setting the starting and ending positions - where the graphs are located is constantly changing
            # startingpos is the top left corner of the graph, endingpos is the bottom right corner of the graph
            self.startpos = (startpos[0] - self.winset[0], startpos[1] - self.winset[1])
            self.endpos = (endpos[0] - self.winset[0], endpos[1] - self.winset[1])
        
        if type(self) == self.Playerclass:#if it is a Player object
            self.graph(stocklist)#graph the player networth
            self.message(screen)#display the messages
        
        blnkspacex = (self.startpos[0]-self.endpos[0])//10#the amount of blank space to be left on the right side of the graph for x
        blnkspacey = (self.endpos[1]-self.startpos[1])//10#the amount of blank space to be left on the right side of the graph for y

        if self.bankrupcy(True,screen=screen):#if stock is not bankrupt, first argument is drawn
            percentchange = round(((self.graphrangelists[self.graphrange][-1]/self.graphrangelists[self.graphrange][0])-1)*100,2)
            color = (0,55,0) if percentchange >= 0 else (55,0,0)

            gfxdraw.filled_polygon(screen, [(self.endpos[0], self.startpos[1]), self.endpos, (self.startpos[0], self.endpos[1]), self.startpos],color)  # draws the perimeter around graphed values
            gfxdraw.filled_polygon(screen,[(self.endpos[0],self.startpos[1]),(self.endpos[0],self.endpos[1]-blnkspacey),(self.startpos[0]-blnkspacex,self.endpos[1]-blnkspacey),(self.startpos[0]-blnkspacex,self.startpos[1])],(15,15,15))#draws the background of the graph
        
        if rangecontrols:# if the range controls are drawn
            self.rangecontrols(screen,Mousebuttons)#draws the range controls

        # Kind of deceptive with the name, but graphheight is not acually the full height of the graph - it is divided by 1.5 and then the blank space is subtracted
        graphheight = ((self.endpos[1]-self.startpos[1])//1.5)-blnkspacex
        graphwidth = (self.startpos[0]-self.endpos[0])-blnkspacex

        # putting the points for the current graph we are using in the graphingpoints
        graphingpoints = self.graphrangelists[self.graphrange]

        # finding the min and max values of the graphingpoints
        minpoint = (np.amin(self.graphrangelists[self.graphrange]))
        maxpoint = (np.amax(self.graphrangelists[self.graphrange]))        

        if abs(minpoint-maxpoint) > 0.1:#prevents divide by zero error
            yScale = graphheight/(maxpoint-minpoint)#the amount of pixels per point with the y axis

            yOffset = (self.startpos[1]+graphheight-(blnkspacey*3.5))+blnkspacey# slides the graph up on the screen to fit

            graphingpoints = (((graphheight)-((graphingpoints - minpoint)) * yScale)) + yOffset# Doing the math to make the points fit on the graph 

            spacing = graphwidth/len(self.graphrangelists[self.graphrange])#the spacing between each point

            graphpointlen = len(graphingpoints)# doing this before the iteration to save time
            for i,value in enumerate(graphingpoints):
                if i >= graphpointlen-1:
                    pass#if last one in list or i is too great then don't draw line
                else:
                    nextvalue = graphingpoints[i+1]
                    xpos = self.endpos[0]
                    gfxdraw.line(screen,xpos+int(i*spacing),int(value),xpos+int((i+1)*spacing),int(nextvalue),(255,255,255))

            """text that displays the price of the stock and the lines that go across the graph"""
            sortedlist = self.graphrangelists[self.graphrange].copy();sortedlist.sort()# first makes a copy of the list, then sorts the list
            for i in range(4):
                lenpos = int((len(self.graphrangelists[self.graphrange])-1)*(i/3))#Position based purely on the length of the current graph size
                point = sortedlist[lenpos]#using the sorted list so an even amount of price values are displayed
                
                #gets the position of the point in the graphingpoints (the y values) - the sorted list moves the points around so the index of the point is different
                yvalpos = np.where(self.graphrangelists[self.graphrange] == point)[0][0]
                
                # -------render the text for the graph----------
                # if len(self.recentrenders) > i and round(point,2) in self.recentrenders:
                #     text = self.recentrenders[round(point,2)]# reuse old renders if possible
                #     self.recentrenders.pop(round(point,2))# remove the text from the recentrenders
                #     self.recentrenders[round(point,2)] = text# add the text back to the recentrenders - so it is at the end of the dict (doesn't get deleted)

                # else:# if the text is not in the recentrenders or recent renders doesn't have enough texts
                #     text = fontlist[30].render(f'{point:,.2f}',(255,255,255))[0]# render the text
                #     self.recentrenders[round(point,2)] = text# add the text to the recentrenders
                
                # for i in range(len(self.recentrenders)-4):# if recentrenders has more then 4 texts
                #     self.recentrenders.pop(list(self.recentrenders)[0])# remove the first text from recentrenders
                        
                # draw the text and the lines
                text = num_renderer(point, 30, (255,255,255))
                gfxdraw.line(screen,self.endpos[0]+5,int(graphingpoints[yvalpos]),self.startpos[0]-5,int(graphingpoints[yvalpos]),(150,150,150))
                # text_rect = text.get_rect(left=((self.startpos[0]-text.get_width()),(graphingpoints[yvalpos]-text.get_height()//2-5)))
                screen.blit(text,(self.startpos[0]-text.get_width(),(graphingpoints[yvalpos]-text.get_height()//2-5)))
                
        else:#if the minpoint and maxpoint are the same
            gfxdraw.line(screen,self.endpos[0],int(self.startpos[1]+graphheight),self.startpos[0]-blnkspacex,int(self.startpos[1]+graphheight),(255,255,255))#draws a line across the graph
            spacing = graphwidth/len(self.graphrangelists[self.graphrange])#the spacing between each point
            graphingpoints = [self.startpos[1]+graphheight]*(graphwidth)#makes the graphingpoints a list of the same y value
            
        # black outline of the graph
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.endpos[0], self.startpos[1], (self.startpos[0] - self.endpos[0]),(self.endpos[1] - self.startpos[1])), 5)
        

        #draws the text that displays the price of the stock
        if type(self) == Stock:#text displaying the price, and the net worth
            # pricetext = fontlist[40].render(f'{self.price:,.2f}',(255,255,255))[0]
            pricetext = num_renderer(self.price, 45, (255,255,255))
            textwidth = pricetext.get_width()+20+self.pricetext.get_width(); textheight = pricetext.get_height()
            textx = self.endpos[0]+20; texty = self.endpos[1]-55
            # use textx, and texty to draw the polygon
            gfxdraw.filled_polygon(screen,[(textx-15,texty-5),(textx+textwidth,texty-5),(textx+textwidth+10,texty+textheight+5),(textx,texty+textheight+5)],(60,60,60))
            screen.blit(self.pricetext,(textx,texty))#draws the word price
            screen.blit(pricetext,(textx+self.pricetext.get_width(),texty))# draws the price
                    
        else:
            # goes off the current price of the stock, not the original value stored in the stock object
            screen.blit(fontlist[40].render(f' Net Worth ${player.get_Networth():,.2f}',(255,255,255))[0],(self.endpos[0]+10,self.endpos[1]-40)) 
            

        screen.blit(self.nametext,(self.endpos[0]+15,self.startpos[1]+15))#draws the text that displays the name of the stock or the player

        #Below is the price change text
        # percentchange = round(((self.price - self.graphrangelists[self.graphrange][-2])/self.graphrangelists[self.graphrange][-2])*100,2)
        percentchange = round(((self.graphrangelists[self.graphrange][-1]/self.graphrangelists[self.graphrange][0])-1)*100,2)
       
        color = (0,200,0) if percentchange >= 0 else (200,0,0)
        
        if type(self) == Stock:
            change_text = '+' + str(percentchange) + '%' if percentchange >= 0 else '-' + str(percentchange) + '%'
            change_text_rendered = fontlist[40].render(change_text, color)[0]
            screen.blit(change_text_rendered, (self.endpos[0]+15, self.startpos[1]+45))
        elif type(self) == self.Playerclass:
            change_text = '+' + str(percentchange) + '%' if percentchange >= 0 else '-' + str(percentchange) + '%'
            change_text_rendered = fontlist[40].render(change_text, color)[0]
            screen.blit(change_text_rendered, (self.endpos[0]+15, self.startpos[1]+80))

        if type(self) == self.Playerclass:
            cash_text = fontlist[40].render(f'Cash ${self.cash:,.2f}', (255,255,255))[0]
            screen.blit(cash_text, (self.endpos[0]+15, self.startpos[1]+50))
        
        self.mouseover(screen,graphingpoints,spacing,blnkspacey)#displays the price of the stock when the mouse is over the graph
                
        
