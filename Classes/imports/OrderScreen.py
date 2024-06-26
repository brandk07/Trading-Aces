import pygame
from pygame import gfxdraw
import pygame.gfxdraw
from Defs import *
from Classes.imports.Numpad import Numpad
from Classes.UIControls import UIControls
from Classes.imports.Latterscroll import LatterScroll
TXTCOLOR = (220,220,220)

class OrderScreen:
    """This class will be used in stockbook and porfolio to buy or sell stocks"""
    def __init__(self,uicontrols) -> None:
        self.orderTypes = ['Market','Limit','Stop']
        self.orderType = 'Market'
        self.transactionTypes = ['Buy','Sell']
        self.transactionType = 'Buy'
        background = pygame.image.load(r'Assets\backgrounds\Background (9).png').convert_alpha()
        background = pygame.transform.smoothscale_by(background,2);background.set_alpha(140)
        self.background = background
        # self.wh = [960,650]
        self.whDict = {'MarketBuy':[550,650],'MarketSell':[960,650],'LimitBuy':[960,650],'LimitSell':[960,650],'StopBuy':[960,650],'StopSell':[960,650]}

        # self.surf = pygame.Surface((self.whDict[self.orderType+self.transactionType][0],self.whDict[self.orderType+self.transactionType][1]))
        self.surfs = {key:pygame.Surface((self.whDict[key][0],self.whDict[key][1])) for key in self.whDict.keys()}
        for key in self.surfs.keys():
            self.surfs[key].fill((0,0,0))
            self.surfs[key].blit(self.background,(-750,-200))
        # self.surf.blit(background,(-480,-270))
        self.surfCoords = [750,200]
        self.lastMousePos = [0,0]
        self.numPad = Numpad(displayText=False)
        self.uicontrols : UIControls = uicontrols
        self.latterScroll = LatterScroll()
        self.selectedAsset = None
    
    def reBlitDisplays(self):
        for key in self.surfs.keys():
            self.surfs[key].fill((0,0,0))
            self.surfs[key].blit(self.background,(-self.surfCoords[0],-self.surfCoords[1]))

    def executeOrder(self,player,stockObj,gametime):
        """Executes the order that the player has selected"""
        if self.numPad.getValue() == 0:
            return
        if self.transactionType == 'Buy':
            if self.orderType == 'Market':
                player.buyAsset(StockAsset(player,stockObj,gametime.getTime(),stockObj.price,self.numPad.getValue()))
            elif self.orderType == 'Limit':
                pass
            elif self.orderType == 'Stop':
                pass
        elif self.transactionType == 'Sell':
            if self.orderType == 'Market':
                # print
                self.selectedAsset.sell(player,self.numPad.getValue())
            elif self.orderType == 'Limit':
                pass
            elif self.orderType == 'Stop':
                pass

    def draw(self,screen,stockObj,mousebuttons:int,player,gametime):
        # self.uicontrols.bar.changeMaxValue(5)
        
        mousex,mousey = pygame.mouse.get_pos()
        x,y = self.surfCoords   
        wh = self.whDict[self.orderType+self.transactionType]
        surf = self.surfs[self.orderType+self.transactionType]
        points = [(x,y),(wh[0]+x,y),(wh[0]+x,wh[1]+y),(x,wh[1]+y)]  
        collide = pygame.Rect.collidepoint(pygame.Rect(x-20,y-20,wh[0]+40,wh[1]+40),mousex,mousey)

        if collide and pygame.mouse.get_pressed()[0]:
            xdiff,ydiff = mousex-self.lastMousePos[0],mousey-self.lastMousePos[1]
            if xdiff != 0 or ydiff != 0:
                self.surfCoords[0] += xdiff
                self.surfCoords[1] += ydiff
            
                surf.fill((0,0,0))
                surf.blit(self.background,(-self.surfCoords[0],-self.surfCoords[1]))
                
                
        self.lastMousePos = [mousex,mousey]
        
        # gfxdraw.filled_polygon(screen,points,(50,50,50))
        screen.blit(surf,(x,y))    
        pygame.draw.polygon(screen,(0,0,0),points,10)
        # --------------Title that says what type of order it is--------------
        title = s_render(f'{self.orderType.upper()} Order',85,TXTCOLOR)
        screen.blit(title,(20+x,10+y))
        stockName = s_render(f'{stockObj.name}',85,(stockObj.color))
        screen.blit(stockName,(wh[0]-stockName.get_width()+x-10,10+y))


        # --------------draw the order type and transaction type--------------
        orderTypeText = s_render('Order & Transaction Type',35,TXTCOLOR)
        screen.blit((orderTypeText),(20+x,80+y))
        result = checkboxOptions(screen,self.orderTypes,self.orderType,(500,35),(20+x,y+90+orderTypeText.get_height()),mousebuttons)# draws the checkbox for the order type
        if result != None and result[0] != self.orderType:
            self.orderType = result[0]
            self.reBlitDisplays()

        result = checkboxOptions(screen,self.transactionTypes,self.transactionType,(500,35),(20+x,170+y),mousebuttons)# draws the checkbox for the sell vs buy
        if result != None and result[0] != self.transactionType:
            self.transactionType = result[0]
            self.reBlitDisplays()

        if self.orderType == 'Market':
            self.drawMarketInfo(screen,stockObj,mousebuttons,player,(x,y))
            
        # --------------Cancel button and confirm button --------------
        cancelButton = s_render('Cancel',40,(200,200,200))

        if pygame.Rect.collidepoint(pygame.Rect(wh[0]+x-cancelButton.get_width()-10,610+y,cancelButton.get_width(),cancelButton.get_height()),mousex,mousey):# if the mouse is colliding with the cancel button
            cancelButton = s_render('Cancel',40,(180,0,0))
            if mousebuttons == 1:
                return False
        
        screen.blit(cancelButton,(wh[0]+x-cancelButton.get_width()-10,610+y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x+50, y+380, 350, 50),5,10)
        
        confirmColor = TXTCOLOR
        if pygame.Rect.collidepoint(pygame.Rect(x+50, y+380, 350, 50),mousex,mousey):
            confirmColor = (0,180,0)
            if mousebuttons == 1:
                print('confirmed order')
                self.executeOrder(player,stockObj,gametime)

        confirmtxt = s_render('Confirm Order',40,confirmColor)
        screen.blit(confirmtxt,(-5+x+225-confirmtxt.get_width()/2,380+y+10))
        
        return True# if the cancel button is not clicked, return True
    

    def drawMarketInfo(self,screen,stockObj,mousebuttons:int,player,relaviveCoords):
        """Drawing the Shares, price Per, and cost text"""
        x,y = relaviveCoords
        # --------SHARES TEXT AND THE LINE UNDERNEATH--------
        screen.blit(s_render('Shares',40,TXTCOLOR),(20+x,240+y))
        sharesNum = s_render(str(self.numPad.getValue()),40,TXTCOLOR)
        screen.blit((sharesNum),(470-sharesNum.get_width()+x,240+y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10+x, 245+sharesNum.get_height()+y, 465, 3))
        # ---- PRICE PER TEXT AND THE LINE UNDERNEATH---------
        perPrice = s_render('Price Per',40,TXTCOLOR)
        screen.blit(perPrice,(20+x,285+y))
        perPrice = s_render(f'${limit_digits(stockObj.price,24)}',40,TXTCOLOR)
        screen.blit(perPrice,(470-perPrice.get_width()+x,285+y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10+x, 290+perPrice.get_height()+y, 465, 3))
        # ------COST TEXT-------
        screen.blit(s_render('Cost' if self.transactionType == "Buy" else "Value",40,TXTCOLOR),(20+x,330+y))
        cost = s_render(f'${limit_digits(self.numPad.getValue()*stockObj.price,24)}',40,TXTCOLOR)
        screen.blit(cost,(470-cost.get_width()+x,330+y))
        # DIFFERENT SPECIFIC FUNCTIONS FOR BUY AND SELL
        if self.transactionType == "Sell":
            self.drawMarketSell(screen,stockObj,mousebuttons,player,relaviveCoords)
            maxNum = 0 if self.selectedAsset == None else self.selectedAsset.quantity
            self.numPad.draw(screen,(-5+x,445+y),(450,210),"SHARE",mousebuttons,maxNum)# draws the numpad for the shares
        else:# buy
            self.numPad.draw(screen,(-5+x,445+y),(450,210),"SHARE",mousebuttons,int(player.cash/stockObj.price))# draws the numpad for the shares

    def drawMarketSell(self,screen,stockObj,mousebuttons:int,player,relaviveCoords):
        """Draws the latter scroll on the right side"""
        x,y = relaviveCoords
        wh = self.whDict[self.orderType+self.transactionType]
        def get_Quant(asset):
            return f"{asset.quantity} {'Share'}{'' if asset.quantity == 1 else 's'}"
        
        stocks = [stock for stock in player.stocks if stock.stockobj == stockObj]
        stocks.sort(key=lambda x:x.getValue(),reverse=True)

        get_text = lambda asset : [f'{asset} ',asset.dateobj.strftime("%m/%d/%Y"),get_Quant(asset)]
        # getting the text for each asset
        textlist = [get_text(asset) for asset in stocks]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(25,60)] for i in range(len(textlist))]
        # loop through the textlist and store the text info in the textinfo list
        for i,(text,asset) in enumerate(zip(textlist,stocks)):
            polytexts = []# temporary list to store the text info for each asset
            polytexts.append([text[0],50,asset.color])
            polytexts.append([text[1],35,(190,190,190)])
            polytexts.append([text[2],60,(190,190,190)])
            textinfo.append(polytexts)
            coords[i].append(((text[1],50),30))

        self.latterScroll.storetextinfo(textinfo)# simply changes the s.texts in latterscroll
        self.latterScroll.set_textcoords(coords)# simply changes the s.textcoords in latterscroll
        # Does most of the work for the latter scroll, renders the text and finds all the coords
        scrollmaxcoords = (400,wh[1]+y-35)
        ommitted = self.latterScroll.store_rendercoords((x+wh[0]-440, y+80), scrollmaxcoords,135,0,0,updatefreq=60)

        # drawing the latter scroll and assigning the selected asset
        if self.selectedAsset not in stocks:
            self.selectedAsset = None
        selectedindex = None if self.selectedAsset == None else stocks.index(self.selectedAsset)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        newselected = self.latterScroll.draw_polys(screen, (x+wh[0]-440, y+80), scrollmaxcoords, mousebuttons, selectedindex, True, *[sasset.getPercent() for sasset in stocks[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        if newselected == None:
            self.selectedAsset = None
        else:# if the selected asset is not None
            self.selectedAsset = stocks[newselected]

        # make a text saying displaying # out of # assets
        dispText = s_render(f"Displaying {ommitted[0]} - {ommitted[1]-1} out of {len(stocks)}",35,TXTCOLOR)
        screen.blit(dispText,(x+wh[0]-440,y+dispText.get_height()+20))

        
        

        




