import pygame
from Defs import *

class UI_controls():
    def __init__(self,windowoffset) -> None:
        path = 'Assets/UI controls/'
        self.images = {
            "pause":pygame.image.load(path+"/pausebutton.png").convert_alpha(),
            "play":pygame.image.load(path+"playbutton.png").convert_alpha(),
            "fastforward":pygame.image.load(path+"fastforwardbutton.png").convert_alpha(),
            "blankbutton":pygame.image.load(path+"blankbutton.png").convert_alpha(),
        }

        self.winset = windowoffset
        for key,image in self.images.items():
            image = pygame.transform.scale(image,(50,52))
            surface = pygame.Surface((image.get_width()+10,image.get_height()+10))
            surface.fill((110,110,110))
            surface.blit(image,(5,5))
            self.images[key] = surface.convert_alpha()

        self.gameplay_speed = 3
        self.playing = True

        self.pauseplayxy = (805+self.winset[0],980+self.winset[1])
        self.fastwardxy = (805+self.winset[0]+70,980+self.winset[1])

        self.playrect = pygame.Rect(self.pauseplayxy[0],self.pauseplayxy[1],self.images['play'].get_width(),self.images['play'].get_height())
        self.fastrect = pygame.Rect(self.fastwardxy[0],self.fastwardxy[1],self.images['fastforward'].get_width(),self.images['fastforward'].get_height())
        self.blankrect = pygame.Rect(self.fastwardxy[0]+70,self.fastwardxy[1],self.images['blankbutton'].get_width(),self.images['blankbutton'].get_height())
        self.gamespeedtexts = [fontlist[40].render(f'x{speed}',(0,0,0))[0] for speed in range(0,4)]
    def logic(self,Tick:int):
        if self.playing:#if not paused
            if self.gameplay_speed == 1 and not Tick % 3:#if halfspeed, and on an odd tick
                return True
            if self.gameplay_speed == 2 and Tick % 2:#if not paused, not fastforward, and on an even tick
                return True
            elif self.gameplay_speed == 3:#if fastforward, and on any tick
                return True
        else:#if paused
            return False
        
    def draw(self,screen,mousebuttons:int,menudrawn:bool):
        
        if self.playing:
            screen.blit(self.images['pause'],self.pauseplayxy)
        else:
            screen.blit(self.images['play'],self.pauseplayxy)

        
        screen.blit(self.images['fastforward'],self.fastwardxy )
        
        screen.blit(self.images['blankbutton'],(self.fastwardxy[0]+70,self.fastwardxy[1]))
        if self.playing:
            screen.blit(self.gamespeedtexts[self.gameplay_speed],(self.fastwardxy[0]+88,self.fastwardxy[1]+17))
        else:
            screen.blit(self.gamespeedtexts[0],(self.fastwardxy[0]+88,self.fastwardxy[1]+17))
        
        self.clicksensing(mousebuttons)#740,750
    def clicksensing(self,mousebuttons:int):
        mousex,mousey = pygame.mouse.get_pos()
        
        if mousebuttons == 1:
            if self.playrect.collidepoint(mousex,mousey):
                self.playing = not self.playing
            elif self.fastrect.collidepoint(mousex,mousey) or self.blankrect.collidepoint(mousex,mousey):
                if not self.playing:#if paused, then play
                    self.playing = True
                    self.gameplay_speed = 1
                else:#if playing, then change speed
                    if self.gameplay_speed == 3:
                        self.gameplay_speed = 1
                    else:
                        self.gameplay_speed += 1