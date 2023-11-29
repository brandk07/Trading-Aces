# list each stock name with the next three lines being a event that would cause the stock volatility to rise, don't include wether or not it is positive or negative
#  example of a stock event: VIXEL (VXL) has announced that they have made a new product that will be released in 2 months
# do not repeat the same phrase for different stocks (ex. don't have two stocks that say "has announced that they have made a new product that will be released in 2 months")

# SNTOK (SNT) has announced that they have made a new product that will be released in 2 months
import pygame
from pygame import gfxdraw
from Defs import fontlist,fontlistcry
from random import randint

class News():
    def __init__(self):
        self.eventlist = []
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

        # Separate strings into two roughly equal-length strings stored in a list
        separated_strings = {}
        addlengths = lambda stringlist: sum([len(string) for string in stringlist])
        for stock, events in self.newstext.items(): # stock is the stock name, events is a list of events
            
            separated_strings[stock] = []
            for event in events: # each event is a string
                separated_events = []
                sub_length = len(event) // 3
                words = event.split(' ')
                # print(words, '1')
                
                for i in range(3):
                    removedwords = []  # Initialize removedwords list
                    # print(words, '2')
                    if i == 2:
                        separated_events.append(' '.join(words))
                    else:
                        while addlengths(removedwords) < sub_length:
                            # print(words, '3')
                            removedwords.append(words.pop(0))
                        separated_events.append(' '.join(removedwords))
                # print(separated_events)
                separated_strings[stock].append(separated_events)
            
        self.newstext = separated_strings
        print(separated_strings)
       

    def addNews(self,event:str,duration,color,eventname):
            self.newstext[eventname] = ([fontlist[25].render(event,(255,255,255))[0],color,duration])
    
    def addStockNews(self,stockname:str,duration=6000):
        # print(stockname)
        testlist = self.newstext[stockname][randint(0,4)]
        rendered1 = fontlistcry[55].render(testlist[0],(255,255,255))[0]
        rendered2 = fontlistcry[55].render(testlist[1],(255,255,255))[0]
        rendered3 = fontlistcry[55].render(testlist[2],(255,255,255))[0]
        self.eventlist.append([rendered1,rendered2,rendered3,duration])

    def draw(self,screen:pygame.Surface):
        if self.eventlist:
            if self.eventlist[0][3] > 0:
                self.eventlist[0][3] -= 1# decreases the duration of the event
                text1,text2,text3,duration = self.eventlist[0]

                screen.blit(text1,(305,880))
                screen.blit(text2,(315,930))
                screen.blit(text3,(325,980))
        
        

       