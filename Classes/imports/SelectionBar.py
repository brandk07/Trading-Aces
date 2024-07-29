import pygame
from Defs import *
import math

class SelectionBar:
    def __init__(self) -> None:
        # self.__annotations__
        self.selected = None
    def getSelected(self):
        return self.selected
    def draw(self,screen:pygame.Surface,data:list[str],coords:tuple[int],wh:tuple[int],colors:list[tuple]=None,txtsize:int=36):
        """Data is a list of strings that can be selected
        the length of data can be changed, but it must be at least 1
        will auto select the first element in the list"""	
        assert len(data) > 0, "Data must have at least one element"

        if self.selected == None or self.selected not in data:
            self.selected = data[0]
        
        if colors == None:
            colors = [(255,255,255)]*len(data)

        x,y = coords
        w,h = wh
        spacing = math.ceil(w/len(data))
        # pygame.draw.rect(screen,(20,20,20),pygame.Rect(x,y,w,h),border_radius=25)# Ovalish shape that all elements will be drawn on
        changed = False
        for i,txt in enumerate(data):
            rtxt = s_render(txt,txtsize,colors[i])

            if txt == self.selected:
                pygame.draw.rect(screen,(10,10,10),pygame.Rect(x+(i*spacing)+5,y,spacing-10,h),border_radius=25)

            pygame.draw.rect(screen,(0,0,0),pygame.Rect(x+(i*spacing)+5,y,spacing-10,h),width=5,border_radius=25)
            

                
            txtx = x+(i*spacing)+(spacing//2)-(rtxt.get_width()//2)
            txty = y+(h//2)-(rtxt.get_height()//2)
            screen.blit(rtxt,(txtx,txty))
            if pygame.Rect(x+(i*spacing),y,spacing,h).collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    self.selected = txt
                    changed = True
        return changed
        


        # for i,dat in enumerate(data):
        #     text = fontlist[36].render(dat,(255,255,255))[0]
        #     screen.blit(text,(x+5,y+(i*30)+5))
        # return pygame.Rect(x,y,width,height)