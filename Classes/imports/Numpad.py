import pygame
from pygame import gfxdraw
import pygame.gfxdraw 
from Defs import *

class Numpad:
    def __init__(self,displayText=True,nums=('DEL','0','MAX'),maxDecimals=2,defaultVal=0) -> None:
        self.value = defaultVal
        self.defaultVal = defaultVal
        self.nums = list(nums)
        self.nums.extend([str(i) for i in range(1,10)])
        self.maxDecimals = maxDecimals
        self.numstr = f'{defaultVal}'
        self.numrenders = {name:s_render(name,35,(255,255,255),font='cry') for name in self.nums}
        self.heights = [self.numrenders[name].get_height() for name in self.nums]
        self.widths = [self.numrenders[name].get_width() for name in self.nums]
        self.displayText = displayText

    def getValue(self):
        num = self.numstr
        if self.numstr[-1] == '.':# if the last character is a decimal point
            num = self.numstr[:-1]# remove the decimal point
            if num == '':# if the number is empty
                return self.defaultVal# return the default value
        
        if num.count('.') == 0:# if there are no decimal points
            return int(num)
        return round(float(num),self.maxDecimals)
    def setValue(self,value):
        """Sets the value of the numpad"""	
        self.numstr = str(value)
        self.value = value
    
    def reset(self):
        self.numstr = str(self.defaultVal)
        self.value = self.defaultVal
    
    def getNumstr(self,extraText='',upperCase=False,haveSes=True):
        seS = extraText
        if haveSes:
            s = "S" if upperCase else "s"
            seS += (s if self.getValue() != 1 else "")

        if self.numstr[-1] == '.':
            return f"{self.getValue():,}. "+seS

        if upperCase:
            return f"{self.getValue():,} "+seS
        return f"{self.getValue():,} "+seS
        #     return f"{self.getValue():,.0f} "+extraText+("S" if self.getValue() != 1 else "")
        # return f"{self.getValue():,.0f} "+extraText+("s" if self.getValue() != 1 else "")
    
    def draw(self,screen,coords,wh,extratext,mousebuttons,maxvalue):
        # gfxdraw.box(screen,pygame.Rect(coords,wh),(50,50,50))
        # pygame.draw.rect(screen,(50,50,50),pygame.Rect(coords,wh),)
        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(coords,wh),5,10)
        
        # if self.displayText:
        #     extratext = s_render(f"{int(self.numstr):,.0f} "+extratext+("S" if int(self.numstr) != 1 else ""),45,(255,255,255),font='cry')
        #     topheight = extratext.get_height()*1.8
        #     pygame.draw.rect(screen,(0,0,0),pygame.Rect(coords,(wh[0],topheight)),5,10)
        # # pygame.draw.rect(screen,(0,0,0),pygame.Rect(coords,(wh[0],topheight)),5,10)
        
        # # gfxdraw.box(screen,pygame.Rect((coords[0]+5,coords[1]+5),(wh[0]-10,topheight)),(35,35,35))
        #     screen.blit(extratext,(coords[0]+wh[0]/2-(extratext.get_width()/2),coords[1]+10))

        #     # Triangles for the up and down buttons
        #     leftboxpoints = [(coords[0]+10,coords[1]+10),(coords[0]+45,coords[1]+10),(coords[0]+45,coords[1]+topheight-5),(coords[0]+10,coords[1]+topheight-5)]
        #     rightboxpoints = [(coords[0]+wh[0]-10,coords[1]+10),(coords[0]+wh[0]-45,coords[1]+10),(coords[0]+wh[0]-45,coords[1]+topheight-5),(coords[0]+wh[0]-10,coords[1]+topheight-5)]
        #     gfxdraw.filled_polygon(screen,leftboxpoints,(20,20,20))
        #     gfxdraw.filled_polygon(screen,rightboxpoints,(20,20,20))
        #     pygame.draw.polygon(screen,(0,0,0),leftboxpoints,3)
        #     pygame.draw.polygon(screen,(0,0,0),rightboxpoints,3)
            

        #     lefttripoints = [(coords[0]+15,coords[1]+topheight/2),(coords[0]+40,coords[1]+12),(coords[0]+40,coords[1]+topheight-12)]
        #     righttripoints = [(coords[0]+wh[0]-15,coords[1]+topheight/2),(coords[0]+wh[0]-40,coords[1]+12),(coords[0]+wh[0]-40,coords[1]+topheight-12)]
        #     gfxdraw.filled_polygon(screen,lefttripoints,(150,150,150))
        #     gfxdraw.filled_polygon(screen,righttripoints,(150,150,150))

        #     if point_in_polygon(pygame.mouse.get_pos(),leftboxpoints):
        #         if mousebuttons == 1 and int(self.numstr) > 0: self.numstr = str(int(self.numstr)-1)
        #     if point_in_polygon(pygame.mouse.get_pos(),rightboxpoints):
        #         if mousebuttons == 1: self.numstr = str(int(self.numstr)+1)
        maxvalue = round(maxvalue,self.maxDecimals)
        # if self.numstr == '.': self.numstr = str(self.defaultVal)
        if self.numstr == '.': 
            '0.'
        else:
            if float(self.numstr) > maxvalue:
                self.numstr = str(maxvalue)

            if float(self.numstr) != int(float(self.numstr)):
                self.numstr = str(round(float(self.numstr),self.maxDecimals))

        for row in range(4):
            for col in range(3):
                ind = row*3+col
                # coords and wh
                x = coords[0]+wh[0]*.05+5+(col)*(wh[0]*.9)/3
                y = coords[1]+wh[1]*.05+(row)*(((wh[1])*.9)/4)
                w = (wh[0]*.9)/3 - 10
                h = ((wh[1])*.9)/4 - 10 

                rect = pygame.Rect(x,y,w,h)
                color = (80,80,80)
                

                if rect.collidepoint(pygame.mouse.get_pos()):
                    
                    color = (135,135,135,120)
                    # pygame.gfxdraw.filled_polygon(screen,[(x,y),(x+w,y),(x+w,y+h),(x,y+h)],color)
                    pygame.draw.rect(screen,color,rect,border_radius=10)
                    if mousebuttons == 1:
                        if self.nums[ind] == 'DEL' and len(self.numstr) > 1:
                            self.numstr = self.numstr[:-1]
                        elif self.nums[ind] == 'DEL' and len(self.numstr) == 1:
                            self.numstr = str(self.defaultVal)
                        elif self.nums[ind] == 'MAX':
                            if maxvalue == 0:
                                errors.addMessage(f"Max Quantity = {maxvalue}")
                            self.numstr = str(maxvalue)
                        elif self.nums[ind] == '.': 
                            if '.' not in self.numstr:
                                self.numstr += '.'
                        else:
                            if '.' in self.numstr and len(self.numstr.split('.')[1]) < self.maxDecimals:
                                self.numstr += self.nums[ind]
                            elif '.' not in self.numstr:
                                self.numstr += self.nums[ind]
   
                        self.numstr = self.numstr.lstrip(str(self.defaultVal))
                        if self.numstr == '':
                            self.numstr = str(self.defaultVal)
                        if self.numstr == '.': 
                            '0.'
                        else:
                            if float(self.numstr) > maxvalue:
                                errors.addMessage(f"Max Quantity = {maxvalue}")
                                self.numstr = str(maxvalue)

                # gfxdraw.box(screen,rect,color)
                # pygame.draw.rect(screen,color,rect,5,10)
                
                pos_x = x + w/2 - self.widths[ind]/2
                pos_y = y + h/2 - self.heights[ind]/2

                # Draw the source image onto the screen
                screen.blit(self.numrenders[self.nums[ind]], (pos_x, pos_y))
        # for i in range(12):
            # gfxdraw.box(screen,pygame.Rect((coords[0]+(i%3)*(wh[0]/3),coords[1]+(i//3)*(wh[1]/4)),(wh[0]/3,wh[1]/4)),(100,100,100))
        #     screen.blit(s_render(self.nums[i],25,(255,255,255),font='cry'),(coords[0]+(i%3)*(wh[0]/3),coords[1]+(i//3)*(wh[1]/4)))
