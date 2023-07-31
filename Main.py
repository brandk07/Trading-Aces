import pygame
from random import randint
import time
from Defs import *
from Classes.Stockprice import Stock
from Classes.UI_controls import *
from Classes.Playerportfolio import Player
from Classes.StockGraphManager import StockGraphManager

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

stockgraphmanager = StockGraphManager()

player = Player(window_offset)

stocknames = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
#name, startingvalue_range, volatility, Playerclass, window_offset
stockdict = {name:Stock(name,(500,2500),10,Player,window_offset) for name in stocknames}

# stock1 = Stock('SNTOK',(1600,0),(800,400),(500,2500),75,Player,window_offset)
# # stock1 = Stock('SNTOK',(1600,0),(0,800),randint(500,2500),5)
# stock2 = Stock('KSTON',(800,0),(0,400),(500,2500),110,Player,window_offset)
# stock3 = Stock('STKCO',(800,400),(0,1080),(500,2500),140,Player,window_offset)
# stock4 = Stock('XKSTO',(1600,400),(800,1080),(2300,2310),180,Player,window_offset)
ui_controls = UI_controls((window_offset[0]*-1,window_offset[1]))
Mousebuttons = 0
Tick = 0
stocklist = [stockdict[name] for name in stocknames]
while True:
    mousex,mousey = pygame.mouse.get_pos()
    screen.fill((20,20,20))
    
    if Tick < 4: Tick += 1#used for ui_controls.update
    else: Tick = 0
    
    stockgraphmanager.draw_graphs(screen,stocklist,player,ui_controls.logic(Tick),Mousebuttons)
    # for stock in stocklist:#drawing things to screen  
    #     stock.update(screen,ui_controls.logic(Tick),player)
    #     stock.buy_sell(player,screen,Mousebuttons)
    
    # player.graph(stocklist)
    # player.update(screen,ui_controls.logic(Tick),player,stocklist)

    ui_controls.draw(screen,Mousebuttons)#draws the ui controls to the screen, and senses for clicks
    screen.blit(update_fps(clock),(1570,0))
    
    Mousebuttons = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

    clock.tick(120)


