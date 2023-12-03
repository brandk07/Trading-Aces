# list each stock name with the next three lines being a event that would cause the stock to go up - postitive
#  do not repeat the same phrase
# list of the stocks you must do,  ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
## list each stock name with the next three lines being an event that would cause the stock to go up - positive
# do not repeat the same phrase
# list of the stocks you must do,  ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
import pygame
from pygame import gfxdraw
from Defs import fontlist
from random import randint
class StockEvents():
    def __init__(self) -> None:
        self.refreshtime = 100
        self.stockevents = {}
        self.events_pos = {
        'SNTOK': [
            '(SNTOK) Positive earnings report',
            '(SNTOK) New drug approval',
            '(SNTOK) Acquisition of competitor',
            '(SNTOK) Breakthrough in regenerative medicine',
            '(SNTOK) Advancements in synthetic biology'
        ],
        'KSTON': [
            '(KSTON) New product announcement',
            '(KSTON) Revenue increase',
            '(KSTON) Positive analyst recommendations',
            '(KSTON) Technological breakthrough in urban mobility',
            '(KSTON) Expansion in sustainable transportation solutions'
        ],
        'STKCO': [
            '(STKCO) Successful infrastructure project',
            '(STKCO) Expansion into new markets',
            '(STKCO) Partnership with well-known brand',
            '(STKCO) Launch of cutting-edge technology solutions',
            '(STKCO) Recognition for innovative industry contributions'
        ],
        'XKSTO': [
            '(XKSTO) Positive news about leadership',
            '(XKSTO) Increase in market share',
            '(XKSTO) Positive industry trends',
            '(XKSTO) Advancements in space propulsion technology',
            '(XKSTO) Successful execution of space exploration missions'
        ],
        'VIXEL': [
            '(VIXEL) Successful virtual reality content launch',
            '(VIXEL) Innovations in immersive hardware solutions',
            '(VIXEL) Positive media coverage',
            '(VIXEL) Breakthroughs in VR user experiences',
            '(VIXEL) Expansion of VR product demand'
        ],
        'QWIRE': [
            '(QWIRE) Positive customer reviews',
            '(QWIRE) Expansion of customer base',
            '(QWIRE) Introduction of innovative features',
            '(QWIRE) Significant growth in renewable energy adoption',
            '(QWIRE) Recognition for eco-conscious practices'
        ],
        'QUBEX': [
            '(QUBEX) Positive economic indicators',
            '(QUBEX) Increase in consumer spending',
            '(QUBEX) Positive investor sentiment',
            '(QUBEX) Transformative breakthroughs in biopharmaceuticals',
            '(QUBEX) Development of critical medical therapies'
        ],
        'FLYBY': [
            '(FLYBY) Successful adventure travel packages',
            '(FLYBY) Increase in sales volume',
            '(FLYBY) Positive media coverage',
            '(FLYBY) Introduction of unique and thrilling travel experiences',
            '(FLYBY) Recognition as a leader in adventure tourism'
        ],
        'MAGLO': [
            '(MAGLO) Positive financial performance',
            '(MAGLO) Increase in dividend payouts',
            '(MAGLO) Positive industry outlook',
            '(MAGLO) Culinary innovations and expanding product line',
            '(MAGLO) Recognition for excellence in gourmet culinary offerings'
        ]
    }
        self.events_neg = {
        'SNTOK': [
            '(SNTOK) Disappointing earnings report',
            '(SNTOK) Setback in drug development',
            '(SNTOK) Loss in market share',
            '(SNTOK) Regulatory challenges in regenerative medicine',
            '(SNTOK) Negative developments in synthetic biology'
        ],
        'KSTON': [
            '(KSTON) Delay in product launch',
            '(KSTON) Decline in revenue',
            '(KSTON) Negative analyst recommendations',
            '(KSTON) Technological setbacks in urban mobility',
            '(KSTON) Struggles in adapting to sustainable transportation solutions'
        ],
        'STKCO': [
            '(STKCO) Project failure in infrastructure',
            '(STKCO) Market contraction in new territories',
            '(STKCO) Termination of key partnerships',
            '(STKCO) Technological glitches in products',
            '(STKCO) Criticism for lack of innovation in the industry'
        ],
        'XKSTO': [
            '(XKSTO) Negative news about leadership',
            '(XKSTO) Decline in market share',
            '(XKSTO) Adverse industry trends',
            '(XKSTO) Setbacks in space propulsion technology',
            '(XKSTO) Mission failures in space exploration'
        ],
        'VIXEL': [
            '(VIXEL) Failure in virtual reality content launch',
            '(VIXEL) Issues in immersive hardware solutions',
            '(VIXEL) Negative media coverage',
            '(VIXEL) Decline in VR product demand',
            '(VIXEL) Challenges in enhancing VR user experiences'
        ],
        'QWIRE': [
            '(QWIRE) Negative customer reviews',
            '(QWIRE) Loss of customer base',
            '(QWIRE) Failures in innovative features',
            '(QWIRE) Slow growth in renewable energy adoption',
            '(QWIRE) Criticism for lacking eco-conscious practices'
        ],
        'QUBEX': [
            '(QUBEX) Negative economic indicators',
            '(QUBEX) Decrease in consumer spending',
            '(QUBEX) Negative investor sentiment',
            '(QUBEX) Setbacks in biopharmaceutical breakthroughs',
            '(QUBEX) Delays in critical medical therapies'
        ],
        'FLYBY': [
            '(FLYBY) Unsuccessful adventure travel packages',
            '(FLYBY) Decline in sales volume',
            '(FLYBY) Negative media coverage',
            '(FLYBY) Challenges in delivering unique travel experiences',
            '(FLYBY) Criticism as a leader in adventure tourism'
        ],
        'MAGLO': [
            '(MAGLO) Poor financial performance',
            '(MAGLO) Decrease in dividend payouts',
            '(MAGLO) Negative industry outlook',
            '(MAGLO) Setbacks in culinary innovations',
            '(MAGLO) Criticism for quality in gourmet culinary offerings'
        ]
    }


    def addStockEvent(self,stock,duration,percent,Postive=True):
        """Postive is a boolean that determines if the stock event is positive or negative"""
        color = (0,140,0) if Postive else (175,0,0)
        if stock not in self.stockevents:
            indexloc = list(self.events_pos).index(stock)
            if Postive:
                addminus = " +"
                self.stockevents[stock] = ([fontlist[25].render(list(self.events_pos.values())[indexloc][randint(0,2)]+addminus+str(percent)+"%",(0,0,0))[0],color,duration])
            else:
                addminus = " -"
                self.stockevents[stock] = ([fontlist[25].render(list(self.events_neg.values())[indexloc][randint(0,2)]+addminus+str(percent)+"%",(0,0,0))[0],color,duration])
            

    def addEvent(self,event:str,duration,color,eventname):
        self.stockevents[eventname] = ([fontlist[25].render(event,(255,255,255))[0],color,duration])

    def draw(self,screen:pygame.Surface):
        """Draws all the stock events to the screen"""
        if len(self.stockevents) > 9:
            for i in range(len(self.stockevents)-9):
                del self.stockevents[list(self.stockevents)[i]]
        events_to_remove = []
        for i,event in enumerate(list(self.stockevents.values())):
            text, color, duration = event
            if duration > 0:
                # draw a polygon behind the text, trapozoid, length of 520, height of 50
                gfxdraw.filled_polygon(screen,[(940,175+(i*55)),(955,215+(i*55)),(940+505,215+(i*55)),(925+505,175+(i*55))],color)
                # createa a border around the polygon
                pygame.draw.polygon(screen,(0,0,0),[(940,175+(i*55)),(955,215+(i*55)),(940+505,215+(i*55)),(925+505,175+(i*55))],5)
                screen.blit(text,(965,185+(i*55)))
                event[2] -= 1# subtracts one from the duration
            else:
                events_to_remove.append(list(self.stockevents)[i])
        
        for event_name in events_to_remove:
            del self.stockevents[event_name]

        # if self.refreshtime > 0:
        #     self.refreshtime -= 1
        # else:
        #     # draws the stock events to the screen
        #     indexloc = list(self.events_pos).index(stock)
        #     text = fontlist[30].render(self.events_pos[indexloc][randint(0,2)],(255,255,255))[0]
        #     screen.blit(text,(1500,650+(i*40)))



