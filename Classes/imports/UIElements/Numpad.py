import pygame
from pygame import gfxdraw
import pygame.gfxdraw 
from Defs import *

class Numpad:
    def __init__(self,displayText=True,nums=('DEL','0','MAX'),maxDecimals=2,defaultVal=0,txtSize=35) -> None:
        self.value = defaultVal
        self.defaultVal = defaultVal
        self.txtSize = txtSize
        self.nums = list(nums)
        self.nums.extend([str(i) for i in range(1,10)])
        self.maxDecimals = maxDecimals
        self.numstr = f'{defaultVal}'
        # self.numrenders = {name:s_render(name,35,(255,255,255),font='cry') for name in self.nums}
        # self.heights = [self.numrenders[name].get_height() for name in self.nums]
        # self.widths = [self.numrenders[name].get_width() for name in self.nums]
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

    def doLogic(self,screen:pygame.Surface,mousebuttons,rect:pygame.Rect,ind,maxvalue):
        if rect.collidepoint(pygame.mouse.get_pos()):
                    
            color = (135,135,135,120)
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
                    '0.' if self.maxDecimals != 0 else '0'
                else:
                    if float(self.numstr) > maxvalue:
                        errors.addMessage(f"Max Quantity = {maxvalue}")
                        self.numstr = str(maxvalue)

        # gfxdraw.box(screen,rect,color)
        # pygame.draw.rect(screen,color,rect,5,10)
        # print(self.nums,ind)
        num = self.nums[ind]
        numRender = s_render(num,self.txtSize,(255,255,255),font='cry')
        pos_x = rect.x + rect.w/2
        pos_y = rect.y + rect.h/2

        # Draw the source image onto the screen
        # screen.blit(self.numrenders[self.nums[ind]], (pos_x, pos_y))
        drawCenterRendered(screen,numRender,(pos_x,pos_y))

    def draw(self,screen,coords,wh,extratext,mousebuttons,maxvalue):

        maxvalue = round(maxvalue,self.maxDecimals) if self.maxDecimals != 0 else int(maxvalue)

        if self.numstr == '.': 
            '0.' if self.maxDecimals != 0 else '0'
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
                self.doLogic(screen,mousebuttons,rect,ind,maxvalue)

                
        # for i in range(12):
            # gfxdraw.box(screen,pygame.Rect((coords[0]+(i%3)*(wh[0]/3),coords[1]+(i//3)*(wh[1]/4)),(wh[0]/3,wh[1]/4)),(100,100,100))
        #     screen.blit(s_render(self.nums[i],25,(255,255,255),font='cry'),(coords[0]+(i%3)*(wh[0]/3),coords[1]+(i//3)*(wh[1]/4)))
class SideWaysNumPad(Numpad):
    def __init__(self, displayText=True, nums=('DEL', '0', 'MAX'), maxDecimals=2, defaultVal=0):
        super().__init__(displayText, nums, maxDecimals, defaultVal)
        self.nums = list(nums)
        self.nums.extend([str(i) for i in [1,4,7,2,5,8,3,6,9]])

    def draw(self,screen,coords,wh,extratext,mousebuttons,maxvalue):

        maxvalue = round(maxvalue,self.maxDecimals) if self.maxDecimals != 0 else int(maxvalue)

        if self.numstr == '.': 
            '0.' if self.maxDecimals != 0 else '0'
        else:
            if float(self.numstr) > maxvalue:
                self.numstr = str(maxvalue)

            if float(self.numstr) != int(float(self.numstr)):
                self.numstr = str(round(float(self.numstr),self.maxDecimals))

        for col in range(4):
            for row in range(3):
                ind = row+col*3
                # coords and wh
                x = coords[0]+wh[0]*.05+5+(col)*(wh[0]*.9)/4
                y = coords[1]+wh[1]*.05+(row)*(((wh[1])*.9)/3)
                w = (wh[0]*.9)/4 - 10
                h = ((wh[1])*.9)/3 - 10 

                rect = pygame.Rect(x,y,w,h)
                self.doLogic(screen,mousebuttons,rect,ind,maxvalue)