import pygame
import pygame.gfxdraw
from Defs import *

class BarGraph:
    def __init__(s,name:str,withHeight:list,pos:list) -> None:
        """Creates a bar graph with values and colors, make sure the indices of the values and colors match up."""
        s.width = withHeight[0]
        s.height = withHeight[1]
        s.values : list[float]  = []
        s.colors : list[tuple] = []
        s.units : list[str] = []
        s.pos = pos
        s.nametext = name
        s.name = s_render(name,47,(0,0,0))
    
    def updateValues(s,values:list[float],colors:list[tuple],units:list[str]):
        """Updates the values and colors of the bar graph."""
        s.values = values
        s.colors = colors
        s.units = units
    
    def draw(s,screen:pygame.Surface,position=None):
        """Draws the bar graph to the screen."""
        pos = s.pos if position == None else position
        barwidth = (s.width/len(s.values))
        scaleFactor = (s.height-25)/max(s.values)
        mousex,mousey = pygame.mouse.get_pos()
        # pygame.gfxdraw.rectangle(screen,pygame.Rect(pos[0],pos[1]+s.height,s.width,2),(0,0,0))
        pygame.gfxdraw.filled_polygon(screen,[
            (pos[0],pos[1]+s.height-5),
            (pos[0]+s.width,pos[1]+s.height-5),
            (pos[0]+s.width,pos[1]+s.height),
            (pos[0],pos[1]+s.height)
            ],(0,0,0))


        for i,value in enumerate(s.values):
            startx = pos[0]+i*barwidth+10
            starty = pos[1]+s.height-10
            # coords = [(startx,starty),
            #           (startx+barwidth,starty),
            #           (startx+barwidth,starty-(value*scaleFactor)),
            #           (startx,starty-(value*scaleFactor))]
            # pygame.gfxdraw.filled_polygon(screen,coords,s.colors[i])
            pygame.draw.rect(screen,s.colors[i],(startx,starty-value*scaleFactor,barwidth-10,value*scaleFactor),border_top_left_radius=10,border_top_right_radius=10)

        for i,value in enumerate(s.values):
            startx = pos[0]+i*barwidth+10
            starty = pos[1]+s.height-10
            if startx < mousex < startx+barwidth and s.pos[1] < mousey < starty:
                pygame.gfxdraw.filled_circle(screen,int(startx+(barwidth-10)/2),int(starty-(value*scaleFactor)),5,(200,200,200))
                newstr = str(round(value,2))+s.units[i] if s.units[i] == '%' else s.units[i]+str(round(value,2))
                
                valueText = s_render(newstr,50,(0,0,0))
                x = s.pos[0]+s.width/2-valueText.get_width()/2
                y = s.pos[1]+s.height/2-20
                pygame.draw.rect(screen,s.colors[i],(s.pos[0],y-20,s.width,valueText.get_height()+40),border_radius=10)
                pygame.draw.rect(screen,(0,0,0),(s.pos[0],y-20,s.width,valueText.get_height()+40),width=5,border_radius=10)
                screen.blit(valueText,(x,y))
                

        x = s.pos[0]+s.width/2-s.name.get_width()/2
        y = s.pos[1]+s.height+5
        screen.blit(s.name,(x,y))

    
