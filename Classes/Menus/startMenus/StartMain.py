import pygame
import pygame.camera
from Defs import *
from pygame import gfxdraw
from Classes.imports.UIElements.SelectionElements import SelectionBar
from Classes.Menus.startMenus.CreateMenu import CreateMenu
from Classes.imports.Animations import BuyAnimation
from Classes.Menus.startMenus.StartMenu import StartMenu

def get_key_name(key_event, shift_pressed=False):
    """
    Convert pygame key event to readable name with case sensitivity
    Args:
        key_event: pygame key event
        shift_pressed: boolean indicating if shift is pressed
    """
    key_name = pygame.key.name(key_event)
    dictKeys = ["return", "space", "backspace", "left shift", "right shift", "left ctrl", "right ctrl", "left alt", "right alt", "tab", "escape", "[", "]", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", ";", "'", ",", ".", "/", "`"]
    dictValsShift = ["Enter", " ", "Backspace", "Shift", "Shift", "Ctrl", "Ctrl", "Alt", "Alt", "Tab", "Esc", "{", "}","!","@","#","$","%","^","&","*","(",")","_","+",":",'"',"<",">","?","~"]
    dictValsNorm = ["Enter", " ", "Backspace", "Shift", "Shift", "Ctrl", "Ctrl", "Alt", "Alt", "Tab", "Esc", "[", "]", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", ";", "'", ",", ".", "/", "`"]
    special_keys = dict(zip(dictKeys, dictValsShift if shift_pressed else dictValsNorm))
   

    # Handle letters with case
    if len(key_name) == 1 and key_name.isalpha():
        return key_name.upper() if shift_pressed else key_name.lower()
        
    return special_keys.get(key_name, key_name)

def get_shift_state():
    """Check if shift or caps lock is active"""
    mods = pygame.key.get_mods()
    shift_pressed = mods & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT)
    caps_on = mods & pygame.KMOD_CAPS
    
    # Return True if either shift is held or caps lock is on (but not both)
    return bool(shift_pressed) ^ bool(caps_on)


class StartMain:
    def __init__(self) -> None:

        self.gameMode = 'start'# play, create, settings , credit, or start
        self.menus : str[CreateMenu] = {'create':CreateMenu(self),'play':None,'settings':None,'credit':None,'start':StartMenu()}
        self.pastRuns = {}# the past runs that the player has done

    def loadPastRuns(self):
        pass
    def validName(self,name:str):
        """returns True if the name is valid"""
        if len(name) < 3:
            return "-Name must be at least 3 characters long"
        if name.isspace():
            return "-Name cannot be all spaces"
        for mode in self.pastRuns:
            for run in self.pastRuns[mode]:
                if run.name == name:
                    return "-Name already exists"
        return True
    def drawStartMenu(self, screen: pygame.Surface, clock:pygame.time.Clock):
        mousebuttons,key = 0,None

        background = pygame.image.load(r'Assets\backgrounds\Background (4).png').convert_alpha()
        background = pygame.transform.smoothscale_by(background,2);background.set_alpha(100)
        extraSurf = pygame.Surface((1920,1080))
        extraSurf.fill((60,60,60))
        extraSurf.blit(background,(0,0))

        while True:
            # screen.fill((60,60,60))
            # if self.gameMode == 'start':
            #     screen.fill((60,60,60))
            # else:
            screen.blit(extraSurf,(0,0))

            match self.gameMode:
                case 'start':
                    n = self.menus['start'].draw(screen,mousebuttons)
                    if n != None:
                        self.gameMode = n.lower()
                case 'create':
                    if self.menus['create'].draw(screen,mousebuttons,key):
                        break
                case 'play':
                    pass
                case 'settings':
                    pass
                case 'credit':
                    pass
            
            for animation in animationList: animation.update(screen)# update the animations

            pygame.display.flip()
    
            mousebuttons,key = 0,None

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousebuttons = event.button
                    if mousebuttons == 1:
                        print("Mouse button pressed",pygame.mouse.get_pos())
                    
                elif event.type == pygame.KEYDOWN:
                    key = get_key_name(event.key,get_shift_state())
                    
                    if event.key == pygame.K_j:
                        print("Pressed the J key")

                    
                
            clock.tick(60)




        