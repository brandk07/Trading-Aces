import pygame
from Defs import *
from Classes.imports.Latterscroll import LatterScroll

class Transactions:
    def __init__(self) -> None:
        self.transactlog = []# list of lists containing [texts1,texts2,texts3]
        self.getFileData()
        # self.transactlog = [["Sold 39 Shares of","KSTON for $5,056.93","Balance $26,103.18"] for i in range(10)]# list of lists containing [texts1,texts2,texts3]
        self.latterscroll = LatterScroll()
        self.surfs = []
        self.scrollvalue = 0

    def getFileData(self):
        with open(r'Assets\transactions.json','r') as f:
            data = [json.loads(line) for line in f]
            for line in data:
                self.transactlog.append(line)

    def storeTransactions(self):
        with open(r'Assets\transactions.json','w') as f:
            f.seek(0)  # go to the start of the file
            f.truncate()  # clear the file
            for line in self.transactlog:
                f.write(json.dumps(line)+'\n')
        
    def getTransactions(self) -> list:
        """Returns the transactlog"""
        return self.transactlog
     
    # def drawscroll(self,screen,coords:tuple,wholewh:tuple,polywh,mousebuttons:int):
    #     """Wholewh is the wh of the whole element
    #     polywh is the wh of each transaction displayed"""
    #     textlist = self.transactlog
        
    #     textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
    #     textcoords = [[(10,10),
    #                    (10,(textlist[i][0],20)),
    #                 #    (10,10+int(polywh[1]/4)*2),
    #                     ((textlist[i][2],-polywh[0]+40),(textlist[i][0],20)),
    #                    (10,(textlist[i][0],textlist[i][1],35)),
    #                    ((textlist[i][4],-polywh[0]+40),(textlist[i][0],textlist[i][1],35)),] for i in range(len(textlist))]

    #     sizes = [50,40,40,40,40]
    #     # text example = ["Sold 1 STAR call Option", "02/15/2030", "Profited $160.69", "Value +$714.81", "Balance $852.82"]
    #     # ["Added 1 BOTS put Option", "02/15/2030", "", "Cost -$121.00", "Balance $760.17"]

    #     # loop through the textlist and store the text info in the textinfo list
    #     for i,text in enumerate(textlist):
    #         adjcolor = (230,10,10) if 'Lost' in textlist[i][2] or '-' in textlist[i][3] else (10,230,10)
    #         colors = [(190,190,190),(190,190,190),adjcolor,adjcolor,(190,190,190)]
    #         polytexts = [[text[ii],sizes[ii],colors[ii]] for ii in range(len(text))]# temporary list to store the text info for each asset
    #         textinfo.append(polytexts)

    #     self.latterscroll.storetextinfo(textinfo)# simply changes the self.texts in latterscroll

    #     self.latterscroll.set_textcoords(textcoords)# simply changes the self.textcoords in latterscroll
    #     # Does most of the work for the latter scroll, renders the text and finds all the coords
    #     scrollmaxcoords = wholewh
    #     self.latterscroll.store_rendercoords(coords, scrollmaxcoords,polywh[1],0,0,updatefreq=10)

    #     # drawing the latter scroll and assigning the selected asset
    #     self.latterscroll.draw_polys(screen, coords, scrollmaxcoords, mousebuttons, 0,drawbottom=False)# draws the latter scroll and returns the selected asset



    def addTransaction(self,Date:str,Action:str,ProfitUnit:str,Balance:str):
        """Date, Action, Profit/Unit Cost, Balance
            Action - Sold 1 STAR call Option"""
        self.transactlog.insert(0,[Date,Action,ProfitUnit,Balance])

    # def draw(self,screen,mousebuttons,coords:tuple,wh:tuple,polywh):
    #     if self.transactlog:
    #         pygame.draw.rect(screen,(0,0,0),pygame.Rect(coords[0],coords[1],polywh[0],wh[1]-coords[1]),5)

    #         self.drawscroll(screen,(coords[0]+10,coords[1]+95),(wh[0]-20,wh[1]),polywh,mousebuttons)

    #         ttext = s_render('Transactions',65,(255,255,255))
    #         screen.blit(ttext,(coords[0]+(polywh[0]/2)-(ttext.get_width()/2),coords[1]+10))
    # def addsurf(self,texts1:list,texts2:list,texts3:list,textwidth:int):
    #     surf = pygame.Surface((self.width-20,self.height-20),pygame.SRCALPHA,32)
    #     # surf.fill((255,255,255))
    #     pygame.draw.rect(surf,(0,0,0),pygame.Rect(0,0,self.width-20,self.height-20),4)
    #     totalwidth = 10
    #     for i,(text,color) in enumerate(texts1):
    #         text = s_render(text,textwidth,color)
    #         surf.blit(text,(totalwidth,10))
    #         totalwidth += text.get_width()
    #     totalwidth = 10
    #     for i,(text,color) in enumerate(texts2):
    #         text = s_render(text,textwidth,color)
    #         surf.blit(text,(totalwidth,10+int(self.height/4)))
    #         totalwidth += text.get_width()
    #     totalwidth = 10
    #     for i,(text,color) in enumerate(texts3):
    #         text = s_render(text,textwidth,color)
    #         surf.blit(text,(totalwidth,10+int(self.height/4)*2))
    #         totalwidth += text.get_width()

    #     self.surfs.append(surf)
    # def scrollcontrols(self, mousebuttons, coords, wh):
    #     mousex,mousey = pygame.mouse.get_pos()
    #     if pygame.Rect.collidepoint(pygame.Rect(coords[0],coords[1],wh[0],wh[1]),mousex,mousey):
    #         if mousebuttons == 4 and self.scrollvalue > 0:
    #             self.scrollvalue -= 30
    #         elif mousebuttons == 5:
    #             self.scrollvalue += 30

        
    # def draw(self,screen,coords:tuple,maxheight:int,mousebuttons:int):
    #     self.scrollcontrols(mousebuttons,coords,(self.width,maxheight))

        # points = [(coords[0],coords[1]),(coords[0]+self.width,coords[1]),(coords[0]+self.width,maxheight),(coords[0],maxheight)]
        # gfxdraw.filled_polygon(screen,points,(60,60,60,200))
        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(coords[0],coords[1],self.width,maxheight-coords[1]),5)

        # ttext = s_render('Transactions',65,(255,255,255))
        # screen.blit(ttext,(coords[0]+(self.width/2)-(ttext.get_width()/2),coords[1]+10))

    #     y = coords[1]+95-self.scrollvalue
    #     for i,surf in enumerate(self.surfs):
    #         # if i+self.scrollvalue > coords[1]+95 and i+self.scrollvalue < coords[1]+maxheight:
    #         if y+self.height-30 >= coords[1] and y < maxheight-40:
    #             screen.blit(surf,(coords[0]+10,y))
    #             y += self.height+10

