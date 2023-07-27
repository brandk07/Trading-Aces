import pygame
from random import randint
import statistics
from pygame import gfxdraw
from Defs import *

class Stock():
    def __init__(self,name,startingpos,endingpos,startingvalue,volatility) -> None:
        """Xpos is the starting x position of the graph, startingvalue is the starting value of the stock"""
        self.startingpos = startingpos
        self.pricepoints = [[startingpos[0]-5,startingvalue]]
        self.endingpos = endingpos
        self.volatility = volatility#determines how much the price can change
        self.temporary_movement = randint(-1*volatility,volatility)#determines overall trend in the movement of the price
        self.movement_length = randint(60,360)#determines the length of the movement (60 is 1 second)
        self.name = name

    def price_movement(self,lastprice):
        self.movement_length -= 1
        if self.movement_length <= 0:
            # self.temporary_movement = randint(-4,5)
            self.temporary_movement = randint(-1*(self.volatility-1),self.volatility)
            self.movement_length = randint(60,360)
        
        if self.temporary_movement > 0:#if price greater then set it as the high for the movement
            return lastprice + randint(-2,self.temporary_movement)
        elif self.temporary_movement < 0:# if price less then set it as the low for the movement
            return lastprice + randint(self.temporary_movement,2)
        else:
            return lastprice + randint(-3,3)
    
    def resize_graph(self):
        
        medianpoint = statistics.median([point[1] for point in self.pricepoints])
        # print(f'max is {max(self.pricepoints, key=lambda x: x[1])[1]}, min is {min(self.pricepoints, key=lambda x: x[1])[1]}')
        # print(f'max dif is {abs(max(self.pricepoints, key=lambda x: x[1])[1]-medianpoint)}, min dif is {abs(min(self.pricepoints, key=lambda x: x[1])[1]-medianpoint)}')
        # print(f'min point is {min(self.pricepoints, key=lambda x: x[1])}, max point is {max(self.pricepoints, key=lambda x: x[1])}')
        
        if abs(min(self.pricepoints, key=lambda x: x[1])[1]-medianpoint) > abs(max(self.pricepoints, key=lambda x: x[1])[1]-medianpoint):
            return abs(min(self.pricepoints, key=lambda x: x[1])[1]-medianpoint)+25
        return abs(max(self.pricepoints, key=lambda x: x[1])[1]-medianpoint)+25
    
    def update(self,screen,update:bool):
        gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(60,60,60))
        
        if update:
            self.pricepoints.append([self.startingpos[0]-5,self.price_movement(self.pricepoints[-1][1])])

        graphsize = self.resize_graph()
        if graphsize <= 0: graphsize = 1
        medianpoint = statistics.median([point[1] for point in self.pricepoints])
        # print('graphsize is',graphsize)
        # print('median point is',medianpoint)
        graphheight = (self.endingpos[1]-self.startingpos[1])/2
        yvaluefinder = lambda x: int(graphheight+(((x-medianpoint)/graphsize)*graphheight)+self.startingpos[1])
        new_y_values = list(map(yvaluefinder,[point[1] for point in self.pricepoints]))
            
        for i,point in enumerate(self.pricepoints):
            #logic for determining the y value of the point
            # yvalue = (self.endingpos[1]-self.startingpos[1])-((point[1]/(medianpoint+graphsize))*(self.endingpos[1]-self.startingpos[1]))+self.startingpos[1]
            
            # percent = ((point[1]-medianpoint)/graphsize)
            # graphheight = (self.endingpos[1]-self.startingpos[1])/2
            # yvalue = graphheight+((percent/graphsize)*graphheight)+self.startingpos[1]

            # gfxdraw.filled_circle(screen,point[0],int(yvalue),1,(0,255,0))
            if i >= len(self.pricepoints)-1:
                pass
            else:
                gfxdraw.line(screen,point[0],new_y_values[i],self.pricepoints[i+1][0],new_y_values[i+1],(0,255,0))
            if update:
                point[0] -= 1
                if point[0] <= self.endingpos[0]: 
                    self.pricepoints.remove(point)

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.endingpos[0],self.startingpos[1],(self.startingpos[0]-self.endingpos[0]),self.endingpos[1]),15)
        screen.blit(font40.render(f'{self.name} ${self.pricepoints[-1][1]}',1,(255,255,255)),(self.endingpos[0]+15,self.startingpos[1]+15))
        screen.blit(font18.render(f'temp move {self.temporary_movement}, move length {self.movement_length}',1,(255,255,255)),(self.endingpos[0]+15,self.startingpos[1]+50))
        

    