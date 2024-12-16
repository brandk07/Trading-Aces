import pygame
import pygame.gfxdraw
from Defs import *

class BarGraph:
    def __init__(s,name:str,pos:list,wh:list) -> None:
        """Creates a bar graph with values and colors, make sure the indices of the values and colors match up."""
        s.width = wh[0]
        s.height = wh[1]
        s.values : list[float]  = []
        s.colors : list[tuple] = []
        s.units : list[str] = []
        s.pos = pos
        s.nametext = name
        s.name = s_render(name,47,(255,255,255))
    
    def updateValues(s,values:list[float],colors:list[tuple],units:list[str]):
        """Updates the values and colors of the bar graph."""
        s.values = values
        s.colors = colors
        s.units = units
    def changeName(s,name:str):
        """Changes the name of the bar graph."""
        s.nametext = name
        s.name = s_render(name,47,(255,255,255))
    def draw(s,screen:pygame.Surface,position=None,absoluteScale=None):
        """Draws the bar graph to the screen, position is optional,
        with absoluteScale you can input the max it will always scale to that value rather than the max value of the data"""
        # assert absoluteScale == None or type(absoluteScale) == int or type(absoluteScale) == float, 'absoluteScale must be an int or float'
        assert position == None or type(position) == list or type(position) == tuple, 'position must be a list/tuple'

        pos = s.pos if position == None else position
        barwidth = (s.width/len(s.values))
        scaleFactor = (s.height-25)/max(s.values) if absoluteScale == None else (s.height-25)/absoluteScale
        mousex,mousey = pygame.mouse.get_pos()

        pygame.gfxdraw.filled_polygon(screen,[
            (pos[0],pos[1]+s.height-5),
            (pos[0]+s.width,pos[1]+s.height-5),
            (pos[0]+s.width,pos[1]+s.height),
            (pos[0],pos[1]+s.height)
            ],(0,0,0))

        selectIndex = None# None or values Index
        for i,value in enumerate(s.values):
            startx = pos[0]+i*barwidth+10
            starty = pos[1]+s.height-10
            color = s.colors[i]

            if startx < mousex < startx+barwidth and s.pos[1] < mousey < starty:# if mouse is over bar
                selectIndex = i# set selectIndex to the index of the bar
                color = tuple(min(color[i]*1.5,255) for i in range(3))# make the color brighter

            pygame.draw.rect(screen,color,(startx,starty-value*scaleFactor,barwidth-10,value*scaleFactor),border_top_left_radius=10,border_top_right_radius=10)
        
        if selectIndex != None:# Drawing the box of text, after so it is on top of the bars
            valueTxt = str(limit_digits(s.values[selectIndex],24,s.values[selectIndex]>1000))
            newstr = valueTxt+s.units[i] if s.units[i] == '%' else s.units[i]+valueTxt
            valueText = s_render(newstr,50,(0,0,0))
            x = s.pos[0]+s.width/2-valueText.get_width()/2
            y = s.pos[1]+s.height/2-20
            valw = valueText.get_width()
            pygame.draw.rect(screen,tuple(min(s.colors[selectIndex][i]*1.5,255) for i in range(3)),(x-15,y-20,valw+30,valueText.get_height()+40),border_radius=10)
            pygame.draw.rect(screen,(0,0,0),(x-15,y-20,valw+30,valueText.get_height()+40),width=5,border_radius=10)
            # draw a white box on the bottom of the bar
            gfxdraw.filled_polygon(screen,[
                (pos[0]+selectIndex*barwidth+10,pos[1]+s.height-15),
                (pos[0]+(selectIndex+1)*barwidth,pos[1]+s.height-15),
                (pos[0]+(selectIndex+1)*barwidth,pos[1]+s.height-10),
                (pos[0]+selectIndex*barwidth+10,pos[1]+s.height-10)
                ],(255,255,255))
            # pygame.draw.rect(screen,tuple(min(s.colors[selectIndex][i]*1.5,255) for i in range(3)),(s.pos[0],y-20,s.width,valueText.get_height()+40),border_radius=10)
            # pygame.draw.rect(screen,(0,0,0),(s.pos[0],y-20,s.width,valueText.get_height()+40),width=5,border_radius=10)
            screen.blit(valueText,(x,y))

        x = s.pos[0]+s.width/2-s.name.get_width()/2
        y = s.pos[1]+s.height+5
        screen.blit(s.name,(x,y))

    
