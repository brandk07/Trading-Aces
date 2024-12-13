import pygame.camera
from Classes.Menus.startMenus.CreateMenu import *
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
        
        self.pastRuns : dict[str:list[GameRun]] = {'Career':[],'Blitz':[],'Goal':[]}# the past runs that the player has done
        self.loadPastRuns()

        # --------------------------------------------- Temporary ---------------------------------------------
        # blitzRuns = [BlitzRun(f'Blitz Run {i}',[randint(0,15000),randint(0,15000),randint(0,15000),randint(0,5000),randint(0,5000)],"1M",'01/02/2030 09:30:00 AM') for i in range(5)]
        # blitzRuns.append(BlitzRun(f'Blitz Run Timed',[randint(0,15000),randint(0,15000),randint(0,15000),randint(0,15000),randint(0,15000)],"3Y",'01/02/2030 09:30:00 AM'))
        
        
    def loadPastRuns(self):
        for mode in self.pastRuns:
            for runName in os.listdir(os.path.join("Saves",mode)):
                with open(os.path.join("Saves",mode,runName,"BasicInfo.json"),"r") as f:
                    basicInfo = json.load(f)
                with open(os.path.join("Saves",mode,runName,"ModeSpecificInfo.json"),"r") as f:
                    modeSpecificInfo = json.load(f)
                if mode == 'Career':
                    pass
                elif mode == 'Blitz':
                    print(basicInfo)
                    print(modeSpecificInfo)
                    run = BlitzRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],modeSpecificInfo['duration'],endGameDate=modeSpecificInfo['endGameDate'],startTime=basicInfo['startTime'],endTime=modeSpecificInfo['endTime'])
                elif mode == 'Goal':
                    pass
                self.pastRuns[mode].append(run)

                    
            #     if filename.endswith(".json"):
            #         with open(os.path.join("Saves",mode,filename),"r") as f:
            #             data = json.load(f)
            #             if mode == 'Career':
            #                 self.pastRuns[mode].append(CareerRun(data['name'],data['networth'],data['time'],data['date']))
            #             elif mode == 'Blitz':
            #                 self.pastRuns[mode].append(BlitzRun(data['name'],data['networth'],data['time'],data['date']))
            #             elif mode == 'Goal':
            #                 self.pastRuns[mode].append(GoalRun(data['name'],data['networth'],data['time'],data['date']))


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
    def getSurfs(self):
        background = pygame.image.load(r'Assets\StartBackground.png').convert_alpha()
        background = pygame.transform.smoothscale_by(background,2);background.set_alpha(100)
        extraSurf = pygame.Surface((1920,1080))
        extraSurf.fill((60,60,60))
        extraSurf.blit(background,(0,0))
        tempSurf = pygame.Surface((1920,1080),pygame.SRCALPHA)
        tempSurf.fill((60,60,60,200))
        createSurf = pygame.Surface((1920,1080))
        createSurf.blit(extraSurf,(0,0))
        drawBoxedImage(createSurf,(150,10),tempSurf,(1620,1060),25,5)# main box
        return createSurf,extraSurf
    
    def drawStartMenu(self, screen: pygame.Surface, clock:pygame.time.Clock):
        mousebuttons,key = 0,None

        createSurf,backSurf = self.getSurfs()
        

        lastfps = deque(maxlen=300)
        while True:

            if self.gameMode == 'create':
                screen.blit(createSurf,(0,0))
            else:
                screen.blit(backSurf,(0,0))
            
            match self.gameMode:
                case 'start':
                    n = self.menus['start'].draw(screen,mousebuttons)
                    if n != None:
                        self.gameMode = n.lower()
                case 'create':
                    if self.menus['create'].draw(screen,mousebuttons,key):
                        self.pastRuns[self.menus['create'].mode.capitalize()].append(self.menus['create'].currentRun)# add the run to the past runs
                        return self.menus['create'].currentRun
                case 'play':
                    pass
                case 'settings':
                    pass
                case 'credit':
                    pass
            if self.gameMode != 'start':
                if drawClickableBoxWH(screen,(170,905),(540,130),"Return Home", 75, (0,0,0),(0,210,0),mousebuttons):
                    self.gameMode = 'start'
                

            mousebuttons,key = 0,None
            screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(1900,0),(1900,30),(1900,60)]))
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

                    
            pygame.display.flip()
            clock.tick(180)



        