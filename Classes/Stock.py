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
from Classes.imports.Graph import Graph
POINTSPERGRAPH = 200

class Stock():
    def __init__(self,name,startingvalue_range,volatility,Playerclass,stocknames,color) -> None:
        self.color = color
        # (coords[0]+wh[0],coords[1]),(coords[0],coords[1]+wh[1]) = (0,0),(0,0)
        # self.coords,self.wh = (0,0),(0,0)
        self.Playerclass = Playerclass
        self.starting_value_range = startingvalue_range
        self.name = name
        # self.price = randint(*self.starting_value_range)#not used if there are points in any graph
        self.price = 100#not used if there are points in any graph
        self.pricereset_time = None
        self.stocknames = stocknames
        #variables for graphing the stock 
        #make graphingrangeoptions a dict with the name of the option as the key and the value as the amount of points to show
        self.graphrangeoptions = {"1H":3600,"1D":23_400,"1W":117_000,"1M":489_450,"3M":1_468_350,"1Y":5_873_400}
        
        self.graphrange = '1H' # H, D, W, M, 3M, Y
        self.graphrangelists = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphfillvar = {key:0 for key in self.graphrangeoptions.keys()}# used to see when to add a point to a graph
        
        # self.bonustrendranges = [[(-1*i,i),(100000-(i*8325),500000-(i*41400))] for i in range(12)]
        self.bonustrendranges = [[(-1,1),(1,3600)] for i in range(12)]
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]
        self.datafromfile()
        self.price = self.graphrangelists['1H'][-1]
        
        #variables for the stock price+
        self.volatility = volatility
        self.recentrenders = {}# a dict of the renders of the recent prices
        # self.reset_trends()
        self.graph = Graph()
    

    def __str__(self) -> str:
        return f'{self.name}'
    
    def reset_trends(self):
        """Sets/resets the trends for the stock"""
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]#resets the trends for each bonus trend
    
    def reset_graphs(self):
        """resets the graphs to be empty"""
        for i in ["1H","1D","1W","1M","3M","1Y","trends"]:
            file_path = f"Assets/Stockdata/{self}/{i}.json"
            with open(file_path, "w+") as f:
                json.dump([], f)
        newprice = randint(*self.starting_value_range)
        for grange in self.graphrangelists.keys():# for each graph range, ["1H","1D","1W","1M","3M","1Y","trends"], assign the new price to each graph
            self.graphrangelists[grange] = np.array([newprice])
    def datafromfile(self):
        """gets the data from each file and puts it into the graphlist"""
        for grange in self.graphrangelists.keys():# for each graph range, ["1H","1D","1W","1M","3M","1Y","trends"]
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
        for grange in self.graphrangelists.keys():# for each graph range, ["1H","1D","1W","1M","3M","1Y","trends"]
            with open(f'Assets/Stockdata/{self.name}/{grange}.json','w') as file:
                file.seek(0)# go to the start of the file
                file.truncate()# clear the file
                json.dump(self.graphrangelists[grange].tolist(),file)# write the new data to the file
        
        with open(f'Assets/Stockdata/{self.name}/trends.json','w') as file:
            file.seek(0)
            file.truncate()
            json.dump(self.bonustrends,file)



    def bankrupcy(self,drawn,coords=None,wh=None,screen:pygame.Surface=None):
        """returns False if stock is not bankrupt,don't need screen if drawn is False"""	
        if self.price < 0 and self.pricereset_time == None:#if stock goes bankrupt, and no time has been set
            self.pricereset_time = time.time()
            return False
        elif self.pricereset_time != None and time.time() > self.pricereset_time+5:#if stock goes bankrupt and 5 seconds have passed
            self.price = randint(*self.starting_value_range)
            self.reset_trends(); self.pricereset_time = None#reset the trends and the pricereset_time
            self.reset_graphs()
            if drawn:
                gfxdraw.filled_polygon(screen,[(coords[0],coords[1]),(coords[0],coords[1]+wh[1]),(coords[0]+wh[0],coords[1]+wh[1]),(coords[0]+wh[0],coords[1])],(200,0,0))#draws the background of the graph red
            return False
        elif self.pricereset_time != None and time.time() < self.pricereset_time+5:#if stock goes bankrupt and less then 5 seconds have passed
            if drawn:
                gfxdraw.filled_polygon(screen,[(coords[0],coords[1]),(coords[0],coords[1]+wh[1]),(coords[0]+wh[0],coords[1]+wh[1]),(coords[0]+wh[0],coords[1])],(200,0,0))#draws the background of the graph red
                screen.blit(fontlist[40].render(f'BANKRUPT',(255,255,255))[0],(coords[0]+15,coords[1]+15))
            return False
        return True
    
    def stock_split(self,player):
        if self.price >= 2500:
            player.messagedict[f'{self.name} has split'] = (time.time(),(0,0,200))
            for grange in self.graphrangelists.keys():# for each graph range, ["1H","1D","1W","1M","3M","1Y","trends"]
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


    def rangecontrols(self,screen:pygame.Surface,Mousebuttons,blnkspacey,coords,wh):
        """draws the range controls and checks for clicks"""
        x,y = coords[0]+wh[0]-int((coords[1]+wh[1]-coords[1])/20),coords[1]+wh[1]-blnkspacey*.75
        for i in range(len(self.graphrangeoptions),0,-1):
            name = list(self.graphrangeoptions)[i-1]
            text = s_render(name,int((coords[1]+wh[1]-coords[1])/15),(255,255,255) if self.graphrange == name else (120,120,120))
            screen.blit(text,(x-(text.get_width()/2),y))
            if pygame.Rect(x - text.get_width() / 2 - 2, y - 2, text.get_width() + 10, text.get_height() + 10).collidepoint(pygame.mouse.get_pos()):
                if Mousebuttons == 1:
                    self.graphrange = name
            x -= text.get_width()+int((coords[1]+wh[1]-coords[1])/40)



    def mouseover(self,screen:pygame.Surface,graphpoints,spacing,blnkspacey,coords,wh):
        """displays the price of the stock when the mouse is over the graph"""
        mousex,mousey = pygame.mouse.get_pos()
        if pygame.Rect(coords[0],coords[1],(coords[0]+wh[0]-coords[0]),(coords[1]+wh[1]-coords[1])).collidepoint(mousex,mousey):
            pos = (mousex-coords[0])//spacing
            if pos < len(self.graphrangelists[self.graphrange]):
                text1 = fontlist[30].render(f'${self.graphrangelists[self.graphrange][int(pos)]:,.2f}',(255,255,255))[0]
                screen.blit(text1,(mousex,graphpoints[int(pos)]))
                percentchange = round(((self.graphrangelists[self.graphrange][int(pos)]/self.graphrangelists[self.graphrange][0])-1)*100,2)
                color = (0,205,0) if percentchange >= 0 else (205,0,0)
                if percentchange == 0: color = (205,205,205)
                screen.blit(fontlist[30].render(f'{percentchange:,.2f}%',color)[0], (mousex,graphpoints[int(pos)]+text1.get_height()+5))
                gfxdraw.line(screen,mousex,coords[1]+wh[1]-blnkspacey,mousex,coords[1],(255,255,255))


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

    def baredraw(self,screen,coords,wh,graphrange,mouseover=False):
        """Draws only the graph of the stock - uses the graphrange,startpos, and endpos parameter, not self.graphrange,(coords[0]+wh[0],coords[1]), and (coords[0],coords[1]+wh[1])"""
        # startingpos is the top left corner of the graph, endingpos is the bottom right corner of the graph
        
        percentchange = round(((self.graphrangelists[graphrange][-1]/self.graphrangelists[graphrange][0])-1)*100,2)

        self.graph.setPoints(self.graphrangelists[graphrange])
        color = (30,30,30) if percentchange == 0 else (0,30,0) if percentchange > 0 else (30,0,0)
        graphheight = wh[1]
        graphwidth = wh[0]

        graphingpoints,spacing,minmax_same = self.graph.draw_graph(screen,coords,(graphwidth,graphheight),color,True)

        if mouseover:
            self.mouseover(screen,graphingpoints,spacing,0,coords,wh)#displays the price of the stock when the mouse is over the graph

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0],coords[1],graphwidth,graphheight), 5)
        # if self.bankrupcy(True,screen=screen):#if stock is not bankrupt, first argument is drawn
        #     percentchange = round(((self.graphrangelists[graphrange][-1]/self.graphrangelists[graphrange][0])-1)*100,2)
        #     color = (0,55,0) if percentchange >= 0 else (55,0,0)
        #     gfxdraw.filled_polygon(screen, [(endpos[0], startpos[1]), endpos, (startpos[0], endpos[1]), startpos],color)  # draws the perimeter around graphed values
        #     gfxdraw.filled_polygon(screen,[(endpos[0],startpos[1]),(endpos[0],endpos[1]),(startpos[0],endpos[1]),(startpos[0],startpos[1])],(15,15,15))#draws the background of the graph

        # graphheight = ((endpos[1]-startpos[1])//2)
        # graphwidth = (startpos[0]-endpos[0])
        # graphingpoints = self.graphrangelists[graphrange]
        # minpoint = (np.amin(self.graphrangelists[graphrange]))
        # maxpoint = (np.amax(self.graphrangelists[graphrange]))        

        # if minpoint != maxpoint:#prevents divide by zero error
        #     yScale = graphheight/(maxpoint-minpoint)#the amount of pixels per point with the y axis

        #     yOffset = (startpos[1]+graphheight)-10# slides the graph up on the screen to fit

        #     graphingpoints = (((graphheight)-((graphingpoints - minpoint)) * yScale)) + yOffset# Doing the math to make the points fit on the graph 

        # spacing = graphwidth/len(self.graphrangelists[graphrange])#the spacing between each point

        # graphpointlen = len(graphingpoints)# doing this before the iteration to save time
        # for i,value in enumerate(graphingpoints):
        #     if i >= graphpointlen-1:
        #         pass#if last one in list or i is too great then don't draw line
        #     else:
        #         nextvalue = graphingpoints[i+1]
        #         xpos = endpos[0]
        #         gfxdraw.line(screen,xpos+int(i*spacing),int(value),xpos+int((i+1)*spacing),int(nextvalue),(255,255,255))
        

    def draw(self,screen:pygame.Surface,player:object,coords,wh,Mousebuttons,stocklist=None,rangecontrols=True,graphrange=None):
        """Draws the graph of the stock along with the range controls, price lines, and the name"""
        # if coords != (coords[0]+wh[0],coords[1]) or wh != (coords[0],coords[1]+wh[1]):#if the starting or ending positions have changed
        #     #setting the starting and ending positions - where the graphs are located is constantly changing
        #     # startingpos is the top right corner of the graph, endingpos is the bottom left corner of the graph
        #     self.coords = coords
        #     self.wh = wh
        
        if type(self) == self.Playerclass:#if it is a Player object
            # self.graph(stocklist)#graph the player networth
            self.message(screen)#display the messages
        
        blnkspacex = (coords[0]+wh[0]-coords[0])//10#the amount of blank space to be left on the right side of the graph for x
        blnkspacey = (coords[1]+wh[1]-coords[1])//10#the amount of blank space to be left on the right side of the graph for y
        
        percentchange = round(((self.graphrangelists[self.graphrange][-1]/self.graphrangelists[self.graphrange][0])-1)*100,2)

        if self.bankrupcy(True,screen=screen):#if stock is not bankrupt, first argument is drawn
            percentchange = round(((self.graphrangelists[self.graphrange][-1]/self.graphrangelists[self.graphrange][0])-1)*100,2)
            color = (0,55,0) if percentchange >= 0 else (55,0,0)

            gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],color)  # draws the perimeter around graphed values
            gfxdraw.filled_polygon(screen,[(coords[0],coords[1]),(coords[0],coords[1]+wh[1]-blnkspacey),(coords[0]+wh[0]-blnkspacex,coords[1]+wh[1]-blnkspacey),(coords[0]+wh[0]-blnkspacex,coords[1])],(15,15,15))#draws the background of the graph
        
        if rangecontrols:# if the range controls are drawn
            self.rangecontrols(screen,Mousebuttons,blnkspacey,coords,wh)#draws the range controls

        
        self.graph.setPoints(self.graphrangelists[self.graphrange])
        color = (30,30,30) if percentchange == 0 else (0,30,0) if percentchange > 0 else (30,0,0)
        graphheight = (coords[1]+wh[1]-coords[1])-blnkspacey
        graphwidth = (coords[0]+wh[0]-coords[0])-blnkspacex

        graphingpoints,spacing,minmax_same = self.graph.draw_graph(screen,(coords[0],coords[1]),(graphwidth,graphheight),color,True)
        
        # black outline around the whole graph and the smaller graph
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0], coords[1], (coords[0]+wh[0] - coords[0])-blnkspacex,(coords[1]+wh[1] - coords[1])-blnkspacey), 5)# the one around the graph itself
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0], coords[1], (coords[0]+wh[0] - coords[0]),(coords[1]+wh[1] - coords[1])), 5)# 
        
        if not minmax_same:
            """text that displays the price of the stock and the lines that go across the graph"""
            sortedlist = self.graphrangelists[self.graphrange].copy();sortedlist.sort()# first makes a copy of the list, then sorts the list
            for i in range(4):
                lenpos = int((len(self.graphrangelists[self.graphrange])-1)*(i/3))#Position based purely on the length of the current graph size
                point = sortedlist[lenpos]#using the sorted list so an even amount of price values are displayed
                
                #gets the position of the point in the graphingpoints (the y values) - the sorted list moves the points around so the index of the point is different
                yvalpos = np.where(self.graphrangelists[self.graphrange] == point)[0][0]

                text = s_render(str(limit_digits(point,13)), 30, (255,255,255))
                gfxdraw.line(screen,coords[0]+5,int(graphingpoints[yvalpos]),coords[0]+wh[0]-blnkspacex-5,int(graphingpoints[yvalpos]),(150,150,150))
                # text_rect = text.get_rect(left=((coords[0]+wh[0]-text.get_width()),(graphingpoints[yvalpos]-text.get_height()//2-5)))
                screen.blit(text,(coords[0]+wh[0]-blnkspacex-text.get_width()-10,(graphingpoints[yvalpos]-text.get_height())))


        #draws the text that displays the price of the stock
        if type(self) == Stock:#text displaying the price, and the net worth
            pricetext = s_render(f"${limit_digits(self.price,15)}", 45 if 45 > int((coords[1]+wh[1]-coords[1])/12.5) else int((coords[1]+wh[1]-coords[1])/12.5), (200,200,200))
            textx = coords[0]+10; texty = coords[1]+wh[1]-pricetext.get_height()-15
            screen.blit(pricetext,(textx,texty))# draws the price
                    
        else:
            # goes off the current price of the stock, not the original value stored in the stock object
            screen.blit(s_render(f' Net Worth ${player.get_Networth():,.2f}',40,(255,255,255)),(coords[0]+10,coords[1]+wh[1]-40)) 
            

        screen.blit(s_render(f"{self.name if type(self) == Stock else 'Portfolio'}",50,self.color),(coords[0]+10,coords[1]+10))#draws the text that displays the name of the stock or the player

        #Below is the price change text
        color = (0,175,0) if percentchange >= 0 else (175,0,0)
        
        # if type(self) == Stock:
        change_text = '+' + str(percentchange) + '%' if percentchange >= 0 else '' + str(percentchange) + '%'
        # change_text_rendered = fontlist[40].render(change_text, color)[0]
        change_text_rendered = s_render(change_text, 40, color)
        screen.blit(change_text_rendered, (coords[0]+10, coords[1]+50))
        
        self.mouseover(screen,graphingpoints,spacing,blnkspacey,coords,wh)#displays the price of the stock when the mouse is over the graph
                
        
