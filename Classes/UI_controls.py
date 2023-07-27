import pygame
from Defs import *

class UI_controls():
    def __init__(self) -> None:
        path = 'Assets/UI controls/'
        self.images = {
            "reverse":pygame.transform.flip(pygame.image.load(path+"fastforward.png").convert_alpha(),True,False),
            "pause":pygame.image.load(path+"/pause.png").convert_alpha(),
            "play":pygame.image.load(path+"play.png").convert_alpha(),
            "fastforward":pygame.image.load(path+"fastforward.png").convert_alpha(),
        }
        for key,image in self.images.items():
            surface = pygame.Surface((image.get_width(),image.get_height()))
            surface.fill((110,110,110))
            surface.blit(image,(0,0))
            self.images[key] = surface

        self.imagelengths = [image.get_width()+15 for image in self.images.values()]
        self.gameplay_speed = 2
        self.playing = True
    
    def logic(self,Tick:int):
        if self.playing:#if not paused
            if self.gameplay_speed == 1 and Tick == 0:#if halfspeed, and on an odd tick
                return True
            if self.gameplay_speed == 2 and Tick % 2:#if not paused, not fastforward, and on an even tick
                return True
            elif self.gameplay_speed == 3:#if fastforward, and on any tick
                return True
        else:#if paused
            return False
        
    def draw(self,screen,mousebuttons:int):
        for i,image in enumerate(self.images.values()):
            screen.blit(image,(1605+sum([self.imagelengths[x] for x in range(i)]),405))
        self.clicksensing(mousebuttons)#740,750
        
    def clicksensing(self,mousebuttons:int):
        mousex,mousey = pygame.mouse.get_pos()            
        if mousebuttons == 1:
            print(mousex,mousey)
            for i,image in enumerate(self.images.values()):
                if mousex > 1605+sum([self.imagelengths[x] for x in range(i)]) and mousex < 1605+sum([self.imagelengths[x] for x in range(i)])+image.get_width() and mousey > 405 and mousey < 405+image.get_height():
                    print('clicked',i)
                    if i == 0:#if reverse
                        if self.gameplay_speed == 2:
                            self.gameplay_speed = 1
                        elif self.gameplay_speed == 3:
                            self.gameplay_speed = 2
                    elif i == 1:#if pause
                        self.playing = False
                    elif i == 2:#if play
                        self.playing = True
                        self.gameplay_speed = 1
                    elif i == 3:#if fastforward
                        if self.gameplay_speed == 2:
                            self.gameplay_speed = 3
                        if self.gameplay_speed == 1:
                            self.gameplay_speed = 2
        