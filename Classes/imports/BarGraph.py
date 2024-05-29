import pygame
import pygame.gfxdraw
from Defs import *

class BarGraph:
    def __init__(s,name:str,withHeight:list,values:list,colors:list,pos:list) -> None:
        """Creates a bar graph with values and colors, make sure the indices of the values and colors match up."""
        s.width = withHeight[0]
        s.height = withHeight[1]
        s.values = values
        s.colors = colors
        s.pos = pos
        s.nametext = name
        s.name = s_render(name,47,(0,0,0))
    
    def draw(s,screen:pygame.Surface,position=None):
        pos = s.pos if position == None else position
        barwidth = (s.width/len(s.values))*.9
        scaleFactor = (s.height-25)/max(s.values)
        for i,value in enumerate(s.values):
            startx = pos[0]+i*barwidth+10
            starty = pos[1]+s.height-10
            coords = [(startx,starty),
                      (startx+barwidth,starty),
                      (startx+barwidth,starty-(value*scaleFactor)),
                      (startx,starty-(value*scaleFactor))]
            pygame.gfxdraw.filled_polygon(screen,coords,s.colors[i])
        x = s.pos[0]+s.width/2-s.name.get_width()/2
        y = s.pos[1]+s.height
        screen.blit(s.name,(x,y))

    def updateValues(s,values,colors):
        s.values = values
        s.colors = colors
