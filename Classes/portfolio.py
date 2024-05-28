import pygame
import timeit
from Defs import *
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
from Classes.imports.Latterscroll import *
from Classes.Stockbook import quantityControls
from Classes.imports.Numpad import Numpad
# from Classes.Stock import Stock
from Classes.AssetTypes.OptionAsset import OptionAsset
from Classes.imports.Transactions import Transactions
from Classes.StockVisualizer import StockVisualizer
from Classes.imports.PieChart import PieChart
from Classes.imports.BarGraph import BarGraph
import math
import datetime
from dateutil import parser

DX = 300# default x
DY = 230# default y
DH = 120# default height
class Portfolio(Menu):
    def __init__(self,stocklist,player,gametime) -> None:
        self.icon = pygame.image.load(r'Assets\Menu_Icons\portfolio.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        self.icon.set_colorkey((255,255,255))
        super().__init__(self.icon)
        # remove all the white from the image
        # self.bar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
        # self.bar.value = 0
        self.quantitybar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))

        self.sharebackground = pygame.image.load(r"Assets\backgrounds\Background (8).png").convert_alpha()
        self.sharebackground = self.sharebackground.subsurface((0,0,485,880))
        self.sharebackground.set_alpha(150)

        self.displayingtext = fontlist[35].render('Displaying ',(220,220,220))[0]
        self.menudrawn = True
        # self.allrenders = []
        self.selected_asset = None
        self.displayedStocks = [StockVisualizer(gametime,stocklist[i],stocklist) for i in range(3)]# the stock visualizers for the stocks that are displayed
        self.networthGraph = StockVisualizer(gametime,player,stocklist)
        self.selectedGraph = StockVisualizer(gametime,stocklist[0],stocklist)
        self.piechart = PieChart(150, (200, 650))
        self.barGraphs = [BarGraph([175,175],[],[],[875,400]),BarGraph([175,175],[],[],[1100,400])]

        # for the asset type selection which sorts the latterscroll
        # self.assetoptions = ["Stocks","Options","Other"]# future, Crypto, bonds, minerals, real estate, etc
        self.assetoptions = ["Stocks","Options","Other"]
        self.displayed_asset_type = ["Stocks","Options","Other"]

        

        self.classtext = {StockAsset:"Share",OptionAsset:"Option"}# Used quite a bit and saves an if statement every time I need class specific text

        # self.latterScrollsurf = pygame.Surface((730,730))
        self.latterscrollnorm = PortfolioLatter()
        self.latterscrollselect = PortfolioLatter()
        self.numpad = Numpad()
        stocknames = [stock.name for stock in stocklist]
        self.stocktext = {name:[] for name in stocknames}# the list has [fullstockname,stockdescription1,stockdescription etc...]
        with open(r'Assets\newstockdes.txt','r') as descriptions:
            filecontents = descriptions.readlines()
            for i,line in enumerate(filecontents):
                for stockname in stocknames:
                    if line.replace('\n','') == stockname:
                        self.stocktext[stockname].append(filecontents[i+1].replace('\n',''))# Full stock name Ex. "Kyronix Solutions Inc. (KSTON)"
                        seperatatedstrings = separate_strings((filecontents[i+2].replace('\n','')),5)
                        for string in seperatatedstrings:# a list containing 4 strings 
                            self.stocktext[stockname].append(string)

        self.renderedstocknames = {name:fontlist[90].render(name,(150,150,150))[0] for name in stocknames}
        for key,lines in self.stocktext.items():#rendering the text that displays info about the stocks
            for i,line in enumerate(lines):
                if i == 0:#if its the first line, render it with a larger font and grey color
                    self.stocktext[key][i] = fontlist[55].render(line,(190, 190, 190))[0]
                else:#else render it with a smaller font and orange color
                    self.stocktext[key][i] = fontlist[35].render(line,(140, 140, 140))[0]
 
        
    def getpoints(self, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]
    

    def draw_assetscroll(self,sortedassets,screen,mousebuttons):
        """Draws the assetscroll"""
        # asset is the class name (the class should have a str method that returns the name of the asset)

        # asset is [class, ogvalue:float, secondary text:str, value:float, percent:float]
        # function to get the text for each asset
        get_text = lambda asset,secondtext : [f'{asset} ',
                                    # f"{limit_digits(asset[2],10,False)} Share{'' if asset[2] == 1 else 's'}",
                                    secondtext,
                                    f'${limit_digits(asset.getValue(),15)}',]
        # getting the text for each asset
        textlist = [get_text(asset,secondtext) for [asset,secondtext] in sortedassets]# stores 3 texts for each asset in the sortedassets list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(25,60)] for i in range(len(textlist))]
        # loop through the textlist and store the text info in the textinfo list
        for i,(text,[asset,secondtext]) in enumerate(zip(textlist,sortedassets)):
            polytexts = []# temporary list to store the text info for each asset
            polytexts.append([text[0],50,asset.color])
            polytexts.append([text[1],35,(190,190,190)])
            polytexts.append([text[2],60,(190,190,190)])
            textinfo.append(polytexts)
            coords[i].append(((text[1],100),30))

        self.latterscrollnorm.storetextinfo(textinfo)# simply changes the self.texts in latterscroll
        self.latterscrollnorm.set_textcoords(coords)# simply changes the self.textcoords in latterscroll
        # Does most of the work for the latter scroll, renders the text and finds all the coords
        scrollmaxcoords = (535,960)
        ommitted = self.latterscrollnorm.store_rendercoords((855, 200), scrollmaxcoords,135,0,0,updatefreq=60)

        # drawing the latter scroll and assigning the selected asset
        selectedindex = None if self.selected_asset == None else sortedassets.index(self.selected_asset)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        newselected = self.latterscrollnorm.draw_polys(screen, (855, 200), scrollmaxcoords, mousebuttons, selectedindex, True, *[sasset[0].getPercent() for sasset in sortedassets[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        if newselected == None:
            self.selected_asset = None
        else:# if the selected asset is not None
            self.selected_asset = sortedassets[newselected]

        # make a text saying displaying # out of # assets
        screen.blit(self.displayingtext,(1025,105))
        currenttext = s_render(f'{ommitted[0]} - {ommitted[1]-1}',35,(220,220,220))
        outoftext = s_render(f' out of {len(sortedassets)}',35,(220,220,220))

        screen.blit(currenttext,(1025+self.displayingtext.get_width(),105))

        screen.blit(outoftext,(1025+self.displayingtext.get_width()+currenttext.get_width(),105))

    def assetscroll_controls(self,screen,mousebuttons):
        """Controls for the asset scroll"""
        screen.blit(s_render("My Assets", 45, (210, 210, 210)), (880, 100))
        
        width = 500//len(self.assetoptions)
        for i,option in enumerate(self.assetoptions):
            x,y = 880+(i*width),160
            rect = pygame.Rect(x,y,width-5,35)
            color = (120,120,120)
            if rect.collidepoint(pygame.mouse.get_pos()):
                color = (160,160,160)
                if mousebuttons == 1:
                    soundEffects['clickbutton2'].play()
                    if option in self.displayed_asset_type:
                        self.displayed_asset_type.remove(option)
                    else:
                        self.displayed_asset_type.append(option)
                    self.selected_asset = None

            pygame.draw.rect(screen, color, rect, width=3,border_radius=10)
            pygame.draw.rect(screen, (0,0,0), [x+10,y+10,15,15], 3)
            # rectangle inside the one above
            if option in self.displayed_asset_type:
                pygame.draw.rect(screen, (200,200,200), [x+13,y+13,9,9])
            screen.blit(s_render(option, 30, (210, 210, 210)), (x+34,y+8))

    def get_allassets(self,player) -> list:
        """returns a sorted list of the currently displayed assets of the player"""
        def get_second(asset):
            text = self.classtext[type(asset)]
            return f"{asset.quantity} {text}{'' if asset.quantity == 1 else 's'}"
            
        # asset is [class, ogvalue:float, quantity:int, secondary text:str, value:float, percent:float]
        # asset is [class, secondarytext]
            
        stockassets,optionassets = [],[]
        if "Stocks" in self.displayed_asset_type: stockassets = [[stock, get_second(stock)] for stock in player.stocks]# gets the stock assets
        if "Options" in self.displayed_asset_type: optionassets = [[option, get_second(option)] for option in player.options]# gets the option assets

        allassets = stockassets + optionassets 
        # sortedstocks = sorted(player.stocks,key=lambda stock: stock[0].price*stock[2],reverse=True)
        return sorted(allassets,key=lambda asset: asset[0].getValue(),reverse=True)
    
    def drawselectedScroll(self,screen,asset,mousebuttons):
        """Draws the selected asset scroll"""
        asset,secondtext = asset
        
        text = [f'{asset} ',secondtext,f'${limit_digits(asset.getValue(),15)}',f'{"+" if asset.getPercent() > 0 else ""}{limit_digits(asset.getPercent(),15)}%']
        polytexts = []# temporary list to store the text info for each asset
        polytexts.append([text[0],50,asset.color])
        polytexts.append([text[1],35,(190,190,190)])
        polytexts.append([text[2],60,(190,190,190)])
        color = ((190,0,0) if asset.getPercent() < 0 else (0,190,0)) if asset.getPercent() != 0 else (190,190,190)
        polytexts.append([text[3],60,color])
        textinfo = [polytexts]
        coords = [[(20,15),(25,60),((text[1],100),30),((text[1],text[2],150),30)]]

        self.latterscrollselect.storetextinfo(textinfo)# simply changes the self.texts in latterscroll
        self.latterscrollselect.set_textcoords(coords)# simply changes the self.textcoords in latterscroll
        # Does most of the work for the latter scroll, renders the text and finds all the coords
        scrollmaxcoords = (770,335)
        self.latterscrollselect.store_rendercoords((855, 200), scrollmaxcoords,135,0,0)
        # drawing the latter scroll and assigning the selected asset
        newselected = self.latterscrollselect.draw_polys(screen, (875, 200), scrollmaxcoords, mousebuttons, 0, True, *[asset.getPercent()])# draws the latter scroll and returns the selected asset
        if newselected == None:
            self.selected_asset = None
        
    def draw_selected_description(self,screen,asset,mousebuttons,player,gametime):
        """Draws the description of the selected asset"""
        asset,secondtext= asset

        mousex, mousey = pygame.mouse.get_pos()

        color = (200,200,200)
        if pygame.Rect(1450,115,300,50).collidepoint(mousex,mousey):
            color = (200,10,10)
            if pygame.mouse.get_pressed()[0]:
                self.selected_asset = None
        screen.blit(s_render("Deselect Asset", 70, color), (1450, 115))

        # Draws the description about the stock on the left side of the screen
        points = [(200, 605), (850, 605), (850, 960), (200, 960)]
        # gfxdraw.filled_polygon(screen, points, (30, 30, 30))
        # pygame.draw.polygon(screen, (0, 0, 0), points, 5)

        # NEED TO REIMPLEMENT THE ASSET ANALYTICS
        self.drawAssetInfo(screen,asset,gametime,player)# draws the Asset Analytics underneath the stock graph on the left side of the screen

        # draws the information about the stock in the middle of the screen
        points = [(860, 330), (1620, 330), (1620, 960), (860, 960)]
        pygame.draw.polygon(screen, (0, 0, 0), points, 5)

        # draws the calculator
        extratext = self.classtext[type(asset)].upper()
        
        self.numpad.draw(screen,(200,610),(275,350),extratext,mousebuttons,asset.quantity)
        # self.numpad.draw(screen,(870,620),(300,330),extratext,mousebuttons,asset.quantity)
        
        for i,graphname in enumerate(asset.stockobj.graphrangeoptions):# 1H, 1D, etc...
            # asset.stockobj.baredraw(screen,(1630,200+(i*125)),(270,115),graphname)# draws the graph on the right side of the screen
            self.selectedGraph.drawBare(screen,(1630,200+(i*125)),(270,115),graphname,True,"None")
            text = s_render(graphname, 40, (230, 230, 230))
            screen.blit(text, (1640, 325+(i*125)-text.get_height()-20))

        # color = ((200,0,0) if asset.getPercent() < 0 else (0,200,0)) if asset.getPercent() != 0 else (200,200,200)
        quantity = self.numpad.get_value()# gets the quantity from the numpad
        netgl = (asset.getValue(bypass=True,fullvalue=False) - asset.ogvalue)*quantity# net gain/loss
        taxedamt = 0 if netgl <= 0 else netgl*player.taxrate# the amount taxed
        percent = asset.getPercent()
        # descriptions = [s_render("Net Gain" if asset.getPercent() > 0 else "Net Loss", 25, (230,230,230)),
        descriptions = [s_render(p3choice("Net Loss","Net Gain", "",percent), 25, (230,230,230)),
            s_render(f"Taxes ({player.taxrate*100}%)", 25, (230, 230, 230)),
            s_render("Final Value (After Tax)", 25, (230, 230, 230)),]
        
        texts = [s_render(f"${limit_digits(netgl,10)}", 70, p3choice((200, 0, 0),(0,200,0),(200,200,200),percent)),
            s_render(f"-${limit_digits(abs(taxedamt),10)}", 70, p3choice((200, 0, 0),(0,0,0),(90,90,90),-taxedamt)),
            s_render(f"${limit_digits((asset.getValue(fullvalue=False)*quantity)-taxedamt,15)}", 70, (190, 190, 190)),]
        
        
        if self.drawSellingInfo(screen,descriptions,texts,mousebuttons,quantity):# if the asset should be sold, and drawing the selling info
            asset.sell(player,quantity)
            self.selected_asset = None
        # need to fix teh option.add method - when you add the og value doesn't change
        
    def drawAssetInfo(self,screen,asset,gametime,player):
        def getYearlyReturn(asset,gametime):
            """returns the yearly return of the asset"""
            diff = gametime.time-asset.dateobj
            if diff.days <= 365: return asset.getPercent()
            extra = 100 if asset.getPercent() > 0 else -100
            percent = abs(asset.getPercent()); days = 1/(diff.days/365)
            return (((1+(percent/100)) ** days)-1) * extra
        
    #     # coords = [
    #     #     (880,345),# Per Share
    #     #     (880,380),# Per share #
    #     #     # ()
    #     #     (880,440),
    #     # ]
    #     # [(860, 330), (1620, 330), (1620, 960), (860, 960)]
    #     # 860-1620 = 760
    #     # 760/3 = 253.33333333333334
    #     # 890+253.33333333333334 = 1143.3333333333333
    #     # 1143.3333333333333+253.33333333333334 = 1396.6666666666667
    #     # 1396.6666666666667+253.33333333333334 = 1650
        if isinstance(asset,StockAsset):
            otherTexts = ("Dividends",[f"${limit_digits(asset.totalDividends,15)}",""])
        elif isinstance(asset,OptionAsset):
            otherTexts = ("Expiration & Strike",[f"{asset.expiration_date} Days",f"${asset.strikePrice}"])
                
    #     texts = [
    #         "Per Share",
    #         "Total Cost",
    #         otherTexts[0]
    #     ]
    #     values = [
    #         [f"${limit_digits(asset.ogvalue,12)}", f"${limit_digits(asset.getValue(fullvalue=False),12)}"],# Per Share (OG Value, Current Value)
    #         [f"${limit_digits(asset.ogvalue*asset.quantity,12)}", f"${limit_digits(asset.getValue(fullvalue=False)*asset.quantity,12)}"],# Total Cost (OG Value, Current Value)
    #         otherTexts[1]
    #     ]
    #     for i in range(3):
    #         points = [(880+(i*250), 385), (1133+(i*235), 385), (1133+(i*235), 530), (880+(i*250), 530)]

    #         # pygame.draw.polygon(screen, (0, 0, 0), points, 5)
    #         pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(880+(i*250), 385, 253, 145), 5, 10)
            
    #         x,y = 890+(i*253),390
    #         screen.blit(s_render(texts[i], 40, (190, 190, 190)), (x, y-40))# the text describing the values in the boxes (Per Share, Total Cost, etc...)
    #         screen.blit(s_render(values[i][0], 50, (190, 190, 190)), (x, y))# the value of the variable (Per Share, Total Cost, etc...)
    #         screen.blit(s_render(values[i][1], 50, (190, 190, 190)), (x, y+50))# the value of the variable (Per Share, Total Cost, etc...)
        


    #     screen.blit(s_render(f"Purchased on {asset.date}", 40, (190, 190, 190)), (880, 540))
        # def drawAssetInfo(self,screen,asset,gametime,player):
        ogtext = s_render("Original", 55, (190, 190, 190))
        screen.blit(ogtext, (885, 350))
        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(900+ogtext.get_width(), 350, 35, 35), 0, 10)

        screen.blit(s_render("Current", 55, asset.color), (1140, 350))
        pygame.draw.rect(screen, asset.color, pygame.Rect(1155+ogtext.get_width(), 350, 35, 35), 0, 10)

        
        self.barGraphs[0].updateValues([asset.ogvalue,asset.getValue(fullvalue=False)],[(110,110,110),asset.color])# bar graph 1 with the original value and the current value
        self.barGraphs[1].updateValues([asset.ogvalue*asset.quantity,asset.getValue(fullvalue=True)],[(110,110,110),asset.color])# bar graph 2 with the original value and the current value
        for graph in self.barGraphs:
            
            graph.draw(screen)
        # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(870, 340, 740, 250), 5, 10)

        # movingRect(screen,getYearlyReturn(asset,gametime),35,740,100,870,600)
        # movingRect(screen,(asset.getValue()/player.getNetworth())*100,35,740,100,870,740)



        # offset = 1 if abs(x:=(getYearlyReturn(asset,gametime))) >= 25 else abs(x/25)
        # colorval = (120*offset)+70
        # color = p3choice((colorval,0,0),(0,colorval,0),(190,190,190),float(getYearlyReturn(asset,gametime)))

        # if x < 0:
        #     # print(x,offset,1240-(offset*740), 740*offset)
        #     pygame.draw.rect(screen, color, pygame.Rect(1240-(offset*340), 600, 340*offset, 100),border_bottom_left_radius=25,border_top_left_radius=25)
        # else:
        #     pygame.draw.rect(screen, color, pygame.Rect(1240, 600, 340*offset, 100),border_bottom_right_radius=25,border_top_right_radius=25)
        #     # avgrtrnRect = pygame.Rect(1240, 600, 340*offset, 100)
        
       
        
        # pygame.draw.rect(screen, (0,0,0), pygame.Rect(870,595,740,110), width=7, border_radius=10)
        # pygame.draw.rect(screen, (0,0,0), avgrtrnRect)



        


    # def drawAssetInfo(self,screen,asset,gametime,player):
    #     """Draws the Asset Analytics underneath the stock graph on the left side of the screen"""
    #     descriptexts = [# the descriptions for all the text that will be displayed
    #         s_render(f"Per {self.classtext[type(asset)]}", 40, (190, 190, 190)),
    #         s_render("Total Cost", 40, (190, 190, 190)),
    #         s_render("Avg Return", 25, (190, 190, 190)),
    #         s_render(f"Percent of Portfolio", 25, (190, 190, 190))]
    #     # All the values that will be displayed
        # def getYearlyReturn(asset,gametime):
        #     """returns the yearly return of the asset"""
        #     diff = gametime.time-asset.dateobj
        #     if diff.days <= 365:
        #         return asset.getPercent()
        #     extra = 100 if asset.getPercent() > 0 else -100
        #     percent = abs(asset.getPercent())
        #     days = 1/(diff.days/365)
        #     num = (((1+(percent/100)) ** days)-1) * extra
        #     if len(f"{num:,.4f}".format(num)) > 12:
        #         return "{:,.2e}".format(num)    
        #     else:
        #         return f"{num:,.4f}"
        
    #     getCorrrectSize = lambda strlen: int(-85*math.log10(strlen))+155
        # valstrings = [# the strings that will be displayed
        #     f"${limit_digits(asset.ogvalue,12)}",
        #     f"${limit_digits(asset.ogvalue*asset.quantity,12)}",
        #     f"{getYearlyReturn(asset,gametime)}%",
        #     f"{limit_digits((asset.getValue()/player.getNetworth())*100,12)}%"]
        # # colors = [(190, 0, 0) if getYearlyReturn(asset,gametime) < 0 else (0, 190, 0),(190, 190, 190)]
        # colors = [p3choice((190,0,0),(0,190,0),(190,190,190),float(getYearlyReturn(asset,gametime))),(190, 190, 190)]

    #     if isinstance(asset,OptionAsset):
    #         descriptexts.append(s_render("Expiration", 25, (190, 190, 190)))
    #         valstrings.append(f"{asset.expiration_date} Days")
    #         colors.append((190,0,0) if asset.expiration_date < 5 else (190,190,190))
    #     elif isinstance(asset,StockAsset):
    #         descriptexts.append(s_render("Dividends Received", 25, (190, 190, 190)))
    #         valstrings.append(f"${limit_digits(asset.totalDividends,15)}")
    #         colors.append((190,190,190) if asset.totalDividends == 0 else (0,190,0))
            
        
    #     valueTexts = [s_render(valstrings[i], getCorrrectSize(len(valstrings[i])), (190, 190, 190)) for i in range(2)]# adds the top row (per share and total cost)
        
    #     valueTexts += [s_render(valstrings[i], 50, colors[i-2]) for i in range(2,5)]# adds values below the top row (avg return, etc...)
        
    #     # top rows (the OG value of the share and the total)
    #     for i in range(2):
    #         valueText = valueTexts[i]# the value of the variable 
    #         screen.blit(valueText, (205+(i*320)+(315-valueText.get_width())/2, 670+(100-valueText.get_height())/2))
    #         screen.blit(descriptexts[i], (205+(i*320)+(315-descriptexts[i].get_width())/2, 773))# the text describing the variable
    #         pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(205+(i*320), 665, 315, 145), 5,10)# the border of the variable
    #     # bottom rows (the avg return, etc...)
    #     for i in range(2,5):
    #         valueText = valueTexts[i]
    #         screen.blit(valueText, (205+((i-2)*213)+(210-valueText.get_width())/2, 835))
    #         screen.blit(descriptexts[i], (205+((i-2)*213)+(210-descriptexts[i].get_width())/2, 885))
    #         pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(205+((i-2)*213), 815, 210, 95), 5,10)
        
    #     anatext, datetext = s_render(f"Original Asset Analytics", 55, (190, 190, 190)), s_render(f"{asset.date}", 45, (190, 190, 190))
    #     screen.blit(anatext, (205+(650-anatext.get_width())/2, 610))
    #     screen.blit(datetext, (210+(650-datetext.get_width())/2, 918))# blits the date of the asset


    def drawSellingInfo(self,screen,descriptions,values,mousebuttons,quantity) -> bool:
        """Draws the selling info above the trade asset button and the button itself"""
        mousex, mousey = pygame.mouse.get_pos()

        for i,(dtxt,vtxt) in enumerate(zip(descriptions,values)):
            screen.blit(dtxt,(485,615+(i*85)))
            screen.blit(vtxt,(495,640+(i*85))) 
            # screen.blit(dtxt,(1180,620+(i*85)))
            # screen.blit(vtxt,(1190,645+(i*85))) 

        # rect = pygame.Rect(1180, 590, 425, 70)
        rect = pygame.Rect(485, 875, 325, 70)
        # rect = pygame.Rect(1180, 875, 425, 75)
        pygame.draw.rect(screen, (0, 0, 0), rect, 5,border_radius=10)
        color = (190,190,190)
        if rect.collidepoint(mousex,mousey):
            color = (0,190,0)
            if mousebuttons == 1 and quantity > 0:# if the asset should be sold
                return True
        screen.blit(s_render("TRADE ASSET", 65, color), (535, 887))
        # screen.blit(s_render("TRADE ASSET", 65, color), (1275, 600))
        # screen.blit(s_render("TRADE ASSET", 65, color), (1275, 890))
        return False    

    def drawStockGraphs(self,screen,stocklist,mousebuttons):
        """Draws the stock graphs on the right side of the screen"""
        wh = (500,285)
        for i,stock in enumerate(self.displayedStocks):
            # 870/3 = 290
            # if stock.draw(screen,stock,(1400,200+(i*255)),(500,245),mousebuttons,0,rangecontroldisp=False,graphrange="1D") and mousebuttons == 1:# if the stock name is clicked
            coords = (1400,100+(i*290))
            stock.drawFull(screen,coords,wh,f"PortfolioExtra{i}",True,"hoverName")

        

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player, gametime):
        """Draws all of the things in the portfolio menu"""
        mousex, mousey = pygame.mouse.get_pos()
        
        sortedassets = self.get_allassets(player)# gets the sorted assets of the player
        if self.selected_asset != None and self.selected_asset not in sortedassets:# if the selected asset is not in the sorted assets
            if len(sortedassets) > 0:# if there are assets
                self.selected_asset = sortedassets[0]# set the selected asset to the first asset in the sorted assets
            else:# if there are no assets
                self.selected_asset = None# set the selected asset to None

        
        if self.selected_asset == None:# if the selected asset is None
            # player.draw(screen,player,(200,100),(650,500),mousebuttons,gametime)
            # player.drawFull(screen,(200,100),(650,500),"Portfolio Networth",True,"Normal")
            self.networthGraph.drawFull(screen,(200,100),(650,500),"Portfolio Networth",True,"Normal")

            if len(sortedassets) > 0:
                # draws the stocks on the right of the screen
                self.draw_assetscroll(sortedassets,screen,mousebuttons)

            # Pie chart
            # values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
            values = [(stock.getValue(),stock.name) for stock in player.stocks]
            names = set([stock.name for stock in player.stocks])

            values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]
            values.append([player.cash, "Cash",player.color])
            for option in player.options:
                values.append([option.getValue(),option.name,option.color])

            self.piechart.updateData(values)
            self.piechart.draw(screen)
            # draw_pie_chart(screen, values, 150,(200, 650))  
            
            self.drawStockGraphs(screen,stocklist,mousebuttons)# draws the stock graphs on the right side of the screen
            # for stock in self.displayedStocks:
            #     stock.draw(screen,player,(1400,stock.y),(500,245),mousebuttons,gametime,rangecontroldisp=False,graphrange="1D")
                
            # stocklist[0].draw(screen,player,(1400,200),(500,245),mousebuttons,gametime,rangecontroldisp=False,graphrange="1D")
            # stocklist[1].draw(screen,player,(1400,455),(500,245),mousebuttons,gametime,rangecontroldisp=False,graphrange="1D")
            # stocklist[2].draw(screen,player,(1400,710),(500,245),mousebuttons,gametime,rangecontroldisp=False,graphrange="1D")
            # self.transact.draw(screen,mousebuttons,(1400,105),(500,960),(500,1

        
        else:# if the selected asset is NOT None
            # stockgraph = self.selected_asset[0].stockobj
            self.selectedGraph.setStockObj(self.selected_asset[0].stockobj)

            # stockgraph.draw(screen,player,(200,100),(650,500),mousebuttons,gametime)# draws the selected stock graph on the left
            # stockgraph.drawFull(screen,(200,100),(650,500),f"Main Portfolio",True,"Normal")# draws the selected stock graph on the left
            self.selectedGraph.drawFull(screen,(200,100),(650,500),f"Main Portfolio",True,"Normal")# draws the selected stock graph on the left

            selectedindex = sortedassets.index(self.selected_asset)
            self.drawselectedScroll(screen,sortedassets[selectedindex],mousebuttons)# draws the selected asset scroll on the right

            self.draw_selected_description(screen,sortedassets[selectedindex],mousebuttons,player,gametime)# draws the description of the selected asset
        self.assetscroll_controls(screen,mousebuttons)

        
