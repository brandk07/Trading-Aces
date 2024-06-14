import pygame
import timeit

import pygame.draw_py
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
    def __init__(s,stocklist,player,gametime,totalmarket,menuList) -> None:
        s.icon = pygame.image.load(r'Assets\Menu_Icons\portfolio.png').convert_alpha()
        s.icon = pygame.transform.scale(s.icon,(140,100))
        s.icon.set_colorkey((255,255,255))
        super().__init__(s.icon)
        # remove all the white from the image
        # s.bar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
        # s.bar.value = 0
        s.quantitybar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
        s.totalmarket = totalmarket

        s.sharebackground = pygame.image.load(r"Assets\backgrounds\Background (8).png").convert_alpha()
        s.sharebackground = s.sharebackground.subsurface((0,0,485,880))
        s.sharebackground.set_alpha(150)

        s.displayingtext = fontlist[35].render('Displaying ',(220,220,220))[0]
        s.menudrawn = True
        # s.allrenders = []
        s.selectedAsset = None
        s.player = player
        s.displayedStocks = [StockVisualizer(gametime,stocklist[i],stocklist) for i in range(3)]# the stock visualizers for the stocks that are displayed
        s.networthGraph = StockVisualizer(gametime,player,stocklist)
        s.selectedGraph = StockVisualizer(gametime,stocklist[0],stocklist)
        s.piechart = PieChart(150, (200, 650),menuList)
        s.barGraphs = [BarGraph("Value",[175,175],[875,400]),BarGraph("Allocation",[175,175],[1150,400])]

        # for the asset type selection which sorts the latterscroll
        # s.assetoptions = ["Stocks","Options","Other"]# future, Crypto, bonds, minerals, real estate, etc
        s.assetoptions = ["Stocks","Options","Other"]
        s.displayed_asset_type = ["Stocks","Options","Other"]

        

        s.classtext = {StockAsset:"Share",OptionAsset:"Option"}# Used quite a bit and saves an if statement every time I need class specific text

        # s.latterScrollsurf = pygame.Surface((730,730))
        s.latterscrollnorm = PortfolioLatter()
        s.latterscrollselect = PortfolioLatter()
        s.numpad = Numpad()
        stocknames = [stock.name for stock in stocklist]
        s.stocktext = {name:[] for name in stocknames}# the list has [fullstockname,stockdescription1,stockdescription etc...]
        with open(r'Assets\newstockdes.txt','r') as descriptions:
            filecontents = descriptions.readlines()
            for i,line in enumerate(filecontents):
                for stockname in stocknames:
                    if line.replace('\n','') == stockname:
                        s.stocktext[stockname].append(filecontents[i+1].replace('\n',''))# Full stock name Ex. "Kyronix Solutions Inc. (KSTON)"
                        seperatatedstrings = separate_strings((filecontents[i+2].replace('\n','')),5)
                        for string in seperatatedstrings:# a list containing 4 strings 
                            s.stocktext[stockname].append(string)

        s.renderedstocknames = {name:fontlist[90].render(name,(150,150,150))[0] for name in stocknames}
        for key,lines in s.stocktext.items():#rendering the text that displays info about the stocks
            for i,line in enumerate(lines):
                if i == 0:#if its the first line, render it with a larger font and grey color
                    s.stocktext[key][i] = fontlist[55].render(line,(190, 190, 190))[0]
                else:#else render it with a smaller font and orange color
                    s.stocktext[key][i] = fontlist[35].render(line,(140, 140, 140))[0]
 
        
    def getpoints(s, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]
    

    def draw_assetscroll(s,sortedassets,screen,mousebuttons):
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

        s.latterscrollnorm.storetextinfo(textinfo)# simply changes the s.texts in latterscroll
        s.latterscrollnorm.set_textcoords(coords)# simply changes the s.textcoords in latterscroll
        # Does most of the work for the latter scroll, renders the text and finds all the coords
        scrollmaxcoords = (535,960)
        ommitted = s.latterscrollnorm.store_rendercoords((855, 200), scrollmaxcoords,135,0,0,updatefreq=60)

        # drawing the latter scroll and assigning the selected asset
        selectedindex = None if s.selectedAsset == None else sortedassets.index(s.selectedAsset)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        newselected = s.latterscrollnorm.draw_polys(screen, (855, 200), scrollmaxcoords, mousebuttons, selectedindex, True, *[sasset[0].getPercent() for sasset in sortedassets[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        if newselected == None:
            s.selectedAsset = None
        else:# if the selected asset is not None
            s.selectedAsset = sortedassets[newselected]

        # make a text saying displaying # out of # assets
        screen.blit(s.displayingtext,(1025,105))
        currenttext = s_render(f'{ommitted[0]} - {ommitted[1]-1}',35,(220,220,220))
        outoftext = s_render(f' out of {len(sortedassets)}',35,(220,220,220))

        screen.blit(currenttext,(1025+s.displayingtext.get_width(),105))

        screen.blit(outoftext,(1025+s.displayingtext.get_width()+currenttext.get_width(),105))

    def assetscroll_controls(s,screen,mousebuttons):
        """Controls for the asset scroll"""
        screen.blit(s_render("My Assets", 45, (210, 210, 210)), (880, 100))
        result = checkboxOptions(screen,s.assetoptions,s.displayed_asset_type,500,35,(880,160),mousebuttons)
        if result != None:
            if result[0] in s.displayed_asset_type:
                s.displayed_asset_type.remove(result[0])
            else:
                s.displayed_asset_type.append(result[0])
            s.selectedAsset = None
        # width = 500//len(s.assetoptions)
        # for i,option in enumerate(s.assetoptions):
        #     x,y = 880+(i*width),160
        #     rect = pygame.Rect(x,y,width-5,35)
        #     color = (120,120,120)
        #     if rect.collidepoint(pygame.mouse.get_pos()):
        #         color = (160,160,160)
        #         pygame.draw.rect(screen, color, rect, width=3,border_radius=10)
        #         if mousebuttons == 1:
        #             soundEffects['clickbutton2'].play()
                    # if option in s.displayed_asset_type:
                    #     s.displayed_asset_type.remove(option)
                    # else:
                    #     s.displayed_asset_type.append(option)
                    # s.selectedAsset = None

            
        #     pygame.draw.rect(screen, (0,0,0), [x+10,y+10,15,15], 3)
        #     # rectangle inside the one above
        #     if option in s.displayed_asset_type:
        #         pygame.draw.rect(screen, color, rect, width=3,border_radius=10)
        #         pygame.draw.rect(screen, (200,200,200), [x+13,y+13,9,9])
        #     screen.blit(s_render(option, 30, (210, 210, 210)), (x+34,y+8))

    def get_allassets(s) -> list:
        """returns a sorted list of the currently displayed assets of the player"""
        def get_second(asset):
            text = s.classtext[type(asset)]
            return f"{asset.quantity} {text}{'' if asset.quantity == 1 else 's'}"
            
        # asset is [class, secondarytext]
        # stockassets,optionassets = [],[]
        # if "Stocks" in s.displayed_asset_type: stockassets = [[stock, get_second(stock)] for stock in s.player.stocks]# gets the stock assets
        # if "Options" in s.displayed_asset_type: optionassets = [[option, get_second(option)] for option in s.player.options]# gets the option assets
        nameDict = {StockAsset:"Stocks",OptionAsset:"Options"}
        allassets = s.player.getAssets()# gets all the assets
        allassets = [[asset, get_second(asset)] for asset in allassets if nameDict.get(type(asset)) in s.displayed_asset_type]# gets the assets that are in the displayed asset type
        # sortedstocks = sorted(player.stocks,key=lambda stock: stock[0].price*stock[2],reverse=True)
        return sorted(allassets,key=lambda asset: asset[0].getValue(),reverse=True)
    
    def findAsset(s,value,name):
        """Finds the asset with the name and value"""
        for asset in s.get_allassets():
            if asset[0].getValue() == value and asset[0].name == name:
                return asset
        return None
    def drawselectedScroll(s,screen,asset,mousebuttons):
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

        s.latterscrollselect.storetextinfo(textinfo)# simply changes the s.texts in latterscroll
        s.latterscrollselect.set_textcoords(coords)# simply changes the s.textcoords in latterscroll
        # Does most of the work for the latter scroll, renders the text and finds all the coords
        scrollmaxcoords = (770,335)
        s.latterscrollselect.store_rendercoords((855, 200), scrollmaxcoords,135,0,0)
        # drawing the latter scroll and assigning the selected asset
        newselected = s.latterscrollselect.draw_polys(screen, (875, 200), scrollmaxcoords, mousebuttons, 0, True, *[asset.getPercent()])# draws the latter scroll and returns the selected asset
        if newselected == None:
            s.selectedAsset = None
        
    def draw_selected_description(s,screen,asset,mousebuttons,player,gametime):
        """Draws the description of the selected asset"""
        asset,secondtext= asset

        mousex, mousey = pygame.mouse.get_pos()

        color = (200,200,200)
        if pygame.Rect(1450,115,300,50).collidepoint(mousex,mousey):
            color = (200,10,10)
            if pygame.mouse.get_pressed()[0]:
                s.selectedAsset = None
        screen.blit(s_render("Deselect Asset", 70, color), (1450, 115))

        # Draws the description about the stock on the left side of the screen
        points = [(200, 605), (850, 605), (850, 960), (200, 960)]
        # gfxdraw.filled_polygon(screen, points, (30, 30, 30))
        # pygame.draw.polygon(screen, (0, 0, 0), points, 5)

        # NEED TO REIMPLEMENT THE ASSET ANALYTICS
        s.drawAssetInfo(screen,asset,gametime,player)# draws the Asset Analytics underneath the stock graph on the left side of the screen

        # draws the information about the stock in the middle of the screen
        points = [(860, 330), (1620, 330), (1620, 960), (860, 960)]
        pygame.draw.polygon(screen, (0, 0, 0), points, 5)

        # draws the calculator
        extratext = s.classtext[type(asset)].upper()
        
        s.numpad.draw(screen,(200,610),(275,350),extratext,mousebuttons,asset.quantity)
        # s.numpad.draw(screen,(870,620),(300,330),extratext,mousebuttons,asset.quantity)
        
        for i,graphname in enumerate(asset.stockobj.graphrangeoptions):# 1H, 1D, etc...
            # asset.stockobj.baredraw(screen,(1630,200+(i*125)),(270,115),graphname)# draws the graph on the right side of the screen
            s.selectedGraph.drawBare(screen,(1630,200+(i*125)),(270,115),graphname,True,"None")
            text = s_render(graphname, 40, (230, 230, 230))
            screen.blit(text, (1640, 325+(i*125)-text.get_height()-20))

        # color = ((200,0,0) if asset.getPercent() < 0 else (0,200,0)) if asset.getPercent() != 0 else (200,200,200)
        quantity = s.numpad.getValue()# gets the quantity from the numpad
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
        
        
        if s.drawSellingInfo(screen,descriptions,texts,mousebuttons,quantity):# if the asset should be sold, and drawing the selling info
            asset.sell(player,quantity)
            s.selectedAsset = None
        # need to fix teh option.add method - when you add the og value doesn't change
        
    def drawAssetInfo(s,screen,asset,gametime,player):
        
        
    #     # [(860, 330), (1620, 330), (1620, 960), (860, 960)]
    #     # 860-1620 = 760
    #     # 760/3 = 253.33333333333334
    #     # 890+253.33333333333334 = 1143.3333333333333
    #     # 1143.3333333333333+253.33333333333334 = 1396.6666666666667
    #     # 1396.6666666666667+253.33333333333334 = 1650
        # if isinstance(asset,StockAsset):
        #     otherTexts = ("Dividends",[f"${limit_digits(asset.dividends,15)}",""])
        # elif isinstance(asset,OptionAsset):
        #     otherTexts = ("Expiration & Strike",[f"{asset.expiration_date} Days",f"${asset.strikePrice}"])
                
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
        
        
        # descriptexts = [# the descriptions for all the text that will be displayed
        # s_render(f"Per {s.classtext[type(asset)]}", 40, (190, 190, 190)),
        # s_render("Total Cost", 40, (190, 190, 190)),
        # s_render("Avg Return", 25, (190, 190, 190)),
        # s_render(f"Percent of Portfolio", 25, (190, 190, 190))]



        # screen.blit(s_render(f"Purchased on {asset.date}", 40, (190, 190, 190)), (880, 540))
        # def drawAssetInfo(s,screen,asset,gametime,player):


        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # top part of the asset Info
        ogtext = s_render("Original", 55, (190, 190, 190))
        screen.blit(ogtext, (885, 350))
        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(900+ogtext.get_width(), 350, 35, 35), 0, 10)

        screen.blit(s_render("Current", 55, asset.color), (1140, 350))
        pygame.draw.rect(screen, asset.color, pygame.Rect(1155+ogtext.get_width(), 350, 35, 35), 0, 10)

        
        s.barGraphs[0].updateValues([asset.ogvalue,asset.getValue(fullvalue=False)],[(110,110,110),asset.color],["$","$"])# bar graph 1 with the original value and the current value
        portfolioP = lambda x : x/(player.getNetworth())
        s.barGraphs[1].updateValues([asset.portfolioPercent*100,portfolioP(asset.getValue())*100],[(110,110,110),asset.color],["%","%"])# bar graph 2 with the orignial allocation and the current allocation
        for graph in s.barGraphs:
            graph.draw(screen)

        pygame.gfxdraw.filled_polygon(screen,[# base for the dividend / expiration date
            (1425,400+175-5),
            (1425+175,400+175-5),
            (1425+175,400+175),
            (1425,400+175)],(0,0,0))
        
        if isinstance(asset,StockAsset):
            strValue = f"${limit_digits(asset.dividends,15)}"
            color = (60, 60, 60) if asset.dividends == 0 else (0, 190, 0)
            
        elif isinstance(asset,OptionAsset):
            strValue = f"{asset.daysToExpiration(gametime.time)} Days"
            color = p3choice((160,10,10),(10,160,10),(190,190,190),asset.daysToExpiration(gametime.time)-5)
        
        
        
        valueText = s_render(strValue, 50, (0,0,0))# the value for the dividend / expiration date
        nameText = s_render({StockAsset:"Dividends",OptionAsset:"Expiration"}.get(type(asset)),47,(0,0,0))
        x = 1425+175/2-valueText.get_width()/2; y = 400+175/2-20
        pygame.draw.rect(screen, color, pygame.Rect(1425,y-30,175,valueText.get_height()+60), border_radius=10)
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(1425,y-30,175,valueText.get_height()+60), width=5, border_radius=10)
        screen.blit(valueText,(x,y))# the value for the dividend / expiration date
        x = 1425+175/2-nameText.get_width()/2; y = 400+175+5
        screen.blit(nameText,(x,y))# the name for the dividend / expiration date
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # bottom part of the asset Info 
        # ---------------Left bottom (purchase details)----------------
        def getYearlyReturn(asset,gametime):
            """returns the yearly return of the asset"""
            diff = gametime.time-asset.dateobj
            if diff.days <= 365: return asset.getPercent()
            # extra = 100 if asset.getPercent() > 0 else -100
            # percent = abs(asset.getPercent()); days = 365/diff.days
            # return (((1+(percent/100)) ** days)-1) * extra
            if asset.getPercent() < 0:
                # print(1+((asset.getPercent())/100),365/diff.days,((1+((asset.getPercent())/100))**(365/diff.days)),1-((1+((asset.getPercent())/100))**(365/diff.days)))
                return (1-((1+((asset.getPercent())/100))**(365/diff.days))) * -100
            return (((1+(asset.getPercent()/100))**(365/diff.days))-1) * 100
        
        purchaseDetailsText = s_render(f"Purchase Details", 50, (0, 0, 0))
        screen.blit(purchaseDetailsText, (880, 670))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(870, 710, purchaseDetailsText.get_width()+30, 10))


        screen.blit(s_render(f"DOP : {asset.date}", 40, (190, 190, 190)), (880, 730))
        screen.blit(s_render(f"{(gametime.time-asset.dateobj).days} days ago", 40, (190, 190, 190)), (880, 770))
        yearlyReturn = getYearlyReturn(asset,gametime); eText = "+" if yearlyReturn > 0 else ""
        screen.blit(s_render(f"{eText}{limit_digits(yearlyReturn,15)}% Per Year", 40, (190, 190, 190)), (880, 810))
        percentDiff = asset.getPercent()-s.totalmarket.getPercentDate(asset.dateobj,gametime.time); eText = "+" if percentDiff > 0 else ""
        screen.blit(s_render(f"{eText}{limit_digits(percentDiff,15)}% Vs Market (1Y)", 40, (190, 190, 190)), (880, 850))
        # ---------------Right bottom (Asset Specifics)----------------
        assetSpecificsText = s_render(f"Asset Specifics", 50, (0, 0, 0))
        screen.blit(assetSpecificsText, (1285, 670))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1275, 710, assetSpecificsText.get_width()+30, 10))

        if isinstance(asset,StockAsset):
            dividendYield = (asset.dividends/asset.ogvalue)*100
            screen.blit(s_render(f"Total Dividend Yield : {limit_digits(dividendYield,15)}%", 40, (190, 190, 190)), (1285, 730))

            avgYield = 0 if (gametime.time-asset.dateobj).days == 0 else dividendYield/((gametime.time-asset.dateobj).days/365)
            screen.blit(s_render(f"Avg Dividend Yield : {limit_digits(avgYield,15)}%", 40, (190, 190, 190)), (1285, 770))
            screen.blit(s_render(f"Last Quarter Dividend Yield : N/a", 40, (190,190,190)), (1285, 810))
        elif isinstance(asset,OptionAsset):
            screen.blit(s_render(f"Strike Price : {asset.strikePrice}", 40, (190, 190, 190)), (1285, 730))
            screen.blit(s_render(f"Option Type : {asset.option_type}", 40, (190, 190, 190)), (1285, 770))
            screen.blit(s_render(f"Voliatility : {limit_digits(asset.getVolatility()*100,15)}%", 40, (190, 190, 190)), (1285, 810))
            screen.blit(s_render(f"Exp Date : {asset.getExpDate()}", 40, (190, 190, 190)), (1285, 850))
            
        

        

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



        


    # def drawAssetInfo(s,screen,asset,gametime,player):
    #     """Draws the Asset Analytics underneath the stock graph on the left side of the screen"""
        # descriptexts = [# the descriptions for all the text that will be displayed
        #     s_render(f"Per {s.classtext[type(asset)]}", 40, (190, 190, 190)),
        #     s_render("Total Cost", 40, (190, 190, 190)),
        #     s_render("Avg Return", 25, (190, 190, 190)),
        #     s_render(f"Percent of Portfolio", 25, (190, 190, 190))]
        # # All the values that will be displayed
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
        
        # getCorrrectSize = lambda strlen: int(-85*math.log10(strlen))+155
        # valstrings = [# the strings that will be displayed
        #     f"${limit_digits(asset.ogvalue,12)}",
        #     f"${limit_digits(asset.ogvalue*asset.quantity,12)}",
        #     f"{getYearlyReturn(asset,gametime)}%",
        #     f"{limit_digits((asset.getValue()/player.getNetworth())*100,12)}%"]
        
        # colors = [p3choice((190,0,0),(0,190,0),(190,190,190),float(getYearlyReturn(asset,gametime))),(190, 190, 190)]

    #     if isinstance(asset,OptionAsset):
    #         descriptexts.append(s_render("Expiration", 25, (190, 190, 190)))
    #         valstrings.append(f"{asset.expiration_date} Days")
    #         colors.append((190,0,0) if asset.expiration_date < 5 else (190,190,190))
    #     elif isinstance(asset,StockAsset):
    #         descriptexts.append(s_render("Dividends Received", 25, (190, 190, 190)))
    #         valstrings.append(f"${limit_digits(asset.dividends,15)}")
    #         colors.append((190,190,190) if asset.dividends == 0 else (0,190,0))
            
        
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


    def drawSellingInfo(s,screen,descriptions,values,mousebuttons,quantity) -> bool:
        """Draws the selling info above the trade asset button and the button its"""
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

    def drawStockGraphs(s,screen,stocklist,mousebuttons):
        """Draws the stock graphs on the right side of the screen"""
        wh = (500,285)
        for i,stock in enumerate(s.displayedStocks):
            # 870/3 = 290
            # if stock.draw(screen,stock,(1400,200+(i*255)),(500,245),mousebuttons,0,rangecontroldisp=False,graphrange="1D") and mousebuttons == 1:# if the stock name is clicked
            coords = (1400,100+(i*290))
            stock.drawFull(screen,coords,wh,f"PortfolioExtra{i}",True,"hoverName")

        

    def draw_menu_content(s, screen: pygame.Surface, stocklist: list, mousebuttons: int, player, gametime):
        """Draws all of the things in the portfolio menu"""
        mousex, mousey = pygame.mouse.get_pos()
        
        sortedassets = s.get_allassets()# gets the sorted assets of the player
        screen.blit(s_render(f"{None if s.selectedAsset == None else s.selectedAsset[1]}", 70, (210, 210, 210)), (200, 1000))
        if s.selectedAsset != None and s.selectedAsset not in sortedassets:# if the selected asset is not in the sorted assets
            if len(sortedassets) > 0:# if there are assets
                s.selectedAsset = sortedassets[0]# set the selected asset to the first asset in the sorted assets
            else:# if there are no assets
                s.selectedAsset = None# set the selected asset to None

        
        if s.selectedAsset == None:# if the selected asset is None
            # player.draw(screen,player,(200,100),(650,500),mousebuttons,gametime)
            # player.drawFull(screen,(200,100),(650,500),"Portfolio Networth",True,"Normal")
            s.networthGraph.drawFull(screen,(200,100),(650,500),"Portfolio Networth",True,"Normal")

            if len(sortedassets) > 0:
                # draws the stocks on the right of the screen
                s.draw_assetscroll(sortedassets,screen,mousebuttons)

            # Pie chart
            # values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
            values = [(stock.getValue(),stock.name) for stock in player.stocks]
            names = set([stock.name for stock in player.stocks])

            values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]
            values.append([player.cash, "Cash",player.color])
            for option in player.options:
                values.append([option.getValue(),option.name,option.color])

            s.piechart.updateData(values)
            s.piechart.draw(screen)
            # draw_pie_chart(screen, values, 150,(200, 650))  
            
            s.drawStockGraphs(screen,stocklist,mousebuttons)# draws the stock graphs on the right side of the screen
            # for stock in s.displayedStocks:
            #     stock.draw(screen,player,(1400,stock.y),(500,245),mousebuttons,gametime,rangecontroldisp=False,graphrange="1D")
                
            # stocklist[0].draw(screen,player,(1400,200),(500,245),mousebuttons,gametime,rangecontroldisp=False,graphrange="1D")
            # stocklist[1].draw(screen,player,(1400,455),(500,245),mousebuttons,gametime,rangecontroldisp=False,graphrange="1D")
            # stocklist[2].draw(screen,player,(1400,710),(500,245),mousebuttons,gametime,rangecontroldisp=False,graphrange="1D")
            # s.transact.draw(screen,mousebuttons,(1400,105),(500,960),(500,1

        
        else:# if the selected asset is NOT None
            # stockgraph = s.selectedAsset[0].stockobj
            s.selectedGraph.setStockObj(s.selectedAsset[0].stockobj)

            # stockgraph.draw(screen,player,(200,100),(650,500),mousebuttons,gametime)# draws the selected stock graph on the left
            # stockgraph.drawFull(screen,(200,100),(650,500),f"Main Portfolio",True,"Normal")# draws the selected stock graph on the left
            s.selectedGraph.drawFull(screen,(200,100),(650,500),f"Main Portfolio",True,"Normal")# draws the selected stock graph on the left

            selectedindex = sortedassets.index(s.selectedAsset)
            s.drawselectedScroll(screen,sortedassets[selectedindex],mousebuttons)# draws the selected asset scroll on the right

            s.draw_selected_description(screen,sortedassets[selectedindex],mousebuttons,player,gametime)# draws the description of the selected asset
        s.assetscroll_controls(screen,mousebuttons)

        
