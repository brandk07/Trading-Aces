import pygame
from random import randint
import time
from Defs import *
# from Classes.Stockprice import Stock
from Classes.Stock import Stock
from Classes.UI_controls import *
from Classes.Playerportfolio import Player
from Classes.StockGraphManager import StockGraphManager
from Classes.Stockbook import Stockbook
import timeit

pygame.init()

# Set the aspect ratio of your game
aspect_ratio = 16 / 9

# Get the size of the user's monitor
monitor_width, monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
# Calculate the appropriate size for your window based on the aspect ratio and the monitor size
window_width, window_height = (int(monitor_height * aspect_ratio), monitor_height) if int(monitor_height * aspect_ratio) <= monitor_width else (monitor_width, int(monitor_width / aspect_ratio))

# Calculate the position of the window to center it on the monitor
window_x, window_y = int((monitor_width - window_width) / 2), int((monitor_height - window_height) / 2)
print(window_x, window_y)
# Create the Pygame window with the appropriate size and position and the NOFRAME flag
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
screen.fill((0, 0, 0))
pygame.display.set_caption("Investrix")
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()
fonts = lambda font_size: pygame.font.SysFont('Cosmic Sans',font_size)
window_offset = (window_x*-1,window_y)
stocknames = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
stockgraphmanager = StockGraphManager()
stockbook = Stockbook(stocknames)


gametime = [0,0,0,9,30,0,'am']#months,weeks,days,hours,minutes,update interval ,am/pm
player = Player(window_offset,stocknames)
#name, startingvalue_range, volatility, Playerclass, window_offset,stocknames,time
stockdict = {name:Stock(name,(500,2500),100,Player,window_offset,stocknames) for name in stocknames}


# stock1 = Stock('SNTOK',(1600,0),(800,400),(500,2500),75,Player,window_offset)
# # stock1 = Stock('SNTOK',(1600,0),(0,800),randint(500,2500),5)
# stock2 = Stock('KSTON',(800,0),(0,400),(500,2500),110,Player,window_offset)
# stock3 = Stock('STKCO',(800,400),(0,1080),(500,2500),140,Player,window_offset)
# stock4 = Stock('XKSTO',(1600,400),(800,1080),(2300,2310),180,Player,window_offset)

ui_controls = UI_controls((window_offset[0]*-1,window_offset[1]))
Mousebuttons = 0
Tick = 0
stocklist = [stockdict[name] for name in stocknames]
if __name__ == "__main__":
    while True:
        mousex,mousey = pygame.mouse.get_pos()
        screen.fill((20,20,20))
        
        if Tick < 6: Tick += 1#used for ui_controls.update
        else: Tick = 1
        # print(time.time())
        # print(time.asctime())
        # start_time = timeit.default_timer()
        stockgraphmanager.draw_graphs(screen,stocklist,player,ui_controls.logic(Tick),Mousebuttons,stockbook.menudrawn,stockbook,gametime)
        # end_time = timeit.default_timer()
        # print(f"Execution times stock graph: {end_time - start_time} seconds")
        if ui_controls.logic(Tick):
            gametime = Gametime(gametime,ui_controls.playing,screen,clock.get_fps())
            for stock in stocklist:
                stock.update_price(player)
            player.update_price(player)
        player.draw(screen,player,(1920,0),(1600,400),stocklist,Mousebuttons)
        drawgametime(gametime,screen)
        ui_controls.draw(screen,Mousebuttons,stockbook.menudrawn)#draws the ui controls to the screen, and senses for clicks


        stockbook.draw_icon(screen,Mousebuttons,stocklist,ui_controls.logic(Tick),player)

        screen.blit(update_fps(clock),(1570,0))


        Mousebuttons = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for stock in stocklist:
                    stock.save_data()
                player.save_data()
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                for stock in stocklist:
                    stock.save_data()
                player.save_data()
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and Mousebuttons == 0:
                # print(event.button)
                Mousebuttons = event.button
                # if Mousebuttons == 1:
                    # print(stock1.pricepoints)
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     Mousebuttons = 0
            #     print('mouse up')

        
        pygame.display.update()

        clock.tick(60)


