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
import math

DX = 300# default x
DY = 230# default y
DH = 120# default height
class Portfolio(Menu):
    def __init__(self,stocknames,transact) -> None:
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

        self.portfoliotext = fontlist[65].render('Owned Shares',(220,220,220))[0]
        self.displayingtext = fontlist[35].render('Displaying ',(220,220,220))[0]
        self.menudrawn = False
        # self.allrenders = []
        self.selected_asset = None
        self.transact = transact

        # for the asset type selection which sorts the latterscroll
        # self.assetoptions = ["Stocks","Options","Other"]# future, Crypto, bonds, minerals, real estate, etc
        self.assetoptions = ["Stocks","Options","Other"]
        self.displayed_asset_type = ["Stocks","Options","Other"]


        # self.latterScrollsurf = pygame.Surface((730,730))
        self.latterscrollnorm = PortfolioLatter()
        self.latterscrollselect = PortfolioLatter()
        self.numpad = Numpad()

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
            if isinstance(asset,StockAsset):
                text = "Share"
            elif isinstance(asset,OptionAsset):
                text = "Option"
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
        points = [(200, 660), (850, 660), (850, 960), (200, 960)]
        gfxdraw.filled_polygon(screen, points, (30, 30, 30))
        pygame.draw.polygon(screen, (0, 0, 0), points, 5)

        for i,txt in enumerate(self.stocktext[asset.stockobj.name]):
            if i == 0:# the first line is the name of the stock
                screen.blit(txt,(210,605))# blits the full name of the stock 
            else:
                screen.blit(txt,(210,670+((i-1)*35)))# blits the other lines of the stock description

        vol = asset.getVolatility()
        text = s_render(f"Annualized Volatility: {vol:,.2f}%", 40, (190, 190, 190))
        screen.blit(text, (210, 845))
        text = s_render("Annual Dividend: $0.00", 40, (190, 190, 190))
        screen.blit(text, (210, 890))

        # draws the information about the stock in the middle of the screen
        points = [(860, 330), (1620, 330), (1620, 960), (860, 960)]
        pygame.draw.polygon(screen, (0, 0, 0), points, 5)

        # draws the calculator
        if isinstance(asset,StockAsset):
            extratext = "SHARE"
        elif isinstance(asset,OptionAsset):
            extratext = "OPTIONS"
        self.numpad.draw(screen,(870,620),(300,330),extratext,mousebuttons,asset.quantity)
        
        for i,graphname in enumerate(asset.stockobj.graphrangeoptions):# 1H, 1D, etc...
            asset.stockobj.baredraw(screen,(1630,200+(i*125)),(270,115),graphname)# draws the graph on the right side of the screen
            text = s_render(graphname, 40, (230, 230, 230))
            screen.blit(text, (1640, 325+(i*125)-text.get_height()-20))

        color = ((200,0,0) if asset.getPercent() < 0 else (0,200,0)) if asset.getPercent() != 0 else (200,200,200)
        quantity = self.numpad.get_value()# gets the quantity from the numpad
        netgl = (asset.getValue(bypass=True,fullvalue=False) - asset.ogvalue)*quantity# net gain/loss
        taxedamt = 0 if netgl <= 0 else netgl*player.taxrate# the amount taxed

        descriptions = [s_render("Net Gain" if asset.getPercent() > 0 else "Net Loss", 25, (230,230,230)),
            s_render(f"Taxes ({player.taxrate*100}%)", 25, (230, 230, 230)),
            s_render("Final Value (After Tax)", 25, (230, 230, 230)),]
        texts = [s_render(f"${limit_digits(netgl,10)}", 70, color),
            s_render(f"-${limit_digits(abs(taxedamt),10)}", 70, (180, 50, 50)),
            s_render(f"${limit_digits((asset.getValue(fullvalue=False)*quantity)-taxedamt,15)}", 70, (190, 190, 190)),]


        
        if self.drawSellingInfo(screen,descriptions,texts,mousebuttons,quantity):# if the asset should be sold, and drawing the selling info
            asset.sell(player,quantity)
            self.selected_asset = None
        # need to fix teh option.add method - when you add the og value doesn't change
        self.drawAssetInfo(screen,asset,gametime,player)# draws the info above the sell info

    def drawAssetInfo(self,screen,asset,gametime,player):
        """Draws the info above the sell info"""
        # screen.blit(s_render(f"Purchased At {}"))
        def getYearlyReturn(asset,gametime):
            """returns the yearly return of the asset"""
            diff = gametime.time-asset.dateobj
            if diff.days <= 365:
                return asset.getPercent()
            return asset.getPercent()/(diff.days/365)
        color = (200,200,200)
        descriptions = [
            [s_render("Time Of", 25, color),
                s_render("Inital Share", 25, color),
                s_render("Inital", 25, color),
                s_render("Avg Yearly", 25, color),
                s_render("Portfolio", 25, color),],
            [s_render("Purchase", 25, color),
                s_render("Value", 25, color),
                s_render("Value", 25, color),
                s_render("Return", 25, color),
                s_render("Percentage", 25, color),]
        ]
        values = [
            s_render(f"{asset.date}", 40, (190, 190, 190)),
            s_render(f"${limit_digits(asset.ogvalue,12)}", 40, (190, 190, 190)),
            s_render(f"${limit_digits(asset.ogvalue*asset.quantity,12)}", 40, (190, 190, 190)),
            s_render(f"{limit_digits(getYearlyReturn(asset,gametime),12)}%", 40, (190, 0, 0) if getYearlyReturn(asset,gametime) < 0 else (0, 190, 0)),
            s_render(f"{limit_digits((asset.getValue()/player.getNetworth())*100,12)}%", 40, (190, 190, 190)),
        ]
        for i,(dtxt1,dtxt2,vtxt) in enumerate(zip(descriptions[0],descriptions[1],values)):
            screen.blit(dtxt1,(865,335+(i*50)))
            screen.blit(dtxt2,(875,355+(i*50)))
            screen.blit(vtxt, (965,340+(i*50)))
        # text = [
        #     f"Time Of Purchase: {asset.date}",
        #     f"Original Per Share Value: ${asset.ogvalue}",
        #     f"Yearly Return: {getYearlyReturn(asset,gametime)}%",
        #     f"% Of Portfolio: {asset.getValue()/player.getNetworth():.3f}%"
        # ]
        # 866 336
        # for i,txt in enumerate(text):
        #     screen.blit(descriptions[i],(866,336+(i*50)))
        #     screen.blit(txt, (866, 336+(i*50)))



    def drawSellingInfo(self,screen,descriptions,values,mousebuttons,quantity) -> bool:
        """Draws the selling info above the trade asset button and the button itself"""
        mousex, mousey = pygame.mouse.get_pos()

        for i,(dtxt,vtxt) in enumerate(zip(descriptions,values)):
            screen.blit(dtxt,(1180,620+(i*85)))
            screen.blit(vtxt,(1190,645+(i*85))) 

        rect = pygame.Rect(1180, 875, 425, 75)
        pygame.draw.rect(screen, (0, 0, 0), rect, 5,border_radius=10)
        color = (190,190,190)
        if rect.collidepoint(mousex,mousey):
            color = (0,190,0)
            if mousebuttons == 1 and quantity > 0:# if the asset should be sold
                return True
        screen.blit(s_render("TRADE ASSET", 65, color), (1275, 890))
        return False    

        
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
            player.draw(screen,player,(200,100),(650,500),mousebuttons,gametime)

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
            draw_pie_chart(screen, values, 150,(200, 650))


            self.transact.draw(screen,mousebuttons,(1400,105),(500,960),(500,150))

        
        else:# if the selected asset is NOT None
            stockgraph = self.selected_asset[0].stockobj

            stockgraph.draw(screen,player,(200,100),(650,500),mousebuttons,gametime)# draws the selected stock graph on the left

            selectedindex = sortedassets.index(self.selected_asset)
            self.drawselectedScroll(screen,sortedassets[selectedindex],mousebuttons)# draws the selected asset scroll on the right

            self.draw_selected_description(screen,sortedassets[selectedindex],mousebuttons,player,gametime)# draws the description of the selected asset
        self.assetscroll_controls(screen,mousebuttons)

        
