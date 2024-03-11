import pygame
from random import randint
import time
from Defs import *
from Classes.Stock import Stock
from Classes.UI_controls import UI_Controls
from Classes.Gametime import GameTime
from Classes.Playerportfolio import Player
from Classes.StockGraphManager import StockGraphManager
from Classes.Stockbook import Stockbook
from Classes.portfolio import Portfolio
from Classes.OptionMenu import Optiontrade
from collections import deque
from Classes.smallClasses.TotalMarket import TotalMarket
import timeit
from Classes.imports.Transactions import Transactions
GAMESPEED = 250
FASTFORWARDSPEED = 500
pygame.init()
pygame.mixer.init()


monitor_width, monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
window_width, window_height = (monitor_width, monitor_height)

# Create the Pygame window with the appropriate size and position and the NOFRAME flag
screen = pygame.display.set_mode((window_width, window_height-100),pygame.NOFRAME|pygame.HWSURFACE)
pygame.display.set_caption("Trading Aces")
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()
fonts = lambda font_size: pygame.font.SysFont('Cosmic Sans',font_size)
stocknames = ['DRON','FACE','FARM','HOLO','SUNR','BOTS','GENX','NEUR','STAR']
# stocknames = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
stockcolors = [(0, 102, 204),(255, 0, 0),(0, 128, 0),(255, 165, 0),(255, 215, 0),(218, 112, 214),(46, 139, 87),(255, 69, 0),(0, 191, 255),(128, 0, 128),(12, 89, 27)]# -2 is for cash

# CREATING OBJECTS NEEDED FOR FILE DATA
transact = Transactions()
gametime = GameTime("01/01/2030 00:00:00")
player = Player(stocknames,stockcolors[-1],transact,gametime)
# stockdict = {name:Stock(name,(20,400),10,stockcolors[i],Player,stocknames) for i,name in enumerate(stocknames)}#name, startingvalue_range, volatility, Playerclass, stocknames,time
stockdict = {name:Stock(name,10,stockcolors[i]) for i,name in enumerate(stocknames)}#name, startingvalue_range, volatility, Playerclass, stocknames,time
stocklist = [stockdict[name] for name in stocknames]

# GETTING DATA FROM FILE

musicdata = Getfromfile(stockdict,player,gametime)# muiscdata = [time, volume, songindex]

# CREATING OBJECTS
stockgraphmanager = StockGraphManager(stocklist,gametime)
stockbook = Stockbook(stocklist,gametime)
portfolio = Portfolio(stocklist,player,gametime)
optiontrade = Optiontrade(stocklist,gametime)
tmarket = TotalMarket(gametime)
ui_controls = UI_Controls(stocklist,GAMESPEED,gametime,tmarket,player)

# VARS FROM SETTINGS
autofastforward = True


background = pygame.image.load(r'Assets\backgrounds\Background (9).png').convert_alpha()
background = pygame.transform.smoothscale_by(background,2);background.set_alpha(100)

menulist = [stockbook,portfolio,optiontrade]


pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set custom event when music ends
 
musicnames = list(musicThemes)
pygame.mixer.music.load(musicThemes[musicnames[musicdata[2]]] if musicdata[2] < len(musicnames) else musicThemes[musicnames[0]])
pygame.mixer.music.play()
pygame.mixer.music.set_pos(musicdata[0])
pygame.mixer.music.set_volume(musicdata[1])

# LAST DECLARATIONS
lastfps = deque(maxlen=300)
mousebuttons = 0
# timer = timeit.default_timer()
# for stock in stocklist:
#     stock.fill_graphs()
# print('time to fill graphs',timeit.default_timer()-timer)
tmarket.fill_graphs(stocklist)


screen.fill((50,50,50))
screen.blit(background,(0,0))
s = screen.copy()# makes way better performance

if __name__ == "__main__":
    while True:
        mousex,mousey = pygame.mouse.get_pos()
        screen.blit(s,(0,0))

        ui_controls.draw_ui(screen,stockgraphmanager,stocklist,player,gametime,mousebuttons,menulist,tmarket)#draws the ui controls to the screen, and senses for clicks
        
        gametime.advanceTime(ui_controls.gameplay_speed,autofastforward,FASTFORWARDSPEED)


        if gametime.isOpen()[0]:# if the market is open
            if ui_controls.gameplay_speed > 0:# if the game is not paused
                for stock in stocklist:
                    stock.update_price(ui_controls.gameplay_speed,Player)
                player.update_price(ui_controls.gameplay_speed,Player)
                tmarket.updategraphs(stocklist,ui_controls.gameplay_speed)


        
        for i,menu in enumerate(menulist):
            menu.draw_icon(screen,mousebuttons,stocklist,player,menulist,(30,165+(i*175)),ui_controls,gametime)

 
        screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(1900,0),(1900,30),(1900,60)]))


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

                data = [str(gametime),stockdata,optiondata,player.graphrange,float(player.cash),musicdata]
                data.extend([stockobj.graphrange for stockobj in stocklist])
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

        clock.tick(600)


