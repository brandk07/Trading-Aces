import pygame
from random import randint
from pygame import gfxdraw
from Defs import *
import numpy as np
import json
from Classes.imports.Graph import Graph
from datetime import datetime,timedelta
from Classes.StockVisualizer import StockVisualizer,POINTSPERGRAPH


class Stock():
    """Class contains the points and ability to modify the points of the stock"""

    def __init__(self,name,volatility,color) -> None:
        self.color,self.name = color,name

        #variables for graphing the stock 
        #make graphingrangeoptions a dict with the name of the option as the key and the value as the amount of points to show
        self.graphrangeoptions = {"1H":3600,"1D":23_400,"1W":117_000,"1M":489_450,"3M":1_468_350,"1Y":5_873_400}
        self.condensefacs = {key:value/POINTSPERGRAPH for key,value in self.graphrangeoptions.items()}#the amount of points that each index of the graph has
        # self.graphrange = '1H' # H, D, W, M, 3M, Y
        self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
        self.graphfillvar = {key:0 for key in self.graphrangeoptions.keys()}# used to see when to add a point to a graph
        
        # self.bonustrendranges = [[(-1*i,i),(100000-(i*8325),500000-(i*41400))] for i in range(12)]
        self.bonustrendranges = [[(-i,i),(randint(1,12000),randint(12001,1_500_000))] for i in range(12)]
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]

        self.datafromfile()# Retrieves the data from the file
        self.price = self.graphs['1H'][-1]# the price of the stock at the last graphed point
        
        self.volatility = volatility
        self.recentrenders = {}# a dict of the renders of the recent prices

        self.graph = Graph()
    

    def __str__(self) -> str:
        return f'{self.name}'
    
    def reset_trends(self):
        """Sets/resets the trends for the stock"""
        self.bonustrends = [[randint(*x[0]),randint(*x[1])] for x in self.bonustrendranges]#resets the trends for each bonus trend

    def getPercent(self,graphrange):
        """Returns the percent change of the stock"""
        return ((self.graphs[graphrange][-1]/self.graphs[graphrange][0])-1)*100

    def reset_graphs(self):
        """resets the graphs to be empty"""
        # for i in ["1H","1D","1W","1M","3M","1Y","trends"]:
        newprice = randint(*self.starting_value_range)
        for grange in self.graphs.keys():# for each graph range, ["1H","1D","1W","1M","3M","1Y","trends"], assign the new price to each graph
            self.graphs[grange] = np.array([newprice])

    def datafromfile(self):
        """gets the data from each file and puts it into the graphlist"""
        with open(f'Assets/Stockdata/{self.name}/data.json', 'r')as f:
            data = [json.loads(line) for line in f]

            for i,grange in enumerate(self.graphs.keys()):
                if data[i]:# if the file is not empty
                    self.graphs[grange] = np.array(data[i])# add the contents to the graphs
                else:
                    self.graphs[grange] = np.array([100])# if the file is empty then set the graph to 100
            if len(data[-1]) > 0:
                self.bonustrends = data[-1]
            else:
                self.reset_trends()

    def save_data(self):
        with open(f'Assets/Stockdata/{self.name}/data.json','w') as file:
            file.seek(0)  # go to the start of the file
            file.truncate()  # clear the file
            for item in list(self.graphs.values()):
                for i in range(len(item)):
                    item[i] = float(item[i])
                json_item = json.dumps(item.tolist())  # Convert the list to a JSON string
                file.write(json_item + '\n')  # Write the JSON string to the file with a newline character
            
            file.write(json.dumps(self.bonustrends))
        

    # def bankrupcy(self,drawn,coords=None,wh=None,screen:pygame.Surface=None):
    #     """returns False if stock is not bankrupt,don't need screen if drawn is False"""	
    #     if self.price < 0 and self.pricereset_time == None:#if stock goes bankrupt, and no time has been set
    #         self.pricereset_time = time.time()
    #         return False
    #     elif self.pricereset_time != None and time.time() > self.pricereset_time+5:#if stock goes bankrupt and 5 seconds have passed
    #         self.price = randint(*self.starting_value_range)
    #         self.reset_trends(); self.pricereset_time = None#reset the trends and the pricereset_time
    #         self.reset_graphs()
    #         if drawn:
    #             gfxdraw.filled_polygon(screen,[(coords[0],coords[1]),(coords[0],coords[1]+wh[1]),(coords[0]+wh[0],coords[1]+wh[1]),(coords[0]+wh[0],coords[1])],(200,0,0))#draws the background of the graph red
    #         return False
    #     elif self.pricereset_time != None and time.time() < self.pricereset_time+5:#if stock goes bankrupt and less then 5 seconds have passed
    #         if drawn:
    #             gfxdraw.filled_polygon(screen,[(coords[0],coords[1]),(coords[0],coords[1]+wh[1]),(coords[0]+wh[0],coords[1]+wh[1]),(coords[0]+wh[0],coords[1])],(200,0,0))#draws the background of the graph red
    #             screen.blit(fontlist[40].render(f'BANKRUPT',(255,255,255))[0],(coords[0]+15,coords[1]+15))
    #         return False
    #     return True
    
    # def stock_split(self,player):
    #     if self.price >= 2500:
    #         player.messagedict[f'{self.name} has split'] = (time.time(),(0,0,200))
    #         for grange in self.graphs.keys():# for each graph range, ["1H","1D","1W","1M","3M","1Y","trends"]
    #             self.graphs[grange] = np.array([point*0.5 for point in self.graphs[grange]])
    #         self.price = self.price*0.5
    #         stock_quantity = len([stock for stock in player.stocks if stock[0] == self])
    #         if stock_quantity > 0:
    #             player.messagedict[f'You now have {stock_quantity*2} shares of {self.name}'] = (time.time(),(0,0,200))
    #             for stock in player.stocks.copy():
    #                 print(stock)
    #                 if stock[0] == self:
    #                     player.stocks.remove(stock)
    #                     player.stocks.append([stock[0],stock[1]*0.5,stock[2]])
    #                     player.stocks.append([stock[0],stock[1]*0.5,stock[2]])
    #             print('stocks are',player.stocks)

    def addpoint(self, lastprice, multiplier=1,maxstep=25):
        """returns the new price of the stock
        maxstep is the maximum multiplier added to 1 price movement, a lower value will make it more accurate but slower"""
        while multiplier > 0:
            step = multiplier % maxstep if multiplier < maxstep else maxstep# how much to multiply the movement by

            for i, bonustrend in enumerate(self.bonustrends):# for each bonus trend
                if bonustrend[1] <= 0:  # if the time is out
                    self.bonustrends[i] = [randint(*self.bonustrendranges[i][0]), randint(*self.bonustrendranges[i][1])]
                else:
                    bonustrend[1] -= step

            total_trend = sum(trend[0] for trend in self.bonustrends)# the total trend of all the bonus trends
            total_trend = total_trend if total_trend >= 0 else -1 * (total_trend // 2)# if the total trend is negative, then divide it by 2
            highvolitity = self.volatility + total_trend# the highest volitility that the stock can have
            lowvolitity = -self.volatility + total_trend# the lowest volitility that the stock can have
            
            factor = (randint(lowvolitity, highvolitity) / 500_000) * step# the factor that the price will be multiplied by
            lastprice = lastprice * ((1 + factor) if randint(0, 1) else (1 - factor))  # returns the new price of the stock
            multiplier -= step

        return lastprice
    
    def fill_graphs(self):
        def get_lowestgraph(pointsmade):
            for name,points in self.graphs.items():
                """Returns the name of the lowest graph that should get points added to it"""
                # the line below figures out if the amount of points made is greater than the amount of points that the graph can have
                if (diff:=self.graphrangeoptions["1Y"]-self.graphrangeoptions[name]) <= pointsmade:
                    # figuring out the amount of points that each index of the graph has
                    condensefactor = self.condensefacs[name]
                    # if the amount of points made is greater than or equal to the amount of points that the graph can have
                    if pointsmade-diff >= condensefactor*len(points):
                        return name

        self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}# reset the graphs

        lastgraphed = ""
        pointsmade = 0
        while len(self.graphs['1H']) < POINTSPERGRAPH:
            newgraphed = get_lowestgraph(pointsmade)# gets the name of the lowest graph that should get points added to it
            if newgraphed == None:# if there is no graph that needs points added to it for the amount of points made
                pointsmade += 1# advance pointsmade until there is a graph that needs points added to it
                continue
            if self.graphs[newgraphed].size == 0:# if the graph is empty
                if lastgraphed == "":# if there is no last graphed (Only used for the year graph)
                    self.graphs[newgraphed] = np.array([self.price],dtype=object)
                else:# this is when the first point is added to a graph after the year graph
                    self.graphs[newgraphed] = np.append(self.graphs[newgraphed],self.graphs[lastgraphed][-1])

            lastgraphed = newgraphed
            multiplier = int(self.graphrangeoptions[lastgraphed]/POINTSPERGRAPH)
            
            newpoint = self.addpoint(self.graphs[lastgraphed][-1],multiplier)

            for name,points in self.graphs.items():# for each graph
                if (diff:=self.graphrangeoptions["1Y"]-self.graphrangeoptions[name]) <= pointsmade:# figures out if the amount of pointsmade is greater than the amount of points that the graph can have
                    condensefactor = self.condensefacs[name]
                    if pointsmade-diff >= condensefactor*len(points):
                        self.graphs[name] = np.append(self.graphs[name],newpoint)

            pointsmade += multiplier
        self.price = self.graphs['1H'][-1]

    def update_range_graphs(self,stockvalues=0):
        
        for key in self.graphrangeoptions:
            condensefactor = self.condensefacs[key]
            self.graphfillvar[key] += 1
            if self.graphfillvar[key] == int(condensefactor):#if enough points have passed to add a point to the graph (condensefactor is how many points must go by to add 1 point to the graph)
                #add the last point to the list
                self.graphfillvar[key] = 0
                if type(self) == Stock:
                    self.graphs[key] = np.append(self.graphs[key],self.price)
                else:
                    self.graphs[key] = np.append(self.graphs[key],stockvalues)
            
            if len(self.graphs[key]) > POINTSPERGRAPH:
                # print('deleting',key,len(self.graphs[key]))
                self.graphs[key] = np.delete(self.graphs[key],0)

    def update_price(self,gamespeed,PlayerClass):
        # if self.bankrupcy(False):#if stock is not bankrupt
        #     pass
        
        if type(self) == Stock:#making sure that it is a Stock object and that update is true
            self.price = self.addpoint(self.price,multiplier=gamespeed,maxstep=5)#updates the price of the stock
            # self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable
            for _ in range(gamespeed):
                self.update_range_graphs()
            self.price = self.graphs["1H"][-1]
        elif type(self) == PlayerClass:# if Player object

            # stockvalues = sum([stock[0].price*stock[2] for stock in self.stocks])
            self.price = self.getNetworth()
            for _ in range(gamespeed):
                self.update_range_graphs(self.getNetworth())#updates the range graphs
        

    # def rangecontrols(self,screen:pygame.Surface,Mousebuttons,blnkspacey,coords,wh):
    #     """draws the range controls and checks for clicks"""
    #     x,y = coords[0]+wh[0]-int((coords[1]+wh[1]-coords[1])/20),coords[1]+wh[1]-blnkspacey*.75
    #     for i in range(len(self.graphrangeoptions),0,-1):
    #         name = list(self.graphrangeoptions)[i-1]
    #         text = s_render(name,int((coords[1]+wh[1]-coords[1])/15),(255,255,255) if self.graphrange == name else (120,120,120))
    #         screen.blit(text,(x-(text.get_width()/2),y))
    #         if pygame.Rect(x - text.get_width() / 2 - 2, y - 2, text.get_width() + 10, text.get_height() + 10).collidepoint(pygame.mouse.get_pos()):
    #             if Mousebuttons == 1:
    #                 self.graphrange = name
    #         x -= text.get_width()+int((coords[1]+wh[1]-coords[1])/40)



    # def mouseover(self,screen:pygame.Surface,graphpoints,spacing,blnkspacey,coords,wh,gametime=False):
    #     """displays the price of the stock when the mouse is over the graph"""
    #     mousex,mousey = pygame.mouse.get_pos()
    #     if pygame.Rect(coords[0],coords[1],(coords[0]+wh[0]-coords[0]),(coords[1]+wh[1]-coords[1])).collidepoint(mousex,mousey):
    #         pos = (mousex-coords[0])//spacing
    #         if pos < len(self.graphs[self.graphrange]):
    #             text1 = s_render(f'${self.graphs[self.graphrange][int(pos)]:,.2f}',30,(255,255,255))# the value of the stock
    #             screen.blit(text1,(mousex,graphpoints[int(pos)]-text1.get_height()-5))# the value of the stock
    #             # text2 = s_render()
    #             if gametime:
    #                 mousepoint = (len(self.graphs[self.graphrange])-pos)

    #                 graphed_seconds = mousepoint*(self.graphrangeoptions[self.graphrange]/POINTSPERGRAPH)# the amount of seconds that the stock has been graphed
    #                 grapheddays = graphed_seconds//self.graphrangeoptions["1D"]# the amount of days that the stock has been graphed
    #                 seconds = graphed_seconds%self.graphrangeoptions["1D"]# the amount of seconds that the stock has been graphed
    #                 time_offset = gametime.time#time offset
    #                 if gametime.isOpen(time_offset)[0] == False:
    #                     time_offset = time_offset.replace(hour=15,minute=59,second=0)# set the time to 3:59 PM
    #                 dayscount = 0

    #                 while dayscount < grapheddays:
    #                     time_offset -= timedelta(days=1)# add a day to the time offset
    #                     if gametime.isOpen(time_offset)[0]:# if that is a day that was open for trading
    #                         dayscount += 1# add 1 to the days count

    #                 secondsleft = (time_offset - time_offset.replace(hour=9,minute=30,second=0)).seconds# the amount of seconds left in the day
    #                 if seconds > secondsleft:# if the amount of seconds needed to minus is greater than the seconds left in the day
    #                     seconds -= secondsleft
    #                     time_offset -= timedelta(days=1)# add a day to the time offset
    #                     while gametime.isOpen(time_offset)[0] == False:
    #                         time_offset -= timedelta(days=1)
                        
    #                     time_offset = time_offset.replace(hour=15,minute=59,second=0)# set the time to 3:59 PM
                        
    #                 time_offset -= timedelta(seconds=seconds)# add a day to the time offset

    #                 text2 = s_render(f'{time_offset.strftime("%m/%d/%Y %I:%M %p")}',30,(255,255,255))
    #                 screen.blit(text2,(mousex,graphpoints[int(pos)]))# the time of the stock

    #             percentchange = round(((self.graphs[self.graphrange][int(pos)]/self.graphs[self.graphrange][0])-1)*100,2)
    #             color = (0,205,0) if percentchange >= 0 else (205,0,0)
    #             if percentchange == 0: color = (205,205,205)
    #             screen.blit(s_render(f'{percentchange:,.2f}%',30,color),(mousex,graphpoints[int(pos)]+text1.get_height()+5))# the percent change of the stock

    #             gfxdraw.line(screen,mousex,coords[1]+wh[1]-blnkspacey,mousex,coords[1],(255,255,255))

    # def baredraw(self,screen,coords,wh,graphrange,mouseover=False):
    #     """Draws only the graph of the stock - uses the graphrange,startpos, and endpos parameter, not self.graphrange,(coords[0]+wh[0],coords[1]), and (coords[0],coords[1]+wh[1])"""
    #     # startingpos is the top left corner of the graph, endingpos is the bottom right corner of the graph
        
    #     percentchange = round(((self.graphs[graphrange][-1]/self.graphs[graphrange][0])-1)*100,2)

    #     self.graph.setPoints(self.graphs[graphrange])
    #     color = (30,30,30) if percentchange == 0 else (0,30,0) if percentchange > 0 else (30,0,0)
    #     graphheight = wh[1]
    #     graphwidth = wh[0]

    #     graphingpoints,spacing,minmax_same = self.graph.draw_graph(screen,coords,(graphwidth,graphheight),color,True)

    #     if mouseover:
    #         self.mouseover(screen,graphingpoints,spacing,0,coords,wh)#displays the price of the stock when the mouse is over the graph

    #     pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0],coords[1],graphwidth,graphheight), 5)
        
    
    # def draw(self,screen:pygame.Surface,player:object,coords,wh,Mousebuttons,gametime,rangecontroldisp=True,graphrange=None) -> bool:
    #     """Draws the graph of the stock along with the range controls, price lines, and the name"""
        
    #     if type(self) == self.Playerclass:#if it is a Player object
    #         # self.graph(stocklist)#graph the player networth
    #         self.message(screen)#display the messages
        
    #     self.price = self.graphs["1H"][-1]
    #     self.graphrange = graphrange if graphrange != None else self.graphrange

        
    #     blnkspacex = (coords[0]+wh[0]-coords[0])//10#the amount of blank space to be left on the right side of the graph for x
    #     blnkspacey = (coords[1]+wh[1]-coords[1])//10#the amount of blank space to be left on the right side of the graph for y
        
    #     percentchange = round(((self.graphs[self.graphrange][-1]/self.graphs[self.graphrange][0])-1)*100,2)

    #     if self.bankrupcy(True,coords, wh, screen=screen):#if stock is not bankrupt, first argument is drawn
    #         percentchange = round(((self.graphs[self.graphrange][-1]/self.graphs[self.graphrange][0])-1)*100,2)
    #         color = (0,55,0) if percentchange >= 0 else (55,0,0)

    #         gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],color)  # draws the perimeter around graphed values
    #         gfxdraw.filled_polygon(screen,[(coords[0],coords[1]),(coords[0],coords[1]+wh[1]-blnkspacey),(coords[0]+wh[0]-blnkspacex,coords[1]+wh[1]-blnkspacey),(coords[0]+wh[0]-blnkspacex,coords[1])],(15,15,15))#draws the background of the graph
        
    #     if rangecontroldisp:# if the range controls are drawn
    #         self.rangecontrols(screen,Mousebuttons,blnkspacey,coords,wh)#draws the range controls

    #     # using the graph class to graph the points
    #     self.graph.setPoints(self.graphs[self.graphrange])# set the list of points
    #     # color = (30,30,30) if percentchange == 0 else (0,30,0) if percentchange > 0 else (30,0,0)
    #     color = percent3choices((30,0,0),(0,30,0),(30,30,30),self.getPercent(self.graphrange))
    #     graphheight = (coords[1]+wh[1]-coords[1])-blnkspacey
    #     graphwidth = (coords[0]+wh[0]-coords[0])-blnkspacex

    #     graphingpoints,spacing,minmax_same = self.graph.draw_graph(screen,(coords[0],coords[1]),(graphwidth,graphheight),color,True)# graph the points and get needed values
        
    #     # black outline around the whole graph and the smaller graph
    #     pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0], coords[1], (coords[0]+wh[0] - coords[0])-blnkspacex,(coords[1]+wh[1] - coords[1])-blnkspacey), 5)# the one around the graph itself
    #     pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0], coords[1], (coords[0]+wh[0] - coords[0]),(coords[1]+wh[1] - coords[1])), 5)# 
        
    #     if not minmax_same:# if the min and max are not the same
    #         """text that displays the price of the stock and the lines that go across the graph"""
    #         sortedlist = self.graphs[self.graphrange].copy();sortedlist.sort()# first makes a copy of the list, then sorts the list
    #         for i in range(4):
    #             lenpos = int((len(self.graphs[self.graphrange])-1)*(i/3))#Position based purely on the length of the current graph size
    #             point = sortedlist[lenpos]#using the sorted list so an even amount of price values are displayed
                
    #             #gets the position of the point in the graphingpoints (the y values) - the sorted list moves the points around so the index of the point is different
    #             yvalpos = np.where(self.graphs[self.graphrange] == point)[0][0]

    #             text = s_render(str(limit_digits(point,13)), 30, (255,255,255))
    #             gfxdraw.line(screen,coords[0]+5,int(graphingpoints[yvalpos]),coords[0]+wh[0]-blnkspacex-5,int(graphingpoints[yvalpos]),(150,150,150))
    #             # text_rect = text.get_rect(left=((coords[0]+wh[0]-text.get_width()),(graphingpoints[yvalpos]-text.get_height()//2-5)))
    #             screen.blit(text,(coords[0]+wh[0]-blnkspacex-text.get_width()-10,(graphingpoints[yvalpos]-text.get_height())))


    #     #draws the text that displays the price of the stock
    #     if type(self) == Stock:#text displaying the price, and the net worth
    #         pricetext = s_render(f"${limit_digits(self.price,15)}", 45 if 45 > int((coords[1]+wh[1]-coords[1])/12.5) else int((coords[1]+wh[1]-coords[1])/12.5), (200,200,200))
    #         textx = coords[0]+10; texty = coords[1]+wh[1]-pricetext.get_height()-15
    #         screen.blit(pricetext,(textx,texty))# draws the price
                    
    #     else:
    #         # goes off the current price of the stock, not the original value stored in the stock object
    #         screen.blit(s_render(f' Net Worth ${player.getNetworth():,.2f}',40,(255,255,255)),(coords[0]+10,coords[1]+wh[1]-40)) 
            
        
        
    #     #Below is the price change text
    #     color = (0,175,0) if percentchange >= 0 else (175,0,0)
        
    #     # if type(self) == Stock:
    #     change_text = '+' + str(percentchange) + '%' if percentchange >= 0 else '' + str(percentchange) + '%'
    #     change_text_rendered = s_render(change_text, 40, color)
    #     screen.blit(change_text_rendered, (coords[0]+10, coords[1]+50))
        
    #     self.mouseover(screen,graphingpoints,spacing,blnkspacey,coords,wh,gametime=gametime)#displays the price of the stock when the mouse is over the graph
        
    #     nametext = s_render(f"{self.name if type(self) == Stock else 'Portfolio'}",50,self.color)

    #     if pygame.Rect(coords[0]+10,coords[1]+10,nametext.get_width(),nametext.get_height()).collidepoint(pygame.mouse.get_pos()):#if the mouse is over the name of the stock
    #         nametext = s_render(f"{self.name if type(self) == Stock else 'Portfolio'}",50,(230,230,230))    
    #         screen.blit(nametext,(coords[0]+10,coords[1]+10))#draws the text that displays the name of the stock or the player
    #         return True   
    #     screen.blit(nametext,(coords[0]+10,coords[1]+10))#draws the text that displays the name of the stock or the player
    #     return False
    
