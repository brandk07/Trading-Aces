import pygame
from pygame import gfxdraw 
from Defs import *

class Numpad:
    def __init__(self) -> None:
        self.value = 0
        self.nums = ['DEL','0','MAX']
        self.nums.extend([str(i) for i in range(1,10)])
        self.numstr = '0'
        self.numrenders = {name:s_render(name,35,(255,255,255),font='cry') for name in self.nums}
        self.heights = [self.numrenders[name].get_height() for name in self.nums]
        self.widths = [self.numrenders[name].get_width() for name in self.nums]

    def get_value(self):
        return int(self.numstr)
    
    def draw(self,screen,coords,wh,extratext,mousebuttons,maxvalue):
        gfxdraw.box(screen,pygame.Rect(coords,wh),(50,50,50))
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(coords,wh),5)
        extratext = s_render(f"{int(self.numstr):,.0f} "+extratext+("S" if int(self.numstr) != 1 else ""),45,(255,255,255),font='cry')
        topheight = extratext.get_height()*1.8
        gfxdraw.box(screen,pygame.Rect((coords[0]+5,coords[1]+5),(wh[0]-10,topheight)),(35,35,35))
        screen.blit(extratext,(coords[0]+wh[0]/2-(extratext.get_width()/2),coords[1]+10))

        # Triangles for the up and down buttons
        leftboxpoints = [(coords[0]+10,coords[1]+10),(coords[0]+45,coords[1]+10),(coords[0]+45,coords[1]+topheight-5),(coords[0]+10,coords[1]+topheight-5)]
        rightboxpoints = [(coords[0]+wh[0]-10,coords[1]+10),(coords[0]+wh[0]-45,coords[1]+10),(coords[0]+wh[0]-45,coords[1]+topheight-5),(coords[0]+wh[0]-10,coords[1]+topheight-5)]
        gfxdraw.filled_polygon(screen,leftboxpoints,(20,20,20))
        gfxdraw.filled_polygon(screen,rightboxpoints,(20,20,20))
        pygame.draw.polygon(screen,(0,0,0),leftboxpoints,3)
        pygame.draw.polygon(screen,(0,0,0),rightboxpoints,3)
        

        lefttripoints = [(coords[0]+15,coords[1]+topheight/2),(coords[0]+40,coords[1]+12),(coords[0]+40,coords[1]+topheight-12)]
        righttripoints = [(coords[0]+wh[0]-15,coords[1]+topheight/2),(coords[0]+wh[0]-40,coords[1]+12),(coords[0]+wh[0]-40,coords[1]+topheight-12)]
        gfxdraw.filled_polygon(screen,lefttripoints,(150,150,150))
        gfxdraw.filled_polygon(screen,righttripoints,(150,150,150))
        
        if point_in_polygon(pygame.mouse.get_pos(),leftboxpoints):
            if mousebuttons == 1 and int(self.numstr) > 0: self.numstr = str(int(self.numstr)-1)
        if point_in_polygon(pygame.mouse.get_pos(),rightboxpoints):
            if mousebuttons == 1: self.numstr = str(int(self.numstr)+1)

        if int(self.numstr) > maxvalue:
            self.numstr = str(maxvalue)

        for row in range(4):
            for col in range(3):
                ind = row*3+col
                # coords and wh
                x = coords[0]+wh[0]*.05+5+(col)*(wh[0]*.9)/3
                y = coords[1]+wh[1]*.05+(row)*(((wh[1]-topheight)*.9)/4)+topheight
                w = (wh[0]*.9)/3 - 10
                h = ((wh[1]-topheight)*.9)/4 - 10 

                rect = pygame.Rect(x,y,w,h)
                color = (60,60,60)

                if rect.collidepoint(pygame.mouse.get_pos()):
                    color = (120,120,120)
                    if mousebuttons == 1:
                        if self.nums[ind] == 'DEL' and len(self.numstr) > 1:
                            self.numstr = self.numstr[:-1]
                        elif self.nums[ind] == 'DEL' and len(self.numstr) == 1:
                            self.numstr = '0'
                        elif self.nums[ind] == 'MAX':
                            self.numstr = str(maxvalue)
                        else:
                            self.numstr += self.nums[ind]
                        self.numstr = self.numstr.lstrip('0')
                        if self.numstr == '':
                            self.numstr = '0'

                        if int(self.numstr) > maxvalue:
                            self.numstr = str(maxvalue)

                gfxdraw.box(screen,rect,color)
                
                pos_x = x + w/2 - self.widths[ind]/2
                pos_y = y + h/2 - self.heights[ind]/2

                # Draw the source image onto the screen
                screen.blit(self.numrenders[self.nums[ind]], (pos_x, pos_y))
        # for i in range(12):
            # gfxdraw.box(screen,pygame.Rect((coords[0]+(i%3)*(wh[0]/3),coords[1]+(i//3)*(wh[1]/4)),(wh[0]/3,wh[1]/4)),(100,100,100))
        #     screen.blit(s_render(self.nums[i],25,(255,255,255),font='cry'),(coords[0]+(i%3)*(wh[0]/3),coords[1]+(i//3)*(wh[1]/4)))
