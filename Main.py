import pygame
from random import randint
import time
from Defs import *
# from Classes.Stockprice import Stock
from Classes.Stock import Stock
from Classes.UI_controls import UI_Controls
from Classes.Gametime import GameTime
from Classes.Playerportfolio import Player
from Classes.StockGraphManager import StockGraphManager
from Classes.Stockbook import Stockbook
from Classes.portfolio import Portfolio
from Classes.OptionMenu import Optiontrade
from collections import deque
import timeit
GAMESPEED = 25
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
stocknames = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
stockcolors = [(0, 102, 204),(255, 0, 0),(0, 128, 0),(255, 165, 0),(255, 215, 0),(218, 112, 214),(46, 139, 87),(255, 69, 0),(0, 191, 255),(128, 0, 128),(12, 89, 27)]# -2 is for cash

# CREATING OBJECTS
stockgraphmanager = StockGraphManager(stocknames)
stockbook = Stockbook(stocknames)
player = Player(stocknames,stockcolors[-1])
stockdict = {name:Stock(name,(20,400),10,Player,stocknames,stockcolors[i]) for i,name in enumerate(stocknames)}#name, startingvalue_range, volatility, Playerclass, stocknames,time
stocklist = [stockdict[name] for name in stocknames]
portfolio = Portfolio()
optiontrade = Optiontrade(stocklist)
ui_controls = UI_Controls(stocklist,GAMESPEED)


# VARS FROM SETTINGS
autofastforward = True


background = pygame.image.load(r'Assets\backgrounds\Background (9).png').convert_alpha()
background = pygame.transform.smoothscale_by(background,2);background.set_alpha(100)

gametime = GameTime(0,5,15,10,12,'Monday')
menulist = [stockbook,portfolio,optiontrade]
musicdata = Getfromfile(stockdict,player)# muiscdata = [time, volume, songindex]

pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set custom event when music ends

musicnames = list(musicThemes)
pygame.mixer.music.load(musicThemes[musicnames[musicdata[2]]] if musicdata[2] < len(musicnames) else musicThemes[musicnames[0]])
pygame.mixer.music.play()
pygame.mixer.music.set_pos(musicdata[0])
pygame.mixer.music.set_volume(musicdata[1])

# LAST DECLARATIONS
lastfps = deque(maxlen=300)
mousebuttons = 0
for stock in stocklist:
    stock.fill_graphs()
if __name__ == "__main__":
    while True:
        mousex,mousey = pygame.mouse.get_pos()
        screen.fill((50,50,50))
        screen.blit(background,(0,0))
        # screen.blit(polybackground,(0,0))# the background is 1152x896, tile it to fill the screen
        
        # print(mousex,mousey)
        ui_controls.draw_ui(screen,stockgraphmanager,stocklist,player,gametime,mousebuttons,menulist)#draws the ui controls to the screen, and senses for clicks
        
        if gametime.fastforward:
            if (opened:=not gametime.isOpen()[0]):
                ui_controls.bar.set_currentvalue(250)
            gametime.fastforward = opened

        for i in range(ui_controls.gameplay_speed):
            if gametime.isOpen()[0] and ui_controls.gameplay_speed > GAMESPEED:
                ui_controls.bar.set_currentvalue(0)
                ui_controls.bar.changemaxvalue(GAMESPEED)
                break
            gametime.increase_time(1,autofastforward)
            if gametime.isOpen()[0]:
                for stock in stocklist:
                    stock.update_price(player)
                player.update_price(player)
        # player.draw(screen,player,(1920,0),(1600,400),stocklist,mousebuttons)


        # optiontrade.draw_icon(screen,mousebuttons,stocklist,player,menulist,(30,515),ui_controls)
        
        for i,menu in enumerate(menulist):
            menu.draw_icon(screen,mousebuttons,stocklist,player,menulist,(30,165+(i*175)),ui_controls,gametime)


        # stockbook.draw_icon(screen,mousebuttons,stocklist,player,menulist)
        # portfolio.draw_icon(screen,mousebuttons,stocklist,player,menulist)
        # optiontrade.draw_icon(screen,mousebuttons,stocklist,player,menulist)
 
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
                
                stockdata = [[stock[0].name,int(stock[1]),stock[2]] for stock in player.stocks]
                optiondata = [[option.stockobj.name,option.strike_price,option.expiration_date,option.option_type,option.ogvalue] for option in player.options]# options storage is [stockname,strikeprice,expirationdate,optiontype,quantity]
                for option in optiondata:
                    print(type(option))

                data = [str(gametime),stockdata,optiondata,player.graphrange,int(player.cash),musicdata]
                data.extend([stockobj.graphrange for stockobj in stocklist])
                print(data)
                Writetofile(stocklist,player,data)
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and mousebuttons == 0:
                # print(event.button)
                mousebuttons = event.button
                if mousebuttons == 1:
                    print(mousex,mousey)
                # if event.button == 4:
                #     print('Scroll wheel scrolled up')
                # elif event.button == 5:
                #     print('Scroll wheel scrolled down')
                # if mousebuttons == 1:
                    # print(stock1.pricepoints)
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     mousebuttons = 0
            #     print('mouse up')

        
        pygame.display.update()

        clock.tick(60)


