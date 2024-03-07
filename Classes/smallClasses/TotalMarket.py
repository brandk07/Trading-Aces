from Defs import *
import numpy as np
import pygame
from random import randint
from Classes.Stock import Stock

POINTSPERGRAPH = 200

class TotalMarket(Stock):
    def __init__(self,gametime) -> None:
        # name,volatility,color,gametime
        super().__init__('Total Market',0,(213, 219, 44),gametime)

        # self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
    def datafromfile(self):
        # this child class does not need to read data from a file
        self.graphs = {key:np.array([100],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
    def fill_graphs(self,stocklist):
        """Fills the graphs with the stock's prices"""
        # equivalent to the datafromfile method, but it wasn't necessary to store stuff in a file since it can be loaded fast 
        for key in self.graphrangeoptions:
            self.graphs[key] = np.array([],dtype=object)
            for point in range(POINTSPERGRAPH):
                value = sum([stock.graphs[key][point] for stock in stocklist])/9
                self.graphs[key] = np.append(self.graphs[key],value)
        self.price = self.graphs["1H"][-1]
            

    def update_range_graphs(self,value):
        
        for key in self.graphrangeoptions:
            condensefactor = self.condensefacs[key]
            self.graphfillvar[key] += 1
            if self.graphfillvar[key] == int(condensefactor):#if enough points have passed to add a point to the graph (condensefactor is how many points must go by to add 1 point to the graph)
                #add the last point to the list
                self.graphfillvar[key] = 0
                self.graphs[key] = np.append(self.graphs[key],value)

            
            if len(self.graphs[key]) > POINTSPERGRAPH:
                # print('deleting',key,len(self.graphs[key]))
                self.graphs[key] = np.delete(self.graphs[key],0)
        self.price = value

    def updategraphs(self,stocklist:list,gameplay_speed:int):
        """Updates the graphs for the stocks"""
        for i in range(gameplay_speed):
            value = 0
            for stock in stocklist:
                value += stock.graphs["1H"][-1]# adds the last value of the stock to the value
            
            value = value/len(stocklist)# gets the average value of the stocks
            # self.graphs["1H"] = np.append(self.graphs["1H"],value)# adds the value to the graph

            self.update_range_graphs(value)
    
    # def draw(self,screen:pygame.Surface,coords,wh,Mousebuttons,gametime,rangecontrols=True,graphrange=None):
    #     blnkspacex = (coords[0]+wh[0]-coords[0])//10#the amount of blank space to be left on the right side of the graph for x
    #     blnkspacey = (coords[1]+wh[1]-coords[1])//10#the amount of blank space to be left on the right side of the graph for y

    #     percentchange = round(((self.graphs[self.graphrange][-1]/self.graphs[self.graphrange][0])-1)*100,2)
    #     color = (0,55,0) if percentchange >= 0 else (55,0,0)

    #     gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],color)  # draws the perimeter around graphed values
    #     gfxdraw.filled_polygon(screen,[(coords[0],coords[1]),(coords[0],coords[1]+wh[1]-blnkspacey),(coords[0]+wh[0]-blnkspacex,coords[1]+wh[1]-blnkspacey),(coords[0]+wh[0]-blnkspacex,coords[1])],(15,15,15))#draws the background of the graph
        
    #     if rangecontrols:# if the range controls are drawn
    #         self.rangecontrols(screen,Mousebuttons,blnkspacey,coords,wh)#draws the range controls

    #     # using the graph class to graph the points
    #     self.graph.setPoints(self.graphs[self.graphrange])# set the list of points
    #     color = (30,30,30) if percentchange == 0 else (0,30,0) if percentchange > 0 else (30,0,0)
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



    #     pricetext = s_render(f"${limit_digits(self.price,15)}", 45 if 45 > int((coords[1]+wh[1]-coords[1])/12.5) else int((coords[1]+wh[1]-coords[1])/12.5), (200,200,200))
    #     textx = coords[0]+10; texty = coords[1]+wh[1]-pricetext.get_height()-15
    #     screen.blit(pricetext,(textx,texty))# draws the price
 
    #     screen.blit(s_render(f"{self.name}",50,self.color),(coords[0]+10,coords[1]+10))#draws the text that displays the name of the stock or the player

    #     #Below is the price change text
    #     color = (0,175,0) if percentchange >= 0 else (175,0,0)
        
    #     # if type(self) == Stock:
    #     change_text = '+' + str(percentchange) + '%' if percentchange >= 0 else '' + str(percentchange) + '%'
    #     # change_text_rendered = fontlist[40].render(change_text, color)[0]
    #     change_text_rendered = s_render(change_text, 40, color)
    #     screen.blit(change_text_rendered, (coords[0]+10, coords[1]+50))
        
    #     self.mouseover(screen,graphingpoints,spacing,blnkspacey,coords,wh,gametime)#displays the price of the stock when the mouse is over the graph