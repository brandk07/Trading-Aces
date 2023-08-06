import pygame
from random import randint
import statistics
from pygame import gfxdraw
import time
from Defs import *

    
class Stock():
    def __init__(self,name,startingvalue_range,volatility,Playerclass,window_offset,stocknames) -> None:
        """Xpos is the starting x position of the graph, startingvalue is the starting value of the stock"""
        self.winset = window_offset
        self.pricepoints = [[0,randint(*startingvalue_range)]]
        self.startingpos,self.endingpos = (0,0),(0,0)
        self.Playerclass = Playerclass
        self.starting_value_range = startingvalue_range
        self.volatility = volatility#determines how much the price can change
        self.temporary_movement = randint(-1*volatility,volatility)#determines overall trend in the movement of the price
        self.movement_length = randint(60,360)#determines the length of the movement (60 is 1 second)
        self.name = name
        self.recent_movementvar = [None,None,(180,180,180)]
        self.control_images = {txt:pygame.transform.scale(pygame.image.load(f'assets/player controls/{txt}.png'),(60,38)) for txt in ['buy','buyhover','sell','sellhover']}
        self.pricereset_time = None
        self.stocknames = stocknames
    def buy_sell(self,player,screen:pygame.Surface,Mousebuttons):
        """buy or sell stock"""
        if self.pricereset_time == None:#if stock is not bankrupt
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
        """returns the recent price movement in percent, None is no recent movement"""
        if self.recent_movementvar[1] != None:#if there is a recent movement then check if it is still recent
            if self.recent_movementvar[1] < time.time():#if it is no longer recent then set it to none
                self.recent_movementvar = [None,None,(180,180,180)]
            elif len(self.pricepoints) < 50:
                self.recent_movementvar = [None,None,(180,180,180)]
            else:#if it is still recent then return the movement
                # if self.recent_movementvar[0] >= 0:
                if (percent:=round(((self.pricepoints[-1][1]/self.pricepoints[-50][1])-1)*100,2)) > 0:
                    self.recent_movementvar[2] = (0,200,0)
                else:
                    self.recent_movementvar[2] = (200,0,0)
                return percent
            
        if len(self.pricepoints) < 50:#if there are less then 10 points then return none
            return None

        if abs(percent:=round(((self.pricepoints[-1][1]/self.pricepoints[-50][1])-1)*100,2)) > 2:#if it is going down by a change greater than 150%
            color = (0,200,0) if percent >= 0 else (200,0,0)
            self.recent_movementvar = [percent,time.time()+3,color]
            return percent
        return None
    
    def price_movement(self,lastprice):
        self.movement_length -= 1
        if self.movement_length <= 0:
            # self.temporary_movement = randint(-4,5)
            self.temporary_movement = randint(-1*(self.volatility-1),self.volatility)
            self.movement_length = randint(60,360)
        
        if self.temporary_movement > 0:#if price greater then set it as the high for the movement
            return lastprice * 1+(randint(-2,self.temporary_movement)/100)#percent based changes (otherwise it can do some really crazy changes)
        elif self.temporary_movement < 0:# if price less then set it as the low for the movement
            changednum = lastprice * 1+(randint(self.temporary_movement,2)/100)
            return changednum
        else:
            return lastprice * 1+(randint(-3,3)/100)
    
    def resize_graph(self):
        medianpoint = statistics.median([point[1] for point in self.pricepoints])
        
        #below we are checking if the max or min is further away from the median point, and then returning the distance from the median point
        if abs(min(self.pricepoints, key=lambda x: x[1])[1]-medianpoint) > abs(max(self.pricepoints, key=lambda x: x[1])[1]-medianpoint):
            return (abs(min(self.pricepoints, key=lambda x: x[1])[1]-medianpoint)+30)#can add a multiplier to make the graph more towards the middle (*1.5)
        return (abs(max(self.pricepoints, key=lambda x: x[1])[1]-medianpoint)+30)
    def bankrupcy(self,screen:pygame.Surface,drawn):
        """returns False if stock is not bankrupt"""	
        if self.pricepoints[-1][1] < 0 and self.pricereset_time == None:#if stock goes bankrupt, and no time has been set
            self.pricereset_time = time.time()
            print(f'{self.name} went bankrupt')
            return False

        elif self.pricereset_time != None and time.time() > self.pricereset_time+5:#if stock goes bankrupt and 5 seconds have passed
            self.pricepoints[-1][1] = randint(*self.starting_value_range)
            self.temporary_movement = randint(-1*(self.volatility-1),self.volatility)
            self.movement_length = randint(60,360); self.pricereset_time = None
            if drawn:
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(255,0,0))#draws the background of the graph red
            return False

        elif self.pricereset_time != None and time.time() < self.pricereset_time+5:#if stock goes bankrupt and less then 5 seconds have passed
            if drawn:
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(255,0,0))#draws the background of the graph red
                screen.blit(fontlist[40].render(f'BANKRUPT',(255,255,255))[0],(self.endingpos[0]+15,self.startingpos[1]+15))
            return False
        return True
    
    def stock_split(self,player:object):
        if self.pricepoints[-1][1] >= 2500:
            player.messagedict[f'{self.name} has split'] = (time.time(),(0,0,200))
            for point in self.pricepoints:
                point[1] *= 0.5
            stock_quantity = len([stock for stock in player.stocks if stock[0] == self.name])
            if stock_quantity > 0:
                player.messagedict[f'You now have {stock_quantity*2} shares of {self.name}'] = (time.time(),(0,0,200))
                for stock in player.stocks.copy():
                    player.stocks.remove(stock)
                    if stock[0] == self.name:
                        player.stocks.append([stock[0],stock[1]*0.5])
                        player.stocks.append([stock[0],stock[1]*0.5])
            

    def update(self,screen,update:bool,player:object,startingpos,endingpos,drawn=True,stocklist=None):
        """updates the graph"""
        if startingpos != self.startingpos or endingpos != self.endingpos:
            xdif = self.startingpos[0]-startingpos[0]
            self.pricepoints = [[point[0]-xdif,point[1]] for point in self.pricepoints]
            #setting the starting and ending positions - where the graphs are located is constantly changing
            self.startingpos = (startingpos[0] - self.winset[0], startingpos[1] - self.winset[1])
            self.endingpos = (endingpos[0] - self.winset[0], endingpos[1] - self.winset[1])
        # If there is only 1 point in the graph then reset the graph with the new starting and ending positions
        if len(self.pricepoints) <= 1: self.pricepoints = [[startingpos[0]-5,self.pricepoints[-1][1]]]

        if type(self) == self.Playerclass:#if it is a Player object
            self.graph(stocklist)#graph the player networth
            self.message(screen)#display the messages
        if self.bankrupcy(screen,drawn):#if stock is not bankrupt
            if not drawn and type(self) == Stock and update:#still running the update function but not drawing
                self.pricepoints.append([self.startingpos[0]-5,self.price_movement(self.pricepoints[-1][1])])#if update is true then add a new point to the graph
                self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable
                self.pricepoints = [[self.startingpos[0],self.pricepoints[-1][1]]]#only keeps one point if not drawn

            elif not drawn and type(self) == Stock and not update:#still running the update function but not drawing
                pass

            else:#if it is being drawn
                gfxdraw.filled_polygon(screen,[(self.endingpos[0],self.startingpos[1]),self.endingpos,(self.startingpos[0],self.endingpos[1]),self.startingpos],(60,60,60))#draws the background of the graph
                if type(self) == Stock and update:#making sure that it is a Stock object and that update is true
                    self.pricepoints.append([self.startingpos[0]-5,self.price_movement(self.pricepoints[-1][1])])#if update is true then add a new point to the graph
                    self.stock_split(player)#if stock is greater then 2500 then split it to keep price affordable
                    # print(self.pricepoints)
                graphsize = self.resize_graph()
                if graphsize <= 0: graphsize = 1#graphsize is the distance from the median point to the max or min point

                medianpoint = statistics.median([point[1] for point in self.pricepoints])# the median point of the graph

                graphheight = (self.endingpos[1]-self.startingpos[1])/2# graphheight is the height of the graph

                #yvaluefinder is a function that takes a value and returns the y value of the point - look in assets for pic of equation
                yvaluefinder = lambda x: int(graphheight+(((medianpoint-x)/graphsize)*graphheight)+self.startingpos[1])

                #new_y_values is a list of all the y values of the points in the graph - had to use so I could access all of the y values for lines in the for loop
                new_y_values = list(map(yvaluefinder,[point[1] for point in self.pricepoints]))

                tenth_width = int((self.startingpos[0]-self.endingpos[0])/10)#tenth is 1/10th of the width of the graph 

                for i,point in enumerate(self.pricepoints):
                    if i >= len(self.pricepoints)-1:
                        pass#if last one in list then don't draw line
                    else:
                        gfxdraw.line(screen,point[0],new_y_values[i],self.pricepoints[i+1][0],new_y_values[i+1],self.recent_movementvar[2])#draws the line between the points
                    if update:
                        point[0] -= 1
                        if point[0] <= self.endingpos[0]: 
                            self.pricepoints.remove(point)
                
                
                # pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.endingpos[0],self.startingpos[1],(self.startingpos[0]-self.endingpos[0]),self.endingpos[1]),10)#draws the perimeter around graphed values
                gfxdraw.rectangle(screen,pygame.Rect(self.endingpos[0],self.startingpos[1],(self.startingpos[0]-self.endingpos[0]),(self.endingpos[1]-self.startingpos[1])),(0,0,0))#draws the perimeter around graphed values

                #draws the text that displays the price of the stock
                text = bold40.render(f' {self.name}',(255,255,255))[0]
                screen.blit(text,(self.endingpos[0]+15,self.startingpos[1]+15))
                screen.blit(fontlist[40].render(f' ${round(self.pricepoints[-1][1],2)}',(255,255,255))[0],(self.endingpos[0]+10,self.endingpos[1]-40))    

                #if recent_price_movement returns a value then draw the stock image with imagenum as the index
                if (percentchange:=self.recent_price_movement()) is not None:
                    # screen.blit(self.stockimages[imagenum],(self.endingpos[0]+15+round(pricetext.get_width(),-2),self.startingpos[1]+10))
                    color = (0,200,0) if percentchange >= 1 else (200,0,0)
                    if type(self) == Stock:
                        screen.blit(fontlist[40].render(f"{'+' if percentchange >= 0 else '-'}{percentchange}%",color)[0],(self.endingpos[0]+15,self.startingpos[1]+45))
                    elif type(self) == self.Playerclass:
                        screen.blit(fontlist[40].render(f"{'+' if percentchange >= 0 else '-'}{percentchange}%",color)[0],(self.endingpos[0]+15,self.startingpos[1]+80))

                if type(self) == self.Playerclass:#text displaying the cash
                    screen.blit(fontlist[40].render(f'Cash ${round(self.cash,2)}',(255,255,255))[0],(self.endingpos[0]+15,self.startingpos[1]+50))

            
        

    