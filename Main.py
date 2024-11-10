import pygame
from random import randint
import time
from Defs import *
from Classes.Stock import Stock
from Classes.UIControls import UIControls
from Classes.Gametime import GameTime
from Classes.Player import Player
from Classes.StockGraphManager import StockGraphManager
from Classes.Portfolio import Portfolio
# from Classes.OptionMenu import Optiontrade
from collections import deque
from Classes.smallClasses.IndexFunds import TotalMarket,IndexFund
import timeit
from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.Transactions import Transactions
from Classes.NewstockBook import Stockbook2
from Classes.NewOptionMenu import Optiontrade
from Classes.BankMenu import BankMenu

GAMESPEED = 250
FASTFORWARDSPEED = 1000
pygame.init()
pygame.mixer.init()


monitor_width, monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
window_width, window_height = (monitor_width, monitor_height)

# Create the Pygame window with the appropriate size and position and the NOFRAME flag
screen = pygame.display.set_mode((window_width, window_height-100),pygame.NOFRAME|pygame.HWSURFACE)
pygame.display.set_caption("Trading Aces")
pygame.display.set_mode((0, 0), pygame.WINDOWMAXIMIZED) 
# pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 

clock = pygame.time.Clock()
fonts = lambda font_size: pygame.font.SysFont('Cosmic Sans',font_size)
# stocknames = ['DRON','FACE','FARM','HOLO','SUNR','BOTS','GENX','NEUR','STAR']
stocknames = STOCKNAMES
stockVolatilities = [1045,985,890,865,795,825,1060,780,715]# 700=Low, 1075=High
for i in range(len(stockVolatilities)):
    stockVolatilities[i] = stockVolatilities[i]*2
# stocknames = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
stockcolors = [(0, 102, 204),(255, 0, 0),(0, 128, 0),(255, 165, 0),(255, 215, 0),(218, 112, 214),(46, 139, 87),(255, 69, 0),(0, 191, 255),(128, 0, 128),(12, 89, 27)]# -2 is for cash

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
menuList = []

# CREATING OBJECTS
stockgraphmanager = StockGraphManager(stocklist,gametime)

uiControls = UIControls(stocklist,GAMESPEED,gametime,tmarket,player)
orderScreen = OrderScreen(uiControls)
# stockbook = Stockbook(stocklist,gametime,orderScreen)
stockbook = Stockbook2(stocklist,gametime,orderScreen)
portfolio = Portfolio(stocklist,player,gametime,tmarket,menuList)
optiontrade = Optiontrade(stocklist,gametime,player)
bank = BankMenu(stocklist,gametime,player,transact,tmarket,indexFunds)

menuList.extend([stockbook,portfolio,optiontrade,bank])
player.menuList = menuList
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

extraSurf = pygame.Surface((1920,1080))
extraSurf.fill((30,30,30))
extraSurf.blit(background,(0,0))
screenBytes = bytes(extraSurf.get_buffer())
# s = screen.copy()# makes way better performance
menuBackBytes = getDrawnMenuBackground(screen.copy())

if __name__ == "__main__":
    while True:
        mousex,mousey = pygame.mouse.get_pos()
        if any([menu.menudrawn for menu in menuList]):
            screen.blit(menuBackBytes,(0,0))
            # gfxdraw.textured_polygon(screen,[(0,0),(1920,0),(1920,1080),(0,1080)],menuBackBytes,0,0)
            # doBuffer(screen,menuBackBytes)
        else:
            # doBuffer(screen,screenBytes)
            screen.blit(extraSurf,(0,0))
        
        timer = timeit.default_timer()
        uiControls.draw_ui(screen,stockgraphmanager,stocklist,player,gametime,mousebuttons,menuList,tmarket)#draws the ui controls to the screen, and senses for clicks
        # print('Ui controls time',timeit.default_timer()-timer)
        timer = timeit.default_timer()
        if gametime.advanceTime(uiControls.gameplay_speed,autofastforward,FASTFORWARDSPEED):# if there is a new trading day

            player.newDay(gametime,stocklist)
        # print('advance time',timeit.default_timer()-timer)
        timer = timeit.default_timer()
        if gametime.isOpen()[0]:# if the market is open
            if uiControls.gameplay_speed > 0:# if the game is not paused
                timer = timeit.default_timer()
                for stock in stocklist:
                    stock.update_price(uiControls.gameplay_speed,Player)
                    stock.priceEffects.update(gametime,screen,player)
                print('stock for loop',timeit.default_timer()-timer)
                # player.update_price(uiControls.gameplay_speed,Player)
                timer = timeit.default_timer()
                player.gameTick(uiControls.gameplay_speed,gametime)
                print('player game tick',timeit.default_timer()-timer)
                timer = timeit.default_timer()
                for indexfund in indexFunds:
                    indexfund.updategraphs(uiControls.gameplay_speed)
                print('indexfund update',timeit.default_timer()-timer)

                # for stock in stocklist:
                    
        # print('Is open',timeit.default_timer()-timer)
        timer = timeit.default_timer()
        for i,menu in enumerate(menuList):
            menu.draw_icon(screen,mousebuttons,stocklist,player,menuList,(30,165+(i*175)),uiControls,gametime)
        # print('menu draw icon time',timeit.default_timer()-timer)
        timer = timeit.default_timer()
        screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(1900,0),(1900,30),(1900,60)]))
        errors.update(screen)# draws the error messages
        # print('errors and time time',timeit.default_timer()-timer)
        timer = timeit.default_timer()
        for animation in animationList:
            animation.update(screen)
        # print('animation time',timeit.default_timer()-timer)
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
  
        pygame.display.update()

        clock.tick(180)


# {"1H":3600,"1D":23_400,"1W":117_000,"1M":491_400,"1Y":5_896_800,"5Y":29_484_000}