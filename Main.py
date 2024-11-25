import pygame
from random import randint
import time
from Defs import *
from Classes.BigClasses.Stock import Stock
from Classes.BigClasses.UIControls import UIControls
from Classes.imports.Gametime import GameTime
from Classes.BigClasses.Player import Player
from Classes.BigClasses.StockGraphManager import StockGraphManager
from Classes.Menus.Portfolio import Portfolio
# from Classes.OptionMenu import Optiontrade
from collections import deque
from Classes.smallClasses.IndexFunds import TotalMarket,IndexFund
import timeit
from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.Transactions import Transactions
from Classes.Menus.NewstockBook import Stockbook2
from Classes.Menus.NewOptionMenu import Optiontrade
from Classes.Menus.BankMenu import BankMenu
from Classes.Menus.GameModeMenu import GameModeMenu,BlitzRun
from Classes.Menus.startMenus.StartMain import StartMain

GAMESPEED = 250
FASTFORWARDSPEED = 100
pygame.init()
pygame.mixer.init()


monitor_width, monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
window_width, window_height = (monitor_width, monitor_height)

# Create the Pygame window with the appropriate size and position and the NOFRAME flag
screen = pygame.display.set_mode((1920, 1080),pygame.NOFRAME|pygame.HWSURFACE|pygame.SRCALPHA)
pygame.display.set_caption("Trading Aces")
pygame.display.set_mode((0, 0), pygame.WINDOWMAXIMIZED) 
# pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 

clock = pygame.time.Clock()
fonts = lambda font_size: pygame.font.SysFont('Cosmic Sans',font_size)
# stocknames = ['DRON','FACE','FARM','HOLO','SUNR','BOTS','GENX','NEUR','STAR']
startmenu = StartMain()
startmenu.drawStartMenu(screen,clock)
stocknames = STOCKNAMES
stockVolatilities = [1045,985,890,865,795,825,1060,780,715]# 700=Low, 1075=High

# stocknames = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
stockcolors = [(0, 102, 204),(255, 0, 0),(0, 128, 0),(255, 165, 0),(255, 215, 0),(147,112,219),(46, 139, 87),(255, 69, 0),(0, 191, 255),(128, 0, 128),(12, 89, 27)]# -2 is for cash

# CREATING OBJECTS NEEDED FOR FILE DATA
transact = Transactions()
gametime = GameTime("01/01/2030 00:00:00")
setGameTime(gametime)
player = Player(stocknames,stockcolors[-1],transact,gametime)
# stockdict = {name:Stock(name,(20,400),10,stockcolors[i],Player,stocknames) for i,name in enumerate(stocknames)}#name, startingvalue_range, volatility, Playerclass, stocknames,time
stockdict = {name:Stock(name,stockcolors[i],gametime,stockVolatilities[i]) for i,name in enumerate(stocknames)}#name, startingvalue_range, volatility, Playerclass, stocknames,time
stocklist = [stockdict[name] for name in stocknames]
indexfundColors = [(217, 83, 149),(64, 192, 128),(138, 101, 235)]
indexFunds = [IndexFund(gametime,name,stockcolors[i],stocklist[i*3:i*3+3]) for i,name in enumerate(["TDIF","IEIF", "FHMF"])]# Tech, industrial, health
tmarket = TotalMarket(gametime,stocklist)
indexFunds.append(tmarket)
indexFundDict = {fund.name: fund for fund in indexFunds}


# indexFunds = [IndexFund(gametime,name,stockcolors[i],stocklist[i*3:i*3+3]) for i,name in enumerate(['Velocity Ventures','Adaptive Allocation','Reliable Returns'])]# high,med,low risk

# GETTING DATA FROM FILE

musicdata = Getfromfile(stockdict,indexFundDict,player,gametime)# muiscdata = [time, volume, songindex]
menuDict = {}

# CREATING OBJECTS
stockgraphmanager = StockGraphManager(stocklist,gametime)

uiControls = UIControls(stocklist,GAMESPEED,gametime,tmarket,player)
orderScreen = OrderScreen(uiControls)
# stockbook = Stockbook(stocklist,gametime,orderScreen)
stockbook = Stockbook2(stocklist,gametime,orderScreen)
portfolio = Portfolio(stocklist,player,gametime,tmarket,menuDict)
optiontrade = Optiontrade(stocklist,gametime,player)
bank = BankMenu(stocklist,gametime,player,transact,tmarket,indexFunds)
blitzRuns = [BlitzRun(f'Blitz Run {i}',[randint(0,15000),randint(0,15000),randint(0,15000),randint(0,5000),randint(0,5000)],"1M",'01/02/2030 09:30:00 AM') for i in range(5)]

blitzRuns.append(BlitzRun(f'Blitz Run Timed',[randint(0,15000),randint(0,15000),randint(0,15000),randint(0,15000),randint(0,15000)],"3Y",'01/02/2030 09:30:00 AM'))

pastRuns = {'Blitz':blitzRuns,'Career':[],'Goal':[]}

gameModeMenu = GameModeMenu(stocklist,player,pastRuns,blitzRuns[0])

menuDict.update({'Portfolio':portfolio,'Stockbook':stockbook,'Options':optiontrade,'Bank':bank,'GameModeMenu':gameModeMenu})
menuList = list(menuDict.values())
player.menuList = menuDict
# VARS FROM SETTINGS
autofastforward = True


