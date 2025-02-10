import pygame
from random import randint
import time
from Defs import *
from Classes.BigClasses.Stock import Stock
# from Classes.BigClasses.UIControls import UIControls
from Classes.Menus.HomeScreen import HomeScreen
from Classes.imports.Gametime import GameTime
from Classes.BigClasses.Player import Player
from Classes.Menus.StockScreen import StockScreen
from Classes.Menus.Portfolio import Portfolio
# from Classes.OptionMenu import Optiontrade
from collections import deque
from Classes.imports.IndexFunds import TotalMarket,IndexFund
import timeit
from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.Transactions import Transactions
from Classes.Menus.StockBook import Stockbook
from Classes.Menus.OptionScreens.OptionMenu import Optiontrade
from Classes.Menus.BankMenu import BankMenu
from Classes.Menus.GameModeMenu import GameModeMenu,GameRun,RunManager
from Classes.Menus.startMenus.StartMain import StartMain
from Classes.Menus.Menu import ScreenManager


GAMESPEED = 250
FASTFORWARDSPEED = 1000
CLICK_COOLDOWN = 0.2  # 100ms cooldown
last_click_time = 0

pygame.init()

monitor_width, monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
window_width, window_height = (monitor_width, monitor_height)

# Create the Pygame window with the appropriate size and position and the NOFRAME flag
screen = pygame.display.set_mode((1920, 1080),pygame.NOFRAME|pygame.HWSURFACE|pygame.SRCALPHA)
pygame.display.set_caption("Trading Aces")
pygame.display.set_mode((0, 0), pygame.WINDOWMAXIMIZED) 
# pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 

clock = pygame.time.Clock()
fonts = lambda font_size: pygame.font.SysFont('Cosmic Sans',font_size)


# ------------------------------------------ Start of the Start Menu ------------------------------------------
runManager = RunManager()
startmenu = StartMain(runManager)

