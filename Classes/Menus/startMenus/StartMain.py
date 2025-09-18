import sys
import os
from Classes.Menus.startMenus.CreateMenu import *
from Classes.Menus.startMenus.StartMenu import StartMenu
from Classes.Menus.startMenus.PlayMenu import PlayMenu
import threading
import time


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
    def __init__(self,runManager) -> None:

        self.gameMode = 'play'# play, create, settings , credit, or start
        self.menus : str[CreateMenu] = {'create':CreateMenu(runManager),'play':PlayMenu(runManager),'settings':None,'credit':None,'start':StartMenu()}
        self.runManager = runManager
        
        # Game initialization state
        self.game_ready = False
        self.initialized_game_data = None
        self.initialization_thread = None

        # --------------------------------------------- Temporary ---------------------------------------------
        # blitzRuns = [BlitzRun(f'Blitz Run {i}',[randint(0,15000),randint(0,15000),randint(0,15000),randint(0,5000),randint(0,5000)],"1M",'01/02/2030 09:30:00 AM') for i in range(5)]
        # blitzRuns.append(BlitzRun(f'Blitz Run Timed',[randint(0,15000),randint(0,15000),randint(0,15000),randint(0,15000),randint(0,15000)],"3Y",'01/02/2030 09:30:00 AM'))
        
        
    

                    
            #     if filename.endswith(".json"):
            #         with open(os.path.join("Saves",mode,filename),"r") as f:
            #             data = json.load(f)
            #             if mode == 'Career':
            #                 self.pastRuns[mode].append(CareerRun(data['name'],data['networth'],data['time'],data['date']))
            #             elif mode == 'Blitz':
            #                 self.pastRuns[mode].append(BlitzRun(data['name'],data['networth'],data['time'],data['date']))
            #             elif mode == 'Goal':
            #                 self.pastRuns[mode].append(GoalRun(data['name'],data['networth'],data['time'],data['date']))
    # def validName(self,name:str):
    #     """returns True if the name is valid"""
    #     if len(name) < 3:
    #         return "-Name must be at least 3 characters long"
    #     if name.isspace():
    #         return "-Name cannot be all spaces"
    #     for mode in self.pastRuns:
    #         for run in self.pastRuns[mode]:
    #             if run.name == name:
    #                 return "-Name already exists"
    #     return True
    def reset(self):
        self.gameMode = 'start'
        self.menus['create'].reset()
        self.menus['play'].reset()
        self.game_ready = False
        self.initialized_game_data = None
        if self.initialization_thread and self.initialization_thread.is_alive():
            # Note: We can't forcefully stop threads in Python, but we can mark them as obsolete
            pass

    def start_game_initialization(self, currentRun):
        """Start game initialization in a separate thread"""
        def initialize_game():
            try:
                # Import here to avoid circular imports
                from GameInitializer import initialize_game_with_progress
                
                def progress_callback(progress, message):
                    if self.menus['create'].is_creating_game:
                        self.menus['create'].loading_animation.set_progress(progress, message)
                
                # Initialize the game with progress callbacks
                self.initialized_game_data = initialize_game_with_progress(currentRun, self.runManager.pastRuns, progress_callback)
                self.game_ready = True
                
                # Small delay to show completion
                time.sleep(0.5)
                self.menus['create'].loading_animation.stop()
                self.menus['create'].is_creating_game = False
                
            except Exception as e:
                print(f"Error initializing game: {e}")
                self.menus['create'].loading_animation.stop()
                self.menus['create'].is_creating_game = False
        
        self.game_ready = False
        self.initialized_game_data = None
        self.initialization_thread = threading.Thread(target=initialize_game)
        self.initialization_thread.daemon = True
        self.initialization_thread.start()

    def getSurfs(self):
        from Defs import get_asset_path, backgroundColor
        background = pygame.image.load(get_asset_path('back1.jpeg')).convert_alpha()
        background = pygame.transform.smoothscale(background,(1920,1080))
        background.set_alpha(100)
        extraSurf = pygame.Surface((1920,1080))
        extraSurf.fill((60,60,60))
        extraSurf.blit(background,(0,0))
        tempSurf = pygame.Surface((1920,1080),pygame.SRCALPHA)
        tempSurf.fill((*backgroundColor,200))
        createSurf = pygame.Surface((1920,1080))
        createSurf.blit(extraSurf,(0,0))
        drawBoxedImage(createSurf,(150,10),tempSurf,(1620,1060),25,5)# main box
        return createSurf,extraSurf
    
    def drawStartMenu(self, screen: pygame.Surface, clock:pygame.time.Clock):
        # Import resolution scaling functions
        from Defs import resolution_manager, get_game_surface, enable_mouse_scaling
        
        # Enable mouse scaling for start menus
        enable_mouse_scaling()
        
        # Get the game surface to draw on (scaled internally)
        game_surface = get_game_surface()
        
        key = None

        createSurf,backSurf = self.getSurfs()
        

        lastfps = deque(maxlen=300)
        while True:
            # Clear main screen and draw to game surface
            screen.fill((0, 0, 0))  # Black background
            
            if self.gameMode in ['create','play']:
                game_surface.blit(createSurf,(0,0))
            else:
                game_surface.blit(backSurf,(0,0))
            
            match self.gameMode:
                case 'start':
                    n = self.menus['start'].draw(game_surface)
                    if n != None:
                        self.gameMode = n.lower()
                case 'create':
                    # Check if game creation was initiated and start initialization
                    if (self.menus['create'].is_creating_game and 
                        (not self.initialization_thread or not self.initialization_thread.is_alive())):
                        self.start_game_initialization(self.menus['create'].currentRun)
                    
                    # Check if game is ready to return
                    if self.game_ready and self.initialized_game_data:
                        self.runManager.addRun(self.menus['create'].currentRun)
                        return self.menus['create'].currentRun
                    
                    # Draw the create menu (will show loading animation if creating)
                    self.menus['create'].draw(game_surface,events)
                case 'play':
                    if run:=self.menus['play'].draw(game_surface):
                        return run
                case 'settings':
                    pass
                case 'credit':
                    pass
            if self.gameMode != 'start':
                if drawClickableBoxWH(game_surface,(170,905),(540,130),"Return Home", 75, (0,0,0),(0,210,0)):
                    self.gameMode = 'start'
                

            key = None
            events = []  # Collect all events for TextInput
            game_surface.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(1900,0),(1900,30),(1900,60)]))
            
            # Render scaled game to main screen
            resolution_manager.render_to_screen(screen)
            
            mouseButton.update()
            for event in pygame.event.get():
                events.append(event)  # Store all events
                
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    mouseButton.addEvent(event.button)
                    if mouseButton.getButtonOveride('left') == 1:
                        print("Mouse button pressed",pygame.mouse.get_pos())
                    
                elif event.type == pygame.KEYDOWN:
                    key = get_key_name(event.key,get_shift_state())
                    
                    if event.key == pygame.K_j:
                        print("Pressed the J key")

                    
            pygame.display.flip()
            clock.tick(60)



        