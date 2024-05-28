import pygame
import timeit
from Defs import *
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
from Classes.Stockbook import quantityControls
from Classes.AssetTypes.OptionAsset import OptionAsset
import math

#used for the Owned options
DX = 300
DY = 200
DH = 120

class Optiontrade(Menu):
    def __init__(self,stocklist:list,gametime,player):
        # self.icon = pygame.image.load(r'Assets\Portfolio\portfolio2.png').convert_alpha()

        self.icon = pygame.image.load(r'Assets\Menu_Icons\noblack_option3.png').convert_alpha()

        self.icon = pygame.transform.scale(self.icon, (140, 100))
        
        super().__init__(self.icon)
        
        
        self.barowned = SliderBar(50,[(180,120,0),(110,110,110)])
        self.barowned.value = 0
        self.baravailable = SliderBar(50,[(180,120,0),(110,110,110)])
        self.baravailable.value = 0
        # self.icon.set_colorkey((255,255,255))
        self.optiontext = fontlist[65].render('Options',(220,220,220))[0]
        self.ownedtext = [fontlist[50].render('Owned',(220,220,220))[0],fontlist[50].render('Owned',(0,200,0))[0]]
        self.availabletext = [fontlist[50].render('Available',(220,220,220))[0],fontlist[50].render('Available',(0,200,0))[0]]
        self.customtext = [fontlist[50].render('Custom',(220,220,220))[0],fontlist[50].render('Custom',(0,200,0))[0]]
        self.putoptions = []
        self.calloptions = []
        self.refresh_text, _ = fontlist[60].render(f'REFRESH OPTIONS', (225,225,225))
        self.menudrawn = False
        self.renderedpietexts = None; self.renderedback = None
        self.allrenders = []
        self.selected_option = None
        self.view = "Owned"# Owned or Available or Custom
        self.selected_avalaible = None
        self.refreshOptions(stocklist,gametime,player)

    
        
    def getpoints(self, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]

    def SelectedPlayerOption(self, screen, optionindex, mousebuttons, player):
        if optionindex != None:
            option = player.options[optionindex]
            option.getValue(True)# force updates the price of the option (since it is selected)

            mousex, mousey = pygame.mouse.get_pos()
            
           
            # draw a trapozid using gfxdraw.filled_polygon from 1050,565 to 1529,925
            gfxdraw.filled_polygon(screen, [(1000, 200), (1480, 200), (1565, 925), (1100, 925)], (30, 30, 30))
            pygame.draw.polygon(screen, (0, 0, 0), [(1000, 200), (1480, 200), (1565, 925), (1100, 925)], 5)

            # draw the stock name
            text = fontlist[45].render(f'{option.stockobj.name} Option', (190, 190, 190))[0]
                
            screen.blit(text, (1015, 215))
            # use the same system found in the stockbook class to draw the sell button and the selector for the amount of stocks to sell
            if point_in_polygon((mousex,mousey),[(1110,805),(1125,875),(1465,875),(1450,805)]):
                sellcolor = (150,0,0)
                if mousebuttons == 1:
                    player.sellOption(option,1)
                    self.selected_option = None
            else:
                sellcolor = (225,225,225)

            xshift = 15
            yshift = 100
            text = []   
            # draw a polygon from 1030,230 to 1500, 675
            points = [(1030, 260), (1450, 260), (1500, 675), (1100, 675)]
            gfxdraw.filled_polygon(screen, points, (15, 15, 15))
            pygame.draw.polygon(screen, (0, 0, 0), points, 5)

            # Draws the information about the option on the right side of the screen
            info = [f'Expiration: {option.expiration_date} days',f'Strike Price: ${option.strikePrice}',f'Option type: {option.option_type}',f'Volatility: {limit_digits(option.getVolatility()*100,15)}%']
            for i,txt in enumerate(info):
                screen.blit(fontlist[35].render(txt,(190,190,190))[0],(1050+(i*8),280+(i*50)))

            # for loop to draw lots of polygons with text

            # total value of the stocks above the sell button
            # strikePrice = option.strikePrice
            # text = fontlist[45].render(f'Value: ${limit_digits(value,15)}', (190, 190, 190))[0]
            # gfxdraw.filled_polygon(screen,((1100,705),(1115,775),(1455,775),(1440,705)),(15,15,15))#polygon for the total value button
            # pygame.draw.polygon(screen, (0,0,0), ((1110,705),(1125,775),(1465,775),(1450,705)),5)#outline total value button polygon

            value = option.getValue()
            text = fontlist[45].render(f'Value: ${limit_digits(value,15)}', (190, 190, 190))[0]
            gfxdraw.filled_polygon(screen,((1100,705),(1115,775),(1455,775),(1440,705)),(15,15,15))#polygon for the total value button
            pygame.draw.polygon(screen, (0,0,0), ((1110,705),(1125,775),(1465,775),(1450,705)),5)#outline total value button polygon
            
            screen.blit(text, (1130, 725))
            # sell button
            gfxdraw.filled_polygon(screen,((1110,805),(1125,875),(1465,875),(1450,805)),(15,15,15))#polygon for the sell button
            pygame.draw.polygon(screen, (0,0,0), ((1110,805),(1125,875),(1465,875),(1450,805)),5)#outline sell button polygon
            sell_text, _ = fontlist[65].render(f'SELL', sellcolor)
            sell_text_rect = sell_text.get_rect(center=(1280, 840))
            screen.blit(sell_text, sell_text_rect)

    def draw_Owned(self,screen,mousebuttons,player):
        mousex, mousey = pygame.mouse.get_pos()
        xshift = 15
        yshift = 150    
        if len(self.allrenders) < len(player.options):# if the player has more stocks than the renders
            for i in range((len(player.options)-len(self.allrenders))+1):# add the amount of renders needed
                self.allrenders.append({})
        if self.selected_option == None and len(player.options) > 0:
            self.selected_option = 0
        self.barowned.scroll(mousebuttons)# check for the scroll of the bar
        self.barowned.changemaxvalue(len(player.options) if len(player.options) > 0 else 1)# change the max value of the bar based on the amount of stocks the player has

        barheight = (520//len(player.options)) if len(player.options) > 0 else 1

        self.barowned.draw_bar(screen, [225, DY], [45, DY + (yshift*4) - 80], 'vertical', barwh=[43, barheight], shift=85, reversedscroll=True, text=False)
        if len(player.options) > 0:
            self.SelectedPlayerOption(screen, self.selected_option, mousebuttons, player)# draws the additional stock info

        percents = []; alltexts = []
        for i, option in enumerate(player.options[self.barowned.value:self.barowned.value+5]):
            if option.ogvalue == 0: percentchange = 0
            else:percentchange = option.getPercent()
            
            if percentchange > 0:
                grcolor = (0, 200, 0); profittext = "Profit"
                
            elif percentchange == 0:
                grcolor = (200, 200, 200); profittext = ""
            else:
                grcolor = (225, 0, 0); profittext = "Loss"

            textinfo = [[(190, 190, 190), 45],[(190, 190, 190), 35],[grcolor, 35],[grcolor, 35],[grcolor, 35]]



            texts = [f'{option.stockobj.name} {option.option_type}',
                     f'Initial: ${limit_digits(option.ogvalue,15)}',
                     f'Current: ${limit_digits(option.getValue(),15)}',
                     f'{profittext}: ${limit_digits((option.getValue() - (option.ogvalue)),15)}',
                     f'Change %: {limit_digits(percentchange,15)}%'
                    ]
            self.allrenders = reuserenders(self.allrenders, texts, textinfo, i)
            percents.append(percentchange); alltexts.append(texts)

        self.allrenders,self.selected_option = drawLatterScroll(screen,player.options,self.allrenders,self.barowned.value,self.getpoints,(xshift,yshift),self.selected_option,mousebuttons,DH,alltexts,percents)
    def refreshOptions(self,stocklist:list,gametime,player):
        self.calloptions = []; self.putoptions = []
        for i in range(5):
            stock = stocklist[random.randint(0,len(stocklist)-1)]
            strikeprice = random.randint(math.floor(stock.price*0.95)*100,math.ceil(stock.price*1.2)*100)/100

            self.putoptions.append(OptionAsset(stock,strikeprice,random.randint(3,25),'put',str(gametime),1,player.getNetworth()))
            
        for i in range(5):
            stock = stocklist[random.randint(0,len(stocklist)-1)]
            strikeprice = random.randint(math.floor(stock.price*0.8)*100,math.ceil(stock.price*1.05)*100)/100
            self.calloptions.append(OptionAsset(stock,strikeprice,random.randint(3,25),'call',str(gametime),1,player.getNetworth()))

    def SelectedAvailableOption(self, screen, optionindex, mousebuttons, player):
         if optionindex != None:
            option = (self.putoptions+self.calloptions)[optionindex]
            option.getValue(True)# force updates the price of the option (since it is selected)

            mousex, mousey = pygame.mouse.get_pos()
           
            # draw a trapozid using gfxdraw.filled_polygon from 1050,565 to 1529,925
            gfxdraw.filled_polygon(screen, [(1000, 200), (1480, 200), (1565, 925), (1100, 925)], (30, 30, 30))
            pygame.draw.polygon(screen, (0, 0, 0), [(1000, 200), (1480, 200), (1565, 925), (1100, 925)], 5)

            # draw the stock name
            text = fontlist[45].render(f'{option.stockobj.name} Option', (190, 190, 190))[0]
            screen.blit(text, (1015, 215))
           

            xshift = 15
            yshift = 100
            text = []   

            # draw a polygon from 1030,230 to 1500, 675
            points = [(1030, 260), (1450, 260), (1500, 675), (1100, 675)]
            gfxdraw.filled_polygon(screen, points, (15, 15, 15))
            pygame.draw.polygon(screen, (0, 0, 0), points, 5)

            # Draws the information about the option on the right side of the screen
            info = [f'Expiration: {option.expiration_date} days',f'Strike Price: ${option.strikePrice}',f'Option type: {option.option_type}',f'Volatility: {limit_digits(option.getVolatility()*100,15)}%']
            for i,txt in enumerate(info):
                screen.blit(fontlist[35].render(txt,(190,190,190))[0],(1050+(i*8),280+(i*50)))
            
             # use the same system found in the stockbook class to draw the sell button and the selector for the amount of stocks to sell
            if point_in_polygon((mousex,mousey),[(1110,805),(1125,875),(1465,875),(1450,805)]):
                sellcolor = (150,0,0)
                if mousebuttons == 1:
                    if player.cash > (option.getValue(True)):
                        # player.buyOption(option.copy())
                        player.buyAsset(option.copy())
            else:
                sellcolor = (225,225,225)
            # gfxdraw.filled_polygon(screen,((1100,705),(1115,775),(1455,775),(1440,705)),(15,15,15))#polygon for the total value button
            # pygame.draw.polygon(screen, (0,0,0), ((1110,705),(1125,775),(1465,775),(1450,705)),5)#outline total value button polygon

            value = option.getValue()
            text = fontlist[45].render(f'Cost: ${limit_digits(value,15)}', (190, 190, 190))[0]
            gfxdraw.filled_polygon(screen,((1100,705),(1115,775),(1455,775),(1440,705)),(15,15,15))#polygon for the total cost button
            pygame.draw.polygon(screen, (0,0,0), ((1110,705),(1125,775),(1465,775),(1450,705)),5)#outline total cost button polygon
            
            screen.blit(text, (1130, 725))
            # PURCHASE button
            gfxdraw.filled_polygon(screen,((1110,805),(1125,875),(1465,875),(1450,805)),(15,15,15))#polygon for the PURCHASE button
            pygame.draw.polygon(screen, (0,0,0), ((1110,805),(1125,875),(1465,875),(1450,805)),5)#outline PURCHASE button polygon
            buy_text, _ = fontlist[65].render(f'PURCHASE', sellcolor)
            buy_text_rect = buy_text.get_rect(center=(1280, 840))
            screen.blit(buy_text, buy_text_rect)

    def draw_Available(self,screen,mousebuttons,player,stocklist,gametime):
        mousex, mousey = pygame.mouse.get_pos()
        xshift = 15
        yshift = 150    
        alloptions = self.putoptions+self.calloptions
        if len(self.allrenders) < len(alloptions):# if the player has more stocks than the renders
            for i in range((len(alloptions)-len(self.allrenders))+1):# add the amount of renders needed
                self.allrenders.append({})
        if self.selected_avalaible == None and len(alloptions) > 0:
            self.selected_avalaible = 0
        self.baravailable.scroll(mousebuttons)# check for the scroll of the bar
        self.baravailable.changemaxvalue(len(alloptions) if len(alloptions) > 0 else 1)# change the max value of the bar based on the amount of stocks the player has
        
        barheight = (520//len(alloptions)) if len(alloptions) > 0 else 1

        self.baravailable.draw_bar(screen, [225, DY], [45, DY + (yshift*4) - 80], 'vertical', barwh=[43, barheight], shift=85, reversedscroll=True, text=False)

        self.SelectedAvailableOption(screen, self.selected_avalaible, mousebuttons, player)# draws the additional stock info

        # draw a polygon similar to the one above but at the starting point 1000,120 rather than 1110,805. Change the rest of the points accordingly
        gfxdraw.filled_polygon(screen,((1000,120),(1015,190),(1455,190),(1440,120)),(15,15,15))#polygon for the refresh button
        pygame.draw.polygon(screen, (0,0,0), ((1000,120),(1015,190),(1455,190),(1440,120)),5)#outline refresh button polygon

        
        screen.blit(self.refresh_text, (1050,135))
        if point_in_polygon((mousex,mousey),[(1000,120),(1015,190),(1455,190),(1440,120)]):
            if mousebuttons == 1:
                soundEffects['clickbutton2'].play()
                self.refreshOptions(stocklist,gametime,player)

        percents = []; alltexts = []
        for i, option in enumerate(alloptions[self.baravailable.value:self.baravailable.value+5]):
            # percentchange = ((option.getValue() - option.ogvalue) / option.ogvalue) * 100
        
            grcolor = (200, 200, 200)

            textinfo = [[(190, 190, 190), 45],[(190, 190, 190), 35],[grcolor, 35],[grcolor, 35],[grcolor, 35]]

            texts = [f'{option.stockobj.name} {option.option_type}',
                     f'Expiration: {option.expiration_date} days',
                     f'Cost: ${limit_digits(option.getValue(),15)}',
                     f'Stock Price : ${limit_digits(option.stockobj.price,15)}',
                     f'Strike Price: ${option.strikePrice}'
                    ]
            self.allrenders = reuserenders(self.allrenders, texts, textinfo, i)
            alltexts.append(texts)

        self.allrenders,self.selected_avalaible = drawLatterScroll(screen,alloptions,self.allrenders,self.baravailable.value,self.getpoints,(xshift,yshift),self.selected_avalaible,mousebuttons,DH,alltexts,[0 for i in range(len(alltexts))])
    def draw_Custom(self,screen,mousebuttons,player):
        pass


    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player, gametime):
        """Draws all of the things in the option menu"""
        screen.blit(self.optiontext,(220,120))# display the option text
        # draw a polygon from 400,120 to 750,160
        ownedPoints = [(400, 110), (555, 110), (565, 170), (415, 170)]
        availablePoints = [(555, 110), (735, 110), (750, 170), (565, 170)]
        customPoints = [(735, 110), (890, 110), (900, 170), (750, 170)]

        gfxdraw.filled_polygon(screen, ownedPoints, (50, 50, 50))
        pygame.draw.polygon(screen, (0, 0, 0), ownedPoints, 5)
        gfxdraw.filled_polygon(screen, availablePoints, (50, 50, 50))
        pygame.draw.polygon(screen, (0, 0, 0), availablePoints, 5)
        gfxdraw.filled_polygon(screen, customPoints, (50, 50, 50))
        pygame.draw.polygon(screen, (0, 0, 0), customPoints, 5)
        # drwa teh ownded and available text
        screen.blit(self.ownedtext[1] if self.view == 'Owned' else self.ownedtext[0],(435,120))
        screen.blit(self.availabletext[1] if self.view == 'Available' else self.availabletext[0],(585,120))
        screen.blit(self.customtext[1] if self.view == 'Custom' else self.customtext[0],(755,120))
        # draw a line in between the owned and available text
        pygame.draw.line(screen,(0,0,0),(555,110),(565,170),5)
        # draw a line in between the available and custom text
        pygame.draw.line(screen,(0,0,0),(735,110),(750,170),5)
        if point_in_polygon(pygame.mouse.get_pos(),ownedPoints):
            if mousebuttons == 1:
                soundEffects['clickbutton2'].play()
                self.view = "Owned"
                for option in player.options:option.getValue()# recalculate the option values
        elif point_in_polygon(pygame.mouse.get_pos(),availablePoints):
            if mousebuttons == 1:
                soundEffects['clickbutton2'].play()
                self.view = "Available"
                for option in (self.putoptions+self.calloptions):option.getValue()# recalculate the option values
        elif point_in_polygon(pygame.mouse.get_pos(),customPoints):
            if mousebuttons == 1:
                soundEffects['clickbutton2'].play()
                self.view = "Custom"

        if self.view == "Owned":
            self.draw_Owned(screen,mousebuttons,player)
        elif self.view == "Available":
            self.draw_Available(screen,mousebuttons,player,stocklist,gametime)
        elif self.view == "Custom":
            self.draw_Custom(screen,mousebuttons,player)