if __name__ == "__main__":
    while True:
        runManager.reset()
        startmenu.reset()# resets the start menu
        currentRun : GameRun = startmenu.drawStartMenu(screen,clock)
        
        pastRuns = runManager.pastRuns# remember that this is using the real past runs so if it is modified then it will mess stuff up - also deep copy issue b/c there are lists inside
        
        # currentRun = pastRuns["Career"][0]

        gametime = GameTime(DEFAULTSTARTDATE.strftime(DFORMAT),GAMESPEED)
        setGameTime(gametime,currentRun.getFileDir())

        stocknames = STOCKNAMES
        
        stockVolatilities = [i*(2 if currentRun.gameMode == 'Blitz' else 1) for i in [8.03, 7.42, 6.13, 5.58, 4.74, 5.13, 7.8, 4.2, 3.8]]# 700=Low, 1075=High

        stockcolors = [(0, 102, 204),(255, 0, 0),(0, 128, 0),(255, 165, 0),(255, 215, 0),(147,112,219),(46, 139, 87),(255, 69, 0),(0, 191, 255),(128, 0, 128),(12, 89, 27)]# -2 is for cash


        transact = Transactions(currentRun.getFileDir())
        player = Player(stocknames,stockcolors[-1],transact,gametime,currentRun)
        stockdict = {name:Stock(name,stockcolors[i],gametime,stockVolatilities[i],currentRun,player) for i,name in enumerate(stocknames)}#name, startingvalue_range, volatility, Playerclass, stocknames,time
        stocklist = [stockdict[name] for name in stocknames]
        indexfundColors = [(217, 83, 149),(64, 192, 128),(138, 101, 235)]
        indexFunds = [IndexFund(gametime,name,stockcolors[i],stocklist[i*3:i*3+3],currentRun,player) for i,name in enumerate(["TDIF","IEIF", "FHMF"])]# Tech, industrial, health
        tmarket = TotalMarket(gametime,stocklist,currentRun,player)
        indexFunds.append(tmarket)
        indexFundDict = {fund.name: fund for fund in indexFunds}

        optiontrade = Optiontrade(stocklist,gametime,player,currentRun)
        Getfromfile(stockdict,indexFundDict,player,gametime,currentRun.getFileDir(),optiontrade)

        stockScreen = StockScreen(stocklist,gametime)
        orderScreen = OrderScreen()
        homeScreen = HomeScreen(stocklist,gametime,tmarket,player)
        stockbook = Stockbook(stocklist,gametime,orderScreen,currentRun)
        portfolio = Portfolio(stocklist,player,gametime,tmarket,currentRun)
        
        bank = BankMenu(stocklist,gametime,player,transact,tmarket,indexFunds,currentRun)

        gameModeMenu = GameModeMenu(stocklist,player,pastRuns,currentRun,gametime)
        menuDict = {'Portfolio':portfolio,'Stockbook':stockbook,'Options':optiontrade,'Bank':bank,'Mode':gameModeMenu}
        screenManager = ScreenManager(menuDict,homeScreen,stockScreen,gametime)# Handles the drawing of both the screens (stock + home) and the menus (menudict)
        player.screenManager = screenManager
        autofastforward = True

        # LAST DECLARATIONS
        lastfps = deque(maxlen=300)     
            

        timer = timeit.default_timer()
        if not all([all([len(graph) == POINTSPERGRAPH for graph in stock.graphs.values()]) for stock in stocklist]):
            for stock in stocklist:
                stock.fill_graphs()
            print('time to fill graphs',timeit.default_timer()-timer)
            saveGame(stocklist,player,currentRun.getFileDir(),gametime,transact,currentRun,optiontrade)


        for indexfund in indexFunds:
            indexfund.fill_graphs()

        
        menuBackRefresh,screenBackRefresh = getScreenRefreshBackGrounds(screen)

        
        # ------------------------------------------ Main Game Loop ------------------------------------------
        while True:
            mousex,mousey = pygame.mouse.get_pos()

            if currentRun.state == 'complete':
                gametime.speedBar.frozen = True; gametime.speedBar.redraw()
            if screenManager.getCurrentScreen(True) in ['Home','Stock']:# if the current screen is a screen, not a menu then draw the background
                screen.blit(screenBackRefresh,(0,0))
            else:
                screen.blit(menuBackRefresh,(0,0))

            if gametime.advanceTime(autofastforward,FASTFORWARDSPEED):# if there is a new trading day

                player.newDay(gametime,stocklist)

            if gametime.isOpen()[0]:# if the market is open
                if gametime.speedBar.getValue() > 0:# if the game is not paused
                    
                    for stock in stocklist:
                        step = stock.update_price(gametime.speedBar.getValue())
                        if stock.priceEffects.update(gametime,screen,player):
                            homeScreen.newsobj.changeStock(stock)

                    
                    player.gameTick(gametime.speedBar.getValue(),gametime,step)
                    
                    for indexfund in indexFunds:
                        indexfund.updategraphs(gametime.speedBar.getValue(),step)
            if gametime.speedBar.frozen and currentRun.state != 'complete':
                gametime.speedBar.frozen = False
                gametime.speedBar.redraw()

            # print(mouseButton.livebuttons,mouseButton.buttons,mouseButton.live)
            player.updateRunAssetSpread()# updates the asset spread for the current run

            screenManager.drawCurrentScreen(screen,stocklist,player,gametime)

            screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(1900,980),(1900,1010),(1900,1040)]))
            errors.update(screen)# draws the error messages

            
            for animation in animationList:
                animation.update(screen)

            if drawClickableBoxWH(screen,(10,970),(165,100),"Main Menu", 50, (180,180,180),(255,255,255)):
                break
            
            mouseButton.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):                
                    saveGame(stocklist,player,currentRun.getFileDir(),gametime,transact,currentRun,optiontrade)
                    pygame.quit()
                    quit()

                # elif event.type == pygame.MOUSEBUTTONDOWN:
                elif event.type == pygame.MOUSEBUTTONUP:
                    current_time = time.time()
                    print(current_time - last_click_time)
                    if last_click_time-current_time < CLICK_COOLDOWN:# if the time between the last click and the current click is less than the cooldown
                      mouseButton.addEvent(event.button)
                      last_click_time = current_time

                    if mouseButton.getButtonOveride('left') == 1:
                        print(mousex,mousey)
                    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    # Get timestamp for unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    screenshot_dir = os.path.join(currentRun.getFileDir(), "Screenshots")
                    if not os.path.exists(screenshot_dir):
                        os.makedirs(screenshot_dir)

                    filepath = f"{screenshot_dir}/screenshot_{timestamp}.png"
                
                    screenshot = screen.copy()  # screen is your pygame display surface
                    pygame.image.save(screenshot, filepath)

            pygame.display.update()

            clock.tick(60)

        # Saves the game when the user goes back to the main menu
        saveGame(stocklist,player,currentRun.getFileDir(),gametime,transact,currentRun,optiontrade)


# {"1H":3600,"1D":23_400,"1W":117_000,"1M":491_400,"1Y":5_896_800,"5Y":29_484_000}