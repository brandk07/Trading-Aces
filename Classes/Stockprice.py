import pygame
from random import randint
import statistics
from pygame import gfxdraw
import time
from Defs import *

    
class Stock():
    def __init__(self,name,startingpos,endingpos,startingvalue_range,volatility) -> None:
        """Xpos is the starting x position of the graph, startingvalue is the starting value of the stock"""
        self.startingpos = startingpos
        self.starting_value_range = startingvalue_range
        print(startingvalue_range,name)
        self.pricepoints = [[startingpos[0]-5,randint(*startingvalue_range)]]
        self.endingpos = endingpos
        self.volatility = volatility#determines how much the price can change
        self.temporary_movement = randint(-2*volatility,volatility)#determines overall trend in the movement of the price
        self.movement_length = randint(60,360)#determines the length of the movement (60 is 1 second)
        self.name = name
        self.stockimages = [pygame.transform.scale(pygame.image.load(f'assets/stock{txt}.png'),(30,30)) for txt in ['up','down']]
        self.recent_movementvar = (None,None,(180,180,180))
        self.control_images = {txt:pygame.transform.scale(pygame.image.load(f'assets/player controls/{txt}.png'),(60,38)) for txt in ['buy','buyhover','sell','sellhover']}
        self.pricereset_time = None
    def buy_sell(self,player,screen:pygame.Surface,Mousebuttons):
        """buy or sell stock"""
        mousex,mousey = pygame.mouse.get_pos()
        if self.startingpos[0]-140 < mousex < self.startingpos[0]-80 and self.endingpos[1]-51 < mousey < self.endingpos[1]-13:#if mouse is over buy button
            screen.blit(self.control_images['buyhover'],(self.startingpos[0]-140,self.endingpos[1]-51))#draws the buy button with hover image
            if Mousebuttons == 1 and self.pricepoints[-1][1] <= player.cash:#if mouse is clicked and player has enough money
                player.buy(self.name,self.pricepoints[-1][1])
            elif Mousebuttons == 1 and self.pricepoints[-1][1] > player.cash:
                print('you dont have enough money')
        else:
            screen.blit(self.control_images['buy'],(self.startingpos[0]-140,self.endingpos[1]-51))#draws the buy button with normal image
            
        if self.startingpos[0]-75 < mousex < self.startingpos[0]-15 and self.endingpos[1]-51 < mousey < self.endingpos[1]-13:#if mouse is over sell button
            screen.blit(self.control_images['sellhover'],(self.startingpos[0]-75,self.endingpos[1]-51))#draws the sell button with hover image
            if Mousebuttons == 1 and [stock[0] for stock in player.stocks if stock[0] == self.name]:#if mouse is clicked and player has the stock
                player.sell(self.name,self.pricepoints[-1][1])
            elif Mousebuttons == 1 and not [stock[0] for stock in player.stocks if stock[0] == self.name]:
                print('you dont have this stock')
        else:
            screen.blit(self.control_images['sell'],(self.startingpos[0]-75,self.endingpos[1]-51))#draws the sell button with normal image
    def recent_price_movement(self):
        """returns the recent price movement"""
        if self.recent_movementvar[1] != None:#if there is a recent movement then check if it is still recent
            if self.recent_movementvar[1] < time.time():#if it is no longer recent then set it to none
                self.recent_movementvar = (None,None,(180,180,180))
                
            else:#if it is still recent then return the movement
                return self.recent_movementvar[0]
            
        if len(self.pricepoints) < 10:#if there are less then 10 points then return none
            return None
        if self.pricepoints[-1][1]-self.pricepoints[-10][1] > 20:#price going down, know its counter intuitive but it works
            self.recent_movementvar = (0,time.time()+3,(0,200,0))
            return 0
        elif self.pricepoints[-1][1]-self.pricepoints[-10][1] < -20:
            self.recent_movementvar = (1,time.time()+3,(200,0,0))
            return 1
        return None
    
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
        
        #below we are checking if the max or min is further away from the median point, and then returning the distance from the median point
        if abs(min(self.pricepoints, key=lambda x: x[1])[1]-medianpoint) > abs(max(self.pricepoints, key=lambda x: x[1])[1]-medianpoint):
            return abs(min(self.pricepoints, key=lambda x: x[1])[1]-medianpoint)+30
        return abs(max(self.pricepoints, key=lambda x: x[1])[1]-medianpoint)+30
    
    def update(self,screen,update:bool,Player:object):
        if self.pricepoints[-1][1] < 0 and self.pricereset_time == None:#if stock goes bankrupt, and no time has been set
            self.pricereset_time = time.time()
            self.pricepoints = [[self.startingpos[0]-5,randint(*self.starting_value_range)]]
            print('stock went bankrupt')
        elif self.pricereset_time != None and time.time() > self.pricereset_time+5:#if stock goes bankrupt and 5 seconds have passed
            self.pricepoints[-1][1] = randint(*self.starting_value_range)
            self.temporary_movement = randint(-1*(self.volatility-1),self.volatility)
            self.movement_length = randint(60,360); self.pricereset_time = None
            gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(255,0,0))#draws the background of the graph red

        elif self.pricereset_time != None and time.time() < self.pricereset_time+5:#if stock goes bankrupt and less then 5 seconds have passed
            gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(255,0,0))#draws the background of the graph red
            screen.blit(font40.render(f'BANKRUPT',1,(255,255,255)),(self.endingpos[0]+15,self.startingpos[1]+15))
        else:
            gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(60,60,60))#draws the background of the graph
            if type(self) == Stock and update:#making sure that it is a Stock object and that update is true
                self.pricepoints.append([self.startingpos[0]-5,self.price_movement(self.pricepoints[-1][1])])#if update is true then add a new point to the graph
            graphsize = self.resize_graph()
            if graphsize <= 0: graphsize = 1#graphsize is the distance from the median point to the max or min point

            medianpoint = statistics.median([point[1] for point in self.pricepoints])# the median point of the graph

            graphheight = (self.endingpos[1]-self.startingpos[1])/2# graphheight is the height of the graph

            #yvaluefinder is a function that takes a value and returns the y value of the point - look in assets for pic of equation
            yvaluefinder = lambda x: int(graphheight+(((medianpoint-x)/graphsize)*graphheight)+self.startingpos[1])

            #new_y_values is a list of all the y values of the points in the graph - had to use so I could access all of the y values for lines in the for loop
            new_y_values = list(map(yvaluefinder,[point[1] for point in self.pricepoints]))
            
            
            for i,point in enumerate(self.pricepoints):
                if i >= len(self.pricepoints)-1:pass#if last one in list then don't draw line
                else:
                    gfxdraw.line(screen,point[0],new_y_values[i],self.pricepoints[i+1][0],new_y_values[i+1],self.recent_movementvar[2])#draws the line between the points
                if update:
                    point[0] -= 1
                    if point[0] <= self.endingpos[0]: 
                        self.pricepoints.remove(point)
            
            
            # pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.endingpos[0],self.startingpos[1],(self.startingpos[0]-self.endingpos[0]),self.endingpos[1]),10)#draws the perimeter around graphed values
            gfxdraw.rectangle(screen,pygame.Rect(self.endingpos[0],self.startingpos[1],(self.startingpos[0]-self.endingpos[0]),self.endingpos[1]),(0,0,0),)#draws the perimeter around graphed values
            #price text, had to separte because I need the width of the text to draw the stock image
        
            pricetext = font40.render(f'{self.name} ${self.pricepoints[-1][1]}',1,(255,255,255))
            #draws the price text
            screen.blit(pricetext,(self.endingpos[0]+15,self.startingpos[1]+15))
            # if type(self) == Stock:#text displaying the temporary movement and the movement length (not needed for final version and only for Stock objects)
            #     screen.blit(font18.render(f'temp move {self.temporary_movement}, move length {self.movement_length}',1,(255,255,255)),(self.endingpos[0]+15,self.startingpos[1]+50))
    

            #if recent_price_movement returns a value then draw the stock image with imagenum as the index
            if (imagenum:=self.recent_price_movement()) is not None:
                screen.blit(self.stockimages[imagenum],(self.endingpos[0]+15+round(pricetext.get_width(),-2),self.startingpos[1]+10))
            if type(self) == Player:#text displaying the cash
                screen.blit(font40.render(f'Cash ${self.cash}',1,(255,255,255)),(self.endingpos[0]+15,self.startingpos[1]+50))
        

    