# list each stock name with the next three lines being a event that would cause the stock volatility to rise, don't include wether or not it is positive or negative
#  example of a stock event: VIXEL (VXL) has announced that they have made a new product that will be released in 2 months
# do not repeat the same phrase for different stocks (ex. don't have two stocks that say "has announced that they have made a new product that will be released in 2 months")

# SNTOK (SNT) has announced that they have made a new product that will be released in 2 months
import pygame
from pygame import gfxdraw
from Defs import *
from random import randint

class News():
    def __init__(self):
        self.eventlist = []
        self.prerendertext = fontlistcry[50].render('News', (255, 255, 255))[0]
        self.newstext = {
            'SNTOK': [
                '(SNTOK) Unforeseen fluctuations in the regulatory landscape surrounding drug approvals may introduce uncertainty.',
                '(SNTOK) Unexpected leadership changes could impact the strategic direction, causing uncertainty among shareholders.',
                '(SNTOK) Unanticipated challenges in clinical trials may lead to short-term volatility.',
                '(SNTOK) Surprising developments in the competitive landscape may impact market perception.',
                '(SNTOK) Shifts in global economic conditions may introduce unforeseen challenges for the company.'
            ],
            'KSTON': [
                '(KSTON) Unpredictable disruptions in the global supply chain could lead to short-term volatility.',
                '(KSTON) Unexpected shifts in governmental regulations may require prompt adaptations in business strategies.',
                '(KSTON) Unanticipated technological glitches in new product launches may impact market perception.',
                '(KSTON) Surprising developments in the market demand for sustainable solutions may introduce uncertainties.',
                '(KSTON) Changes in economic indicators may lead to unforeseen challenges in revenue generation.'
            ],
            'STKCO': [
                '(STKCO) Unanticipated cybersecurity vulnerabilities may emerge, influencing market perception.',
                '(STKCO) Unexpected legal disputes or regulatory changes could impact ongoing and future projects, introducing unforeseen challenges.',
                '(STKCO) Unforeseen challenges in implementing successful infrastructure projects may lead to short-term volatility.',
                '(STKCO) Surprising developments in global economic conditions may impact the company\'s diverse portfolio.',
                '(STKCO) Shifts in industry trends may introduce uncertainties in the performance of cutting-edge solutions.'
            ],
            'XKSTO': [
                '(XKSTO) Unforeseen setbacks in space exploration missions may affect investor sentiment.',
                '(XKSTO) Unexpected geopolitical events or policy changes may introduce volatility in the space industry.',
                '(XKSTO) Unanticipated challenges in developing next-generation propulsion systems may impact market positioning.',
                '(XKSTO) Surprising developments in market share dynamics may lead to short-term fluctuations.',
                '(XKSTO) Changes in global economic conditions may introduce unforeseen challenges for space exploration initiatives.'
            ],
            'VIXEL': [
                '(VIXEL) Unpredicted technological glitches in hardware solutions could lead to short-term market fluctuations.',
                '(VIXEL) Unexpected legal challenges in intellectual property may impact product development and market positioning.',
                '(VIXEL) Unforeseen shifts in consumer preferences for virtual reality experiences may introduce uncertainties.',
                '(VIXEL) Surprising developments in the competitive landscape may impact market perception.',
                '(VIXEL) Changes in global economic conditions may introduce unforeseen challenges for the VR industry.'
            ],
            'QWIRE': [
                '(QWIRE) Unforeseen challenges in obtaining necessary permits for renewable energy projects may introduce uncertainties.',
                '(QWIRE) Unanticipated fluctuations in raw material prices may impact production costs and financial performance.',
                '(QWIRE) Unexpected changes in government policies may lead to short-term volatility in the renewable energy sector.',
                '(QWIRE) Surprising developments in market demand for green energy solutions may introduce uncertainties.',
                '(QWIRE) Shifts in global economic conditions may lead to unforeseen challenges for eco-conscious initiatives.'
            ],
            'QUBEX': [
                '(QUBEX) Unpredicted delays in drug development timelines may affect investor confidence.',
                '(QUBEX) Unexpected regulatory hurdles or changes may introduce uncertainties in the biopharmaceutical industry.',
                '(QUBEX) Unforeseen challenges in obtaining necessary approvals for breakthrough therapies may lead to short-term market fluctuations.',
                '(QUBEX) Surprising developments in clinical trial outcomes may impact market positioning.',
                '(QUBEX) Changes in global economic conditions may introduce unforeseen challenges for the biopharmaceutical sector.'
            ],
            'FLYBY': [
                '(FLYBY) Unanticipated disruptions in global travel due to unforeseen events may impact short-term market conditions.',
                '(FLYBY) Unexpected shifts in tourism policies or geopolitical events may introduce uncertainties in the travel industry.',
                '(FLYBY) Unforeseen challenges in delivering unique travel experiences may lead to short-term volatility.',
                '(FLYBY) Surprising developments in the competitive landscape may impact market perception.',
                '(FLYBY) Changes in global economic conditions may introduce unforeseen challenges for the adventure tourism sector.'
            ],
            'MAGLO': [
                '(MAGLO) Unpredicted attention impacting brand perception may introduce short-term fluctuations.',
                '(MAGLO) Unexpected legal challenges in product distribution may influence market positioning.',
                '(MAGLO) Unforeseen challenges in maintaining culinary innovations may lead to short-term volatility.',
                '(MAGLO) Surprising developments in the competitive landscape may impact market perception.',
                '(MAGLO) Shifts in global economic conditions may introduce unforeseen challenges for the gourmet culinary sector.'
            ]
        }

        # Everything below is the code that separates the strings into three equal parts
        # I wanted to separate the strings by their len, but not split words in half
        # This makes it much more challenging to code, but only took 35 minutes of work - Ai wans't very helpful
        
        self.newstext = separate_strings(self.newstext, 3)
       

    def addNews(self,event:str,duration,color,eventname):
            self.newstext[eventname] = ([fontlist[25].render(event,(90,90,90))[0],color,duration])
    
    def addStockNews(self,stockname:str,duration=600):
        # print(stockname)
        color = (150,150,150)
        # testlist = self.newstext[stockname][randint(0,4)]
        texts = self.newstext[stockname][randint(0,4)]
        rendered = []
        for text in texts:
            rendered.append(fontlistcry[55].render(text,color)[0])

        self.eventlist.append([*rendered,duration])


    def draw(self, screen: pygame.Surface):
        gfxdraw.filled_polygon(screen, [(275, 815), (280, 855), (405, 855), (400, 815)], (40, 40, 40))  # gap between the top, left, and right
        screen.blit(self.prerendertext, (300, 820))
        if self.eventlist:
            if self.eventlist[0][-1] > 0:
                self.eventlist[0][-1] -= 1  # decreases the duration of the event
                *texts, duration = self.eventlist[0]
                # pygame.draw.line(screen, (120, 120, 120), (270, 860), (1340, 860), 2)  # line above the first line of text
                for i, text in enumerate(texts):
                    x = 300 + (i * 10)
                    y = 870 + (i * 50)
                    screen.blit(text, (x, y))
                    pygame.draw.line(screen, (120, 120, 120), (x-20, y+5+text.get_height()), (x+text.get_width()+10, y+5+text.get_height()), 2)
            else:
                self.eventlist.pop(0)
                    


        
        

       