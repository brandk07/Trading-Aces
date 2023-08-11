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
player = Player(window_offset,stocknames,gametime)
#name, startingvalue_range, volatility, Playerclass, window_offset,stocknames,time
stockdict = {name:Stock(name,(500,2500),100,Player,window_offset,stocknames,gametime) for name in stocknames}


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
    
    if Tick < 6: Tick += 1#used for ui_controls.update
    else: Tick = 1
    # print(time.time())
    # print(time.asctime())
    
    start_time = timeit.default_timer()
    stockgraphmanager.draw_graphs(screen,stocklist,player,ui_controls.logic(Tick),Mousebuttons,stockbook.menudrawn,stockbook,gametime)
    end_time = timeit.default_timer()
    print(f"Execution times stock graph: {end_time - start_time} seconds")

    if ui_controls.logic(Tick):
        gametime = Gametime(gametime,ui_controls.playing,screen,clock.get_fps())
        for stock in stocklist:
            stock.update_price(player,gametime)

    ui_controls.draw(screen,Mousebuttons,stockbook.menudrawn)#draws the ui controls to the screen, and senses for clicks


    stockbook.draw_icon(screen,Mousebuttons,stocklist,ui_controls.logic(Tick),player)

    screen.blit(update_fps(clock),(1570,0))
    # 0.010824900004081428 seconds
    # 0.019969200002378784 seconds

    # 0.0014727000088896602 seconds
    # 0.0018108000076608732 seconds

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

    clock.tick(60)

    # Execution times 2: 0.0003656000044429675 seconds
    # Execution times 3: 0.0006503000040538609 seconds
    # Execution times 1: 0.0003372000064700842 seconds

    # Execution times 2: 0.0003484999906504527 seconds
    # Execution times 3: 0.0006101000035414472 seconds
    # Execution times 1: 0.0007960999937495217 seconds

    # Execution times 2: 0.000338099998771213 seconds
    # Execution times 3: 0.0005828000139445066 seconds
    # Execution times 1: 0.0010402000043541193 seconds
# ------------------------------------------------------------
    # Execution times 1: 0.00011629999789875001 seconds
    # Execution times 2: 5.399997462518513e-06 seconds 0.000005399997462518513
    # Execution times 3: 5.099995178170502e-06 seconds

    # Execution times 1: 0.00011639999866019934 seconds
    # Execution times 2: 8.199989679269493e-06 seconds
    # Execution times 3: 4.0000013541430235e-06 seconds 

    # Execution times 1: 0.0006111000111559406 seconds
    # Execution times 2: 3.7300007534213364e-05 seconds
    # Execution times 3: 7.350000669248402e-05 seconds 

    # Execution times 1: 0.0008095000084722415 seconds
    # Execution times 2: 0.0001795999996829778 seconds
    # Execution times 3: 9.249999129679054e-05 seconds


    # Execution times 1: 0.00258840000606142 seconds
    # Execution times 2: 0.000994000001810491 seconds
    # Execution times 3: 6.92999892635271e-05 seconds


    # Execution times 1: 0.0010986999986926094 seconds
    # Execution times 2: 6.949999078642577e-05 seconds 0.00006949999078642577
    # Execution times 3: 9.299999510403723e-05 seconds


    # Execution times 1: 3.9999940781854093e-07 seconds 0.0000003999999407818541
    # Execution times 1.5: 0.0006681999984721188 seconds 
    # Execution times 2: 6.310000026132911e-05 seconds
    # Execution times 3: 4.7199999244185165e-05 seconds


    # Execution times 1: 6.219999704626389e-05 seconds
    # Execution times 1.4: 4.940000144415535e-05 seconds
    # Execution times 1.5: 0.0017169000020658132 seconds
    # Execution times 2: 8.049999814829789e-05 seconds
    # Execution times 3: 0.00020140000196988694 seconds
