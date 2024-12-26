# list each stock name with the next three lines being a event that would cause the stock volatility to rise, don't include wether or not it is positive or negative
#  example of a stock event: VIXEL (VXL) has announced that they have made a new product that will be released in 2 months
# do not repeat the same phrase for different stocks (ex. don't have two stocks that say "has announced that they have made a new product that will be released in 2 months")

# SNTOK (SNT) has announced that they have made a new product that will be released in 2 months
import pygame
from pygame import gfxdraw
from Defs import *
from random import randint

class News():
    def __init__(self,stocklist):
        self.eventlist = []
        # self.prerendertext = fontlistcry[50].render('News', (255, 255, 255))[0]
        self.prerendertext = s_render('News', 50, (255, 255, 255),font='cry')
        
        self.positiveEvents = {}
        self.negativeEvents = {}
        self.loadNewsEvents()

        self.stock = stocklist[0]
        self.txt = self.grantText()
        

    def grantText(self) -> str:
        """Grants a random text to the news bar"""
        if self.stock.priceEffects.pastReports[0].getPerf() > 0:
            return self.positiveEvents[self.stock.name][randint(0,4)]
        return self.negativeEvents[self.stock.name][randint(0,4)]

    
        
    def loadNewsEvents(self) -> None:
        """Loads the news events from the companyNews.txt file"""
        with open('Assets\GameTexts\companyNews.txt','r') as f:
            lines = f.readlines()
            lines = [l.replace("\n",'') for l in lines]

            for stock in STOCKNAMES:
                index = lines.index(stock)
                self.positiveEvents[stock] = lines[index+1:index+6]
                self.negativeEvents[stock] = lines[index+7:index+12]

    def changeStock(self,stock) -> None:
        """Changes the stock of the news bar"""
        self.stock = stock# assigns a new stock to the news bar
        self.txt = self.grantText()# assigns a new text to the news bar

    def draw(self, screen: pygame.Surface, gametime):

        # drawCenterTxt(screen, self.stock.name, 90, self.stock.color, (680, 630), centerX=False, centerY=False)# blits the stock name to the screen
        drawCenterTxt(screen, self.stock.name, 90, self.stock.color, (265, 715), centerX=False, centerY=False)# blits the stock name to the screen
        
        drawCenterTxt(screen, FSTOCKNAMEDICT[self.stock.name], 45, (180, 180, 180), (397, 745), centerX=False)
        # gfxdraw.filled_polygon(screen, [(275, 815), (280, 855), (405, 855), (400, 815)], (40, 40, 40))  # gap between the top, left, and right
        # screen.blit(self.prerendertext, (300, 820))
        report = self.stock.priceEffects.pastReports[0]

        txt = f'{"Beat" if report.getPerf() > 0 else "Miss"} Expectations {"+" if report.getPerf() > 0 else ""}{limit_digits(report.getPerf(),16)}%'
        drawCenterTxt(screen, txt, 50, (200, 0, 0) if report.getPerf() < 0 else (0,200,0), (1440, 715), centerX=False,centerY=False,fullX=True)
        

        percentChange = self.stock.getPercentDate(report.getTime(),gametime)
        txt = f"Stock {'Up' if percentChange > 0 else 'Down'} {'+' if percentChange > 0 else ''}{limit_digits(percentChange,20)}%"
        drawCenterTxt(screen, txt, 40, p3choice((200,0,0),(0,200,0),(200,200,200),percentChange), (310, 1005), centerX=False, centerY=False)
        
        txt = f"Next Report In {self.stock.priceEffects.daysTillNextReport(gametime)} Days"
        drawCenterTxt(screen, txt, 40, (200, 200, 200), (1455, 1005), centerX=False, centerY=False,fullX=True)

        # txt = f"Volatility: {limit_digits(self.stock.getVolatility()*100,20)}%"
        # drawCenterTxt(screen, txt, 40, (200, 200, 200), (882, 1005), centerX=True, centerY=False)

        for i, text in enumerate(separate_strings(self.txt, 3)):
            x = 290 + (i * 10)
            y = 820 + (i * 50)
            renderedTxt = s_render(text, 50, (255, 255, 255),font='cry')
            # drawCenterTxt(screen, text, 50, (255, 255, 255), (x, y), centerX=False, centerY=False,font='cry')
            drawCenterRendered(screen, renderedTxt, (x, y), centerX=False, centerY=False)
            pygame.draw.line(screen, (120, 120, 120), (x, y+5+renderedTxt.get_height()), (x+renderedTxt.get_width(), y+5+renderedTxt.get_height()), 2)

            


        
        

       