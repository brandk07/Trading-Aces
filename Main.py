import pygame
from random import randint
import time
from Defs import *
from Classes.Stockprice import Stock
from Classes.UI_controls import *
from Classes.Playerportfolio import Player

pygame.init()
screen = pygame.display.set_mode((1920, 800))
pygame.display.set_caption("Investrix")
clock = pygame.time.Clock()
fonts = lambda font_size: pygame.font.SysFont('Cosmic Sans',font_size)

player = Player((1920,0),(1600,400))

stock1 = Stock('SNTOK',(1600,0),(800,400),(500,2500),5)
# stock1 = Stock('SNTOK',(1600,0),(0,800),randint(500,2500),5)
stock2 = Stock('KSTON',(800,0),(0,400),(500,2500),7)
stock3 = Stock('STKCO',(800,400),(0,800),(500,2500),10)
stock4 = Stock('XKSTO',(1600,400),(800,800),(500,2500),14)
ui_controls = UI_controls()
Mousebuttons = 0
Tick = 0
stocklist = [stock1,stock2,stock3,stock4]
while True:
    mousex,mousey = pygame.mouse.get_pos()
    screen.fill((20,20,20))
    
    if Tick < 4: Tick += 1#used for ui_controls.update
    else: Tick = 0
      
    for stock in stocklist:#drawing things to screen  
        stock.update(screen,ui_controls.logic(Tick),Player)
        stock.buy_sell(player,screen,Mousebuttons)
    
    player.graph(stocklist)
    player.update(screen,ui_controls.logic(Tick),Player)

    ui_controls.draw(screen,Mousebuttons)#draws the ui controls to the screen, and senses for clicks
    screen.blit(update_fps(clock),(1570,0))
    
    Mousebuttons = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and Mousebuttons == 0:
            # print(event.button)
            Mousebuttons = event.button
            # if Mousebuttons == 1:
                # print(stock1.pricepoints)
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     Mousebuttons = 0
        #     print('mouse up')

    
    pygame.display.update()

    clock.tick(120)


