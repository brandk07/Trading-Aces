import pygame
import pygame.draw_py
from Defs import *
from Classes.Menus.Menu import Menu
from Classes.imports.UIElements.Latterscroll import *
from Classes.imports.UIElements.Numpad import Numpad
from Classes.AssetTypes.OptionAsset import OptionAsset
from Classes.imports.StockVisualizer import StockVisualizer
from Classes.imports.UIElements.PieChart import PieChartSideInfo
from Classes.imports.UIElements.BarGraph import BarGraph
from Classes.imports.UIElements.OrderBox import OrderBox
from Classes.imports.UIElements.SelectionElements import SelectionBar

DX = 300# default x
DY = 230# default y
DH = 120# default height
class Portfolio(Menu):
    def __init__(self,stocklist,player,gametime,totalmarket) -> None:
        super().__init__()
        self.totalmarket = totalmarket
   
        self.menudrawn = False
        # self.allrenders = []
        self.selectedAsset = None
        self.player = player
        self.displayedStocks = [StockVisualizer(gametime,stocklist[i],stocklist) for i in range(2)]# the stock visualizers for the stocks that are displayed
        self.networthGraph = StockVisualizer(gametime,player,stocklist)
        self.selectedGraph = StockVisualizer(gametime,stocklist[0],stocklist)
        self.piechart = PieChartSideInfo(150, (200, 650))
        self.barGraphs = [BarGraph("Value",[875,400],[175,175]),BarGraph("Allocation",[1150,400],[175,175])]
        self.orderBox = OrderBox((465,605),(385,370),gametime)
        self.barSelection : SelectionBar = SelectionBar()

        # for the asset type selection which sorts the latterscroll
        # self.assetoptions = ["Stock","Option","Other"]# future, Crypto, bonds, minerals, real estate, etc
        self.assetoptions = ["Stocks","Options","Index"]
        self.displayed_asset_type = ["Stocks","Options","Index"]

        self.classtext = {StockAsset:"Share",OptionAsset:"Option",IndexFundAsset:"Share"}# Used quite a bit and saves an if statement every time I need class specific text

        # self.latterScrollsurf = pygame.Surface((730,730))
        self.latterscrollnorm = PortfolioLatter()
        self.latterscrollselect = PortfolioLatter()
        self.numpad = Numpad()
 
    def setSelectedAsset(self,asset):
        """Sets the selected asset"""
        def get_second(asset):
            text = self.classtext[type(asset)]
            return f"{limit_digits(asset.quantity,20,truncate=True)} {text}{'' if asset.quantity == 1 else 's'}"
        nameDict = {StockAsset:"Stocks",OptionAsset:"Options",IndexFundAsset:"Index"}
        if nameDict[type(asset)] not in self.displayed_asset_type:# Ensures that the asset type is displayed
            self.displayed_asset_type.append(nameDict[type(asset)])
        self.selectedAsset = [asset, get_second(asset)]
    def getpoints(self, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]
    

    def draw_assetscroll(self,sortedassets,screen):
        """Draws the assetscroll"""
        # asset is the class name (the class should have a str method that returns the name of the asset)

        # asset is [class, ogValue:float, secondary text:str, value:float, percent:float]
        # function to get the text for each asset
        get_text = lambda asset,secondtext : [f'{asset} ',
                                    # f"{limit_digits(asset[2],10,False)} Share{'' if asset[2] == 1 else 'self'}",
                                    secondtext,
                                    f'${limit_digits(asset.getValue(),17)}',]
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
        selectedindex = None if self.selectedAsset == None else sortedassets.index(self.selectedAsset)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        newselected = self.latterscrollnorm.draw_polys(screen, (855, 200), scrollmaxcoords, selectedindex, True, *[sasset[0].getPercent() for sasset in sortedassets[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        if newselected == None:
            self.selectedAsset = None
        else:# if the selected asset is not None
            self.selectedAsset = sortedassets[newselected]

        # drawCenterTxt(screen,"Displaying ",35,(220,220,220),(1025,105),centerX=False,centerY=False)
        # currenttext = s_render(f'{ommitted[0]} - {ommitted[1]-1}',35,(220,220,220))
        # outoftext = s_render(f' out of {len(sortedassets)}',35,(220,220,220))

        # screen.blit(currenttext,(1025+self.displayingtext.get_width(),105))

        # screen.blit(outoftext,(1025+self.displayingtext.get_width()+currenttext.get_width(),105))
        totalTxt = "Displaying " + str(ommitted[0]) + " - " + str(ommitted[1]-1) + " out of " + str(len(sortedassets))
        drawCenterTxt(screen,totalTxt,35,(220,220,220),(1025,105),centerX=False,centerY=False)

    def assetscroll_controls(self,screen):
        """Controls for the asset scroll"""

        result = checkboxOptions(screen,self.assetoptions,self.displayed_asset_type,(860,160),(530,35))


        if result != None:
            if result[0] in self.displayed_asset_type:
                self.displayed_asset_type.remove(result[0])
            else:
                self.displayed_asset_type.append(result[0])
            self.selectedAsset = None

    def get_allassets(self) -> list:
        """returns a sorted list of the currently displayed assets of the player"""
        def get_second(asset):
            text = self.classtext[type(asset)]
            return f"{limit_digits(asset.quantity,20,truncate=True)} {text}{'' if asset.quantity == 1 else 's'}"
            
        # asset is [class, secondarytext]
        # stockassets,optionassets = [],[]
        # if "Stocks" in self.displayed_asset_type: stockassets = [[stock, get_second(stock)] for stock in self.player.stocks]# gets the stock assets
        # if "Options" in self.displayed_asset_type: optionassets = [[option, get_second(option)] for option in self.player.options]# gets the option assets
        nameDict = {StockAsset:"Stocks",OptionAsset:"Options",IndexFundAsset:"Index"}
        allassets = self.player.getAssets()# gets all the assets
        allassets = [[asset, get_second(asset)] for asset in allassets if nameDict.get(type(asset)) in self.displayed_asset_type]# gets the assets that are in the displayed asset type
        # sortedstocks = sorted(player.stocks,key=lambda stock: stock[0].price*stock[2],reverse=True)
        return sorted(allassets,key=lambda asset: asset[0].getValue(),reverse=True)
    
    def findAsset(self,value,name):
        """Finds the asset with the name and value"""
        for asset in self.get_allassets():
            if asset[0].getValue() == value and asset[0].name == name:
                return asset
        return None
    def drawselectedScroll(self,screen,asset):
        """Draws the selected asset scroll"""
        asset,secondtext = asset
        
        text = [f'{asset} ',secondtext,f'${limit_digits(asset.getValue(),17)}',f'{"+" if asset.getPercent() > 0 else ""}{limit_digits(asset.getPercent(),17)}%']
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
        newselected = self.latterscrollselect.draw_polys(screen, (875, 200), scrollmaxcoords, 0, True, *[asset.getPercent()])# draws the latter scroll and returns the selected asset
        if newselected == None:
            self.selectedAsset = None
        
    def draw_selected_description(self,screen,asset,player,gametime):
        """Draws the description of the selected asset"""
        asset,secondtext= asset

        mousex, mousey = pygame.mouse.get_pos()

        color = (200,200,200)
        if pygame.Rect(1450,115,300,50).collidepoint(mousex,mousey):
            color = (200,10,10)
            if pygame.mouse.get_pressed()[0]:
                self.selectedAsset = None
        # screen.blit(s_render("Deselect Asset", 70, color), (1450, 115))
        drawCenterTxt(screen,"Deselect Asset",70,color,(1740,105),centerY=False)

        # Draws the description about the stock on the left side of the screen
        points = [(200, 605), (850, 605), (850, 960), (200, 960)]

        # NEED TO REIMPLEMENT THE ASSET ANALYTICS
        self.drawAssetInfo(screen,asset,gametime,player)# draws the Asset Analytics underneath the stock graph on the left side of the screen

        # draws the information about the stock in the middle of the screen
        points = [(860, 330), (1620, 330), (1620, 960), (860, 960)]
        pygame.draw.polygon(screen, (0, 0, 0), points, 5)

        # draws the calculator
        extratext = self.classtext[type(asset)].upper()
        
        self.numpad.draw(screen,(190,600),(290,350),extratext,asset.quantity)
        # self.numpad.draw(screen,(870,620),(300,330),extratext,asset.quantity)
        yamt = int(780/len(asset.getStockObj().graphrangeoptions))
        for i,graphname in enumerate(asset.getStockObj().graphrangeoptions):# 1H, 1D, etc...
            # asset.getStockObj().baredraw(screen,(1630,200+(i*125)),(270,115),graphname)# draws the graph on the right side of the screen
            self.selectedGraph.drawBare(screen,(1630,200+(i*(yamt))),(270,yamt-10),graphname,True,"Normal")
            
            text = s_render(graphname, 40, (230, 230, 230))
            screen.blit(text, (1640, 315+(i*(yamt))-text.get_height()-20))

        # color = ((200,0,0) if asset.getPercent() < 0 else (0,200,0)) if asset.getPercent() != 0 else (200,200,200)
        quantity = self.numpad.getValue()# gets the quantity from the numpad
        netgl = (asset.getValue(bypass=True,fullvalue=False) - asset.getOgVal())*quantity# net gain/loss
        taxedAmt = 0 if netgl <= 0 else netgl*player.taxrate# the amount taxed
        value = asset.getValue(fullvalue=False)*quantity
        feeAmt = value*0.02# the amount taxed
        value -= taxedAmt
        
        if type(asset) == OptionAsset:# Options need the extra fee
            value -= feeAmt
            data = [("Value",f"${limit_digits(asset.getValue(bypass=True,fullvalue=False),17)}","x"),(f"{(player.taxrate*100)}% Tax", f"${limit_digits(taxedAmt,22)}","-"),(f"2% Option Fee", f"${limit_digits(feeAmt,22)}","-")]
            self.orderBox.loadData(self.numpad.getNumstr(self.classtext[type(asset)]),f"${limit_digits(value,22)}",data)
 
        else:
            data = [("Value",f"${limit_digits(asset.getValue(bypass=True,fullvalue=False),15)}","x"),(f"{(player.taxrate*100)}% Tax", f"${limit_digits(taxedAmt,22)}","-")]
            self.orderBox.loadData(self.numpad.getNumstr(self.classtext[type(asset)]),f"${limit_digits(value,22)}",data)

        result = self.orderBox.draw(screen)

        if result:
            # asset.sell(player,quantity,(1.02 if type(asset) == OptionAsset else 1))
            player.sellAsset(asset,quantity,(1.02 if type(asset) == OptionAsset else 1))
            self.selectedAsset = None

        
    def drawAssetInfo(self,screen,asset,gametime,player):

        # top part of the asset Info
        ogtext = s_render("Original", 55, (190, 190, 190))
        screen.blit(ogtext, (885, 350))
        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(900+ogtext.get_width(), 350, 35, 35), 0, 10)

        screen.blit(s_render("Current", 55, asset.color), (1140, 350))
        pygame.draw.rect(screen, asset.color, pygame.Rect(1155+ogtext.get_width(), 350, 35, 35), 0, 10)

        
        self.barGraphs[0].updateValues([asset.getOgVal(),asset.getValue(fullvalue=False)],[(110,110,110),asset.color],["$","$"])# bar graph 1 with the original value and the current value
        portfolioP = lambda x : x/(player.getNetworth())
        self.barGraphs[1].updateValues([asset.portfolioPercent*100,portfolioP(asset.getValue())*100],[(110,110,110),asset.color],["%","%"])# bar graph 2 with the orignial allocation and the current allocation
        for graph in self.barGraphs:
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
            strValue = f"{asset.daysToExpiration()} Days"
            color = p3choice((160,10,10),(10,160,10),(190,190,190),asset.daysToExpiration()-5)

        elif isinstance(asset,IndexFundAsset):
            strValue = f"${limit_digits(asset.dividends,15)}"
            color = (0, 190, 0) if asset.dividends > 0 else (190, 190, 190)
        else:
            raise Exception("Asset type not recognized")
        
        
        valueText = s_render(strValue, 50, (0,0,0))# the value for the dividend / expiration date
        nameText = s_render({StockAsset:"Dividends",OptionAsset:"Expiration",IndexFundAsset:"Dividends"}.get(type(asset)),47,(0,0,0))
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

            if asset.getPercent() < 0:
                return (1-((1+((asset.getPercent())/100))**(365/diff.days))) * -100
            return (((1+(asset.getPercent()/100))**(365/diff.days))-1) * 100
        
        drawCenterTxt(screen,f"Purchase Details",45,(220,220,220),(1047,655),centerY=False)

        yearlyReturn = getYearlyReturn(asset,gametime)

        percentDiff = asset.getPercent()-self.totalmarket.getPercentDate(asset.dateobj,gametime)

        info = [
            (f"DOP",f"{asset.dateobj.strftime('%m/%d/%Y')}"),
            (f"Days",f"{(gametime.time-asset.dateobj).days}"),
            (f"Yearly Return",f"{limit_digits(yearlyReturn,15)}%"),       
        ]
        drawLinedInfo(screen,(870,710),(355,260),info,40,(215,215,215))
        # ---------------Right bottom (Asset Specifics)----------------
        drawCenterTxt(screen,f"Asset Specifics",45,(220,220,220),(1422,655),centerY=False)

        if isinstance(asset,StockAsset):

            info = [
                (f"Current Yield", f"{limit_digits(asset.getDividendYield(),15)}%"),
                (f"Vs Market",f"{limit_digits(percentDiff,15)}%"),  
                (f"Voliatility" ,f"{limit_digits(asset.getVolatility()*100,15)}%"),
            ]
            
        elif isinstance(asset,OptionAsset):

            info = [
                (f"Strike Price",f"{asset.strikePrice}"),
                (f"Voliatility",f"{limit_digits(asset.getVolatility()*100,15)}%"),
                (f"Exp Date",f"{asset.getExpDate()}"),
            ]
        elif isinstance(asset,IndexFundAsset):
            # put relevant info for an index fund here
            info = [
                (f"Dividend Yield", f"{limit_digits(asset.getDividendYield(),15)}%"),
                (f"Vs Market (1Y)",f"{limit_digits(percentDiff,15)}%"),  
                (f"Voliatility" ,f"{limit_digits(asset.getVolatility()*100,15)}%"),
            ]
        drawLinedInfo(screen,(1230,710),(385,260),info,40,(215,215,215))


        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(870, 700, 745, 250), 5, border_radius=10)# border for both the lined infos
        

    def drawLoanInfo(self,screen,player):
        """Draws the loan info"""
        # draws the loan info on the right side of the screen
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1400, 100, 500, 285), 5, border_radius=10)
        drawCenterTxt(screen,"Loan Info",70,(163, 12, 7),(1420,115),centerX=False,centerY=False)

        if drawClickableBoxWH(screen,(1690,110),(195,60),"Go to Loans", 45, (0,0,0),(200,200,200)):
            self.player.screenManager.setScreen("Bank")
            self.player.screenManager.screens['Bank'].menuSelection.setSelected("Loans")

        drawLinedInfo(screen,(1410,180),(480,205),[
            ("Total Debt",f"${limit_digits(player.getCurrentDebt(),24)}"),
            ("Max Loans",f"${limit_digits(player.getMaxLoan(),24)}"),
            ("Num Loans",f"{limit_digits(len(player.loans),24,True)} Loans"),
        ],40,(222, 66, 27))



    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, player, gametime):
        """Draws all of the things in the portfolio menu"""
        mousex, mousey = pygame.mouse.get_pos()
        
        sortedassets = self.get_allassets()# gets the sorted assets of the player
        # screen.blit(s_render(f"{None if self.selectedAsset == None else self.selectedAsset[1]}", 70, (210, 210, 210)), (200, 1000))
        if self.selectedAsset != None and self.selectedAsset not in sortedassets:# if the selected asset is not in the sorted assets
            if len(sortedassets) > 0:# if there are assets
                self.selectedAsset = sortedassets[0]# set the selected asset to the first asset in the sorted assets
            else:# if there are no assets
                self.selectedAsset = None# set the selected asset to None

        
        if self.selectedAsset == None:# if the selected asset is None
            self.networthGraph.drawFull(screen,(200,100),(650,500),"Portfolio Networth",True,"Normal")

            if len(sortedassets) > 0:
                # draws the stocks on the right of the screen
                self.draw_assetscroll(sortedassets,screen)

            assets = player.getAssets()
            values = [[asset.getValue(),asset.name,asset.color] for asset in assets]
            values.append([player.cash, "Cash",player.color])
            self.piechart.updateData(values)
            
            self.piechart.draw(screen,self.player.screenManager)
            
            self.drawLoanInfo(screen,player)# draws the loan info on the right side of the screen

            wh = (500,285)
            for i,stock in enumerate(self.displayedStocks):
                # 870/3 = 290
                # if stock.draw(screen,stock,(1400,200+(i*255)),(500,245),0,rangecontroldisp=False,graphrange="1D") and == 1:# if the stock name is clicked
                coords = (1400,390+(i*290))
                stock.drawFull(screen,coords,wh,f"PortfolioExtra{i}",True,"hoverName")

        
        else:# if the selected asset is NOT None

            self.selectedGraph.setStockObj(self.selectedAsset[0].getStockObj())
            self.selectedGraph.drawFull(screen,(200,100),(650,500),f"Main Portfolio",True,"Normal")# draws the selected stock graph on the left

            self.draw_selected_description(screen,self.selectedAsset,player,gametime)# draws the description of the selected asset
            if self.selectedAsset != None:
                self.drawselectedScroll(screen,self.selectedAsset)# draws the selected asset scroll on the right

            
        self.assetscroll_controls(screen)

        
