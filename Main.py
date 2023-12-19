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
from Classes.Portfolio import Portfolio
import timeit

pygame.init()

# Set the aspect ratio of your game
aspect_ratio = 16 / 9

# Get the size of the user's monitor
monitor_width, monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
print(monitor_width, monitor_height)
# Calculate the appropriate size for your window based on the aspect ratio and the monitor size
window_width, window_height = (int(monitor_height * aspect_ratio), monitor_height) if int(monitor_height * aspect_ratio) <= monitor_width else (monitor_width, int(monitor_width / aspect_ratio))

# Calculate the position of the window to center it on the monitor
window_x, window_y = int((monitor_width - window_width) / 2), int((monitor_height - window_height) / 2)
print(window_x, window_y)

# Create the Pygame window with the appropriate size and position and the NOFRAME flag
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
screen.fill((0, 0, 0))
pygame.display.set_caption("Trading Aces")
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()
fonts = lambda font_size: pygame.font.SysFont('Cosmic Sans',font_size)
window_offset = (window_x*-1,window_y)
stocknames = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
stockgraphmanager = StockGraphManager()
stockbook = Stockbook(stocknames)



player = Player(window_offset,stocknames)
#name, startingvalue_range, volatility, Playerclass, window_offset,stocknames,time
stockdict = {name:Stock(name,(20,400),10,Player,window_offset,stocknames) for name in stocknames}

stocklist = [stockdict[name] for name in stocknames]
portfolio = Portfolio()
ui_controls = UI_Controls((window_offset[0]*-1,window_offset[1]),stocklist)
# ui_controls = UI_Controls((window_offset[0]*-1,window_offset[1]),6,[1500,650],[60,380],'vertical')
mousebuttons = 0
polybackground = pygame.image.load('Assets/polybackground2.png')
polybackground = pygame.transform.scale(polybackground,(window_width,window_height))
#gametime is #months,weeks,days,hours,minutes,update interval,am/pm

gametime = GameTime(2023,11,7,9,30,0)
menulist = [stockbook,portfolio]
Getfromfile(stockdict,player)
if __name__ == "__main__":
    while True:
        mousex,mousey = pygame.mouse.get_pos()
        screen.fill((50,50,50))
        # screen.blit(polybackground,(0,0))# the background is 1152x896, tile it to fill the screen
        
        
        # print(mousex,mousey)
        ui_controls.draw_ui(screen,stockgraphmanager,stocklist,player,gametime,mousebuttons)#draws the ui controls to the screen, and senses for clicks

        
        for i in range(ui_controls.gameplay_speed):
            # gametime = Gametime(gametime,,screen,clock.get_fps())
            gametime.increase_time(1)
            for stock in stocklist:
                stock.update_price(player)
            player.update_price(player)
        # player.draw(screen,player,(1920,0),(1600,400),stocklist,mousebuttons)

        # gametime.drawgametime(screen,True)


        stockbook.draw_icon(screen,mousebuttons,stocklist,player,menulist)
        portfolio.draw_icon(screen,mousebuttons,stocklist,player,menulist)
        screen.blit(update_fps(clock),(1570,0))


        mousebuttons = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data = [str(gametime),[[stock[0].name,stock[1],stock[2]] for stock in player.stocks],player.graphrange,player.cash]
                data.extend([stockobj.graphrange for stockobj in stocklist])
                print(data)
                Writetofile(stocklist,player,data)
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                data = [str(gametime),[[stock[0].name,stock[1],stock[2]] for stock in player.stocks],player.graphrange,player.cash]
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


