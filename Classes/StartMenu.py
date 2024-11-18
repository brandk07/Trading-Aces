import pygame
import pygame.camera
from Defs import *
from pygame import gfxdraw
from Classes.imports.SelectionElements import SelectionBar

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


class StartMenu:
    def __init__(self) -> None:

        self.gameMode = 'create'# play, create, settings ,or credit
        self.menus : str[CreateMenu] = {'create':CreateMenu(self),'play':None,'settings':None,'credit':None}
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
            screen.fill((60,60,60))
            screen.blit(extraSurf,(0,0))

            match self.gameMode:
                case 'create':
                    if not self.menus['create'].draw(screen,mousebuttons,key):
                        break
                case 'play':
                    pass
                case 'settings':
                    pass
                case 'credit':
                    pass

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

                    
                
            clock.tick(180)


class CreateMenu:
    def __init__(self,startMenu) -> None:
        self.selectionBar : SelectionBar = SelectionBar()
        self.mode = 'blitz'# career, goal, or blitz
        self.gameModes = ['blitz','career','goal']
        self.modeColors = {self.gameModes[i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        self.currentName = 'Game Name'
        self.startMenu : StartMenu = startMenu
    
    def drawModeInfo(self,screen):
        """Draws the info about the mode (Left side of the screen)"""
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1360,65,395,990),5,border_radius=10)# box for the mode info on right

        descriptions = {
            "blitz": "Make risky trades in this intense trading sprint.",
            "career": "Make strategic investments and grow your wealth over years.",
            "goal": "Reach specific financial targets within set timeframes."
        }
        extraDescriptions = {
            "blitz": ["• 1M to 5Y time frame","• All stocks are twice as volatile","• Maximize ending net worth"],
            "career": ["• Unlimited time","• Unlockable trading methods","• Grow your net worth over time"],
            "goal": ["• Unlimited Time","• Reach specific financial targets","• Achieve goals as fast as possible"]
        }
        for i in range(3):
            color = (0,0,0) if self.gameModes[i] != self.mode else self.modeColors[self.mode]
            drawCenterTxt(screen,self.gameModes[i].capitalize(),65,color,(1370,75+(i*330)),centerX=False,centerY=False)

            color = (140,140,140) if self.gameModes[i] != self.mode else (195,195,195)
            for j,txt in enumerate(separate_strings(descriptions[self.gameModes[i]],2)):# draws the quick description of the mode
                drawCenterTxt(screen,txt,40,color,(1380,140+(i*330)+(j*40)),centerX=False,centerY=False)

            color = (0,0,0) if self.gameModes[i] != self.mode else (59, 171, 22)
            for j,txt in enumerate(extraDescriptions[self.gameModes[i]]):# draws the extra info about the mode
                drawCenterTxt(screen,txt,35,color,(1400,220+(i*330)+(j*35)),centerX=False,centerY=False)

        drawCenterTxt(screen,"Mode Info",65,(0,0,0),(1360+395/2,15),centerX=True,centerY=False)
        
    def drawModeNameSelection(self,screen,mousebuttons,key):


        drawCenterTxt(screen,"Name",65,(0,0,0),(730,65),centerX=False,centerY=False)
        self.currentName = text_input(screen,(715,115),(640,75),self.currentName,key,55)

        if type(n:=self.startMenu.validName(self.currentName)) != bool:
            drawCenterTxt(screen,n,40,(210,0,0),(730,200),centerX=False,centerY=False)

        
        drawCenterTxt(screen,"Mode",65,(0,0,0),(730,270),centerX=False,centerY=False)

        self.selectionBar.draw(screen,[g.capitalize() for g in self.gameModes],(710,320),(640,125),mousebuttons,list(self.modeColors.values()),50)

        if self.selectionBar.getSelected() != None:
            self.mode = (self.selectionBar.getSelected()).lower()

    def draw(self,screen,mousebuttons,key):
       
        pygame.draw.rect(screen,(60,60,60),pygame.Rect(150,10,1620,1060),border_radius=25)# main box
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(150,10,1620,1060),5,border_radius=25)# main box border

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(170,65,540,380),5,border_radius=10)# box for the icon selection

        self.drawModeInfo(screen)# draws the mode info on the right

        self.drawModeNameSelection(screen,mousebuttons,key)# draws the name and mode selection

        
        drawCenterTxt(screen,self.mode.capitalize(),65,self.modeColors[self.mode],(725,460),centerX=False,centerY=False)# title


        
        
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(715,450,640,280),5,border_radius=10)# rect under the game mode selector (says more info about the mode)

        return not drawClickableBoxWH(screen,(170,450),(540,130),"Create Game", 75, (0,0,0),(200,200,200),mousebuttons)# returns False if the create game button is pressed



        