background = pygame.image.load(r'Assets\backgrounds\Background (9).png').convert_alpha()
background = pygame.transform.smoothscale_by(background,2);background.set_alpha(100)




pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set custom event when music ends
 
musicnames = list(musicThemes)
pygame.mixer.music.load(musicThemes[musicnames[musicdata[2]]] if musicdata[2] < len(musicnames) else musicThemes[musicnames[0]])
pygame.mixer.music.play()
pygame.mixer.music.set_pos(musicdata[0])
pygame.mixer.music.set_volume(musicdata[1])
pygame.mixer.music.set_volume(0)

# LAST DECLARATIONS
lastfps = deque(maxlen=300)
mousebuttons = 0
# print(stocklist[0].graphs)

timer = timeit.default_timer()
if not all([all([len(graph) == POINTSPERGRAPH for graph in stock.graphs.values()]) for stock in stocklist]):
    for stock in stocklist:
        stock.fill_graphs()
    print('time to fill graphs',timeit.default_timer()-timer)

for indexfund in indexFunds:
    indexfund.fill_graphs()


screen.fill((30,30,30))
screen.blit(background,(0,0))


   
menuBackRefresh,screenBackRefresh = getScreenRefreshBackGrounds(screen.copy())

if __name__ == "__main__":
    while True:
        mousex,mousey = pygame.mouse.get_pos()
        if any([menu.menudrawn for menu in menuDict.values()]):
            screen.blit(menuBackRefresh,(0,0))
            # gfxdraw.textured_polygon(screen,[(0,0),(1920,0),(1920,1080),(0,1080)],menuBackBytes,0,0)
            # doBuffer(screen,menuBackBytes)
        else:
            # doBuffer(screen,screenBytes)
            screen.blit(screenBackRefresh,(0,0))
        
        
        uiControls.draw_ui(screen,stockgraphmanager,stocklist,player,gametime,mousebuttons,menuList,tmarket)#draws the ui controls to the screen, and senses for clicks
        
        if gametime.advanceTime(uiControls.gameplay_speed,autofastforward,FASTFORWARDSPEED):# if there is a new trading day

            player.newDay(gametime,stocklist,menuList)

        if gametime.isOpen()[0]:# if the market is open
            if uiControls.gameplay_speed > 0:# if the game is not paused
                
                for stock in stocklist:
                    step = stock.update_price(uiControls.gameplay_speed,Player)
                    if stock.priceEffects.update(gametime,screen,player):
                        uiControls.newsobj.changeStock(stock)

                # player.update_price(uiControls.gameplay_speed,Player)
                
                player.gameTick(uiControls.gameplay_speed,gametime,step)
                
                for indexfund in indexFunds:
                    indexfund.updategraphs(uiControls.gameplay_speed,step)


                # for stock in stocklist:            
        
        for i,menu in enumerate(menuList):
            menu.draw_icon(screen,mousebuttons,stocklist,player,menuList,(30,165+(i*175)),uiControls,gametime)

        screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(1900,0),(1900,30),(1900,60)]))
        errors.update(screen)# draws the error messages

        
        for animation in animationList:
            animation.update(screen)
        
        # uiControls.drawBigMessage(screen,mousebuttons,player)
        
        uiControls.bar.changeMaxValue(GAMESPEED)
        
        mousebuttons = 0
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if pygame.USEREVENT == pygame.mixer.music.get_endevent():
                    # Code to start a new song
                    musicdata[2] = musicdata[2]+1 if musicdata[2]+1 < len(musicThemes) else 0# increment the song index
                    musicdata[0] = 0# reset the song time
                    print('song ended, now playing',musicnames[musicdata[2]])
                    pygame.mixer.music.load(musicThemes[list(musicThemes.keys())[musicdata[2]]] if musicdata[2] < len(musicThemes) else musicThemes[list(musicThemes.keys())[0]])
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(musicdata[1])

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                musicdata = [pygame.mixer.music.get_pos()/1000+musicdata[0],pygame.mixer.music.get_volume(),musicdata[2]]
                
                stockdata = [stock.savingInputs() for stock in player.stocks]
                optiondata = [option.savingInputs() for option in player.options]# options storage is [stockname,strikeprice,expirationdate,optiontype,quantity]
                loanData = [loan.savingInputs() for loan in player.loans]
                indexFundData = [indexfund.savingInputs() for indexfund in player.indexFunds]
                
                data = [str(gametime),stockdata,optiondata,loanData,indexFundData,float(player.cash),musicdata]
                data.append(player.extraSavingData())
                # data.extend([stockobj.graphrange for stockobj in stocklist])
                print(data)
                Writetofile(stocklist,player,data)
                transact.storeTransactions()
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and mousebuttons == 0:
                # print(event.button)
                mousebuttons = event.button
                if mousebuttons == 1:
                    print(mousex,mousey)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                # Get timestamp for unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Create screenshots directory if it doesn't exist
                screenshot_dir = "Assets/Screenshots"
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                
                # Generate filepath
                filepath = f"{screenshot_dir}/screenshot_{timestamp}.png"
                
                # Take screenshot and save
                screenshot = screen.copy()  # screen is your pygame display surface
                pygame.image.save(screenshot, filepath)
  
        pygame.display.update()

        clock.tick(180)


# {"1H":3600,"1D":23_400,"1W":117_000,"1M":491_400,"1Y":5_896_800,"5Y":29_484_000}