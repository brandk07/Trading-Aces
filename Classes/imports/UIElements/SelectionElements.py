import pygame
from Defs import *
import math

class SelectionBar:
    """A bar that allows the user to select from a list of strings"""
    def __init__(self,horizontal=True,allowSelcNone=False,rounded=15) -> None:
        # self.__annotations__
        self.selected = None
        self.rounded = rounded
        self.horizontal = horizontal
        self.allowSelcNone = allowSelcNone
    def getSelected(self):
        """Returns the selected string"""
        return self.selected
    def setSelected(self,selected):
        """Sets the selected string"""
        self.selected = selected
        
    def draw(self,screen:pygame.Surface,data:list[str],coords:tuple[int],wh:tuple[int],mousebuttons,colors:list[tuple]=None,txtsize:int=36,condensed=False):
        """Data is a list of strings that can be selected
        the length of data can be changed, but it must be at least 1
        will auto select the first element in the list"""	
        assert len(data) > 0, "Data must have at least one element"

        if self.selected == None or self.selected not in data:
            self.selected = data[0] if not self.allowSelcNone else None
        
        if colors == None:
            colors = [(255,255,255)]*len(data)

        x,y = coords
        w,h = wh
        spacing = math.ceil(w/len(data)) if self.horizontal else math.ceil(h/len(data))
        # pygame.draw.rect(screen,(20,20,20),pygame.Rect(x,y,w,h),border_radius=25)# Ovalish shape that all elements will be drawn on
        changed = False
        for i,txt in enumerate(data):
            rtxt = s_render(txt,txtsize,colors[i])

            if self.horizontal:
                if txt == self.selected:
                    pygame.draw.rect(screen,(10,10,10),pygame.Rect(x+(i*spacing)+5,y,spacing-10,h),border_radius=self.rounded)
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(x+(i*spacing)+5,y,spacing-10,h),width=5,border_radius=self.rounded)
                txtx = x+(i*spacing)+(spacing//2)-(rtxt.get_width()//2)
                txty = y+(h//2)-(rtxt.get_height()//2)
                rect = pygame.Rect(x+(i*spacing),y,spacing,h)
            else:
                if txt == self.selected:
                    pygame.draw.rect(screen,(10,10,10),pygame.Rect(x,y+(i*spacing)+5,w,spacing-10),border_radius=self.rounded)
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(x,y+(i*spacing)+5,w,spacing-10),width=5,border_radius=self.rounded)
                txtx = x+(w//2)-(rtxt.get_width()//2)
                txty = y+(i*spacing)+(spacing//2)-(rtxt.get_height()//2)
                rect = pygame.Rect(x,y+(i*spacing),w,spacing)
            screen.blit(rtxt,(txtx,txty))

            if rect.collidepoint(pygame.mouse.get_pos()) and mousebuttons == 1:
                if not self.selected == txt:
                    soundEffects['generalClick'].play()
                self.selected = txt if txt != self.selected else None
                if not self.allowSelcNone and self.selected == None:
                    self.selected = txt
                changed = True
        return changed
        

class MenuSelection:
    """Similar to SelectionBar, but with a different design more suited for switching between menus"""
    def __init__(self,coords,wh,choices:list,txtsize,colors=None) -> None:
        assert len(choices) == len(colors) if colors else True
        self.coords = coords
        self.wh = wh
        self.colors = colors if colors else [(0,0,0) for _ in range(len(choices))]
        self.choiceTxts : list = choices
        self.choices = [s_render(choice,txtsize,self.colors[i]) for i,choice in enumerate(choices)]
        
        self.selected = 0# the index of the selected choice
    def getSelected(self,index=False):
        """Returns the selected choice or its index"""
        return self.choiceTxts[self.selected] if not index else self.selected
    def setSelected(self,index):
        """Sets the selected choice"""
        if type(index) == int:
            self.selected = index
        else:
            assert index in self.choiceTxts, "The index must be in the list of choices"
            self.selected = self.choiceTxts.index(index)
    def draw(self,screen,mousebuttons):
        """Draws the menu selection onto the screen"""
        width  = self.wh[0]//len(self.choices)
        for i,choice in enumerate(self.choices):
            drawCenterRendered(screen,choice,(self.coords[0]+width//2+i*width,self.coords[1]+self.wh[1]//2))
            if self.selected == i:# Draws the selected choice (choice in white)
                # draw a line under the selected choice
                ylevel = self.coords[1]+self.wh[1]-20
                pygame.draw.line(screen,(255,255,255),(self.coords[0]+i*width+20,ylevel),(self.coords[0]+i*width+width-20,ylevel),4)
    
            if i != len(self.choices)-1:# Draws a vertical line to separate the choices
                pygame.draw.line(screen,(0,0,0),(self.coords[0]+width*(i+1),self.coords[1]+20),(self.coords[0]+width*(i+1),self.coords[1]+self.wh[1]-20),4)

            if pygame.Rect(self.coords[0]+i*width,self.coords[1],width,self.wh[1]).collidepoint(*pygame.mouse.get_pos()) and mousebuttons == 1:
                self.selected = i
                soundEffects['menuClick'].play()
        pygame.draw.rect(screen,(0,0,0),(*self.coords,*self.wh),5,10)# draw the border of the whole menu