import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
# from Classes.imports.stockeventspos import StockEvents
from Classes.imports.Latterscroll import LatterScroll
# from Classes.imports.Newsbar import News
from Classes.Stock import Stock
from Classes.StockVisualizer import StockVisualizer

# [20,60] [60,20]
# [700,1000] [1000,650]

class UIControls():
    def __init__(self,stocklist,gamespeed,gametime,tmarket,player) -> None:
        self.gameplay_speed = 0
        # self.stockevent = StockEvents()# the stock events
        self.bar = SliderBar(gamespeed,[(247, 223, 0),(110,110,110)],barcolor=[(255,255,255),(200,200,200)])# the bar for the gameplay speed
        # self.newsobj = News()
        self.latterscroll = LatterScroll()
        # for i in range(10):
        #     for stock in stocklist:
        #         self.newsobj.addStockNews(stock.name)
        self.totalMarketGraph = StockVisualizer(gametime,tmarket,[tmarket,player])

        self.view = "stock"# home or stock
        self.accbar_middle = "move"# move, stock, pie
        self.accbar_right = "topAsset"# topAsset, transactions, loans
        self.graphscroll = 0
        self.namerenders = [fontlist[30].render(stock.name,stock.color)[0] for stock in stocklist]# [red,green]
        self.weeknames = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        self.weekdaystext = {weekday:fontlist[95].render(weekday,(255,255,255))[0] for weekday in self.weeknames}
        # self.namerenders = [[fontlist[30].render(stock.name,(200,0,0))[0],fontlist[30].render(stock.name,(0,200,0))[0]] for stock in stocklist]# [red,green]

        # get 
        self.get_percent = lambda stock : round(((stock.graphs["1D"][-1]/stock.graphs["1D"][0])-1)*100,2)
        self.get_listpercents = lambda xlist : [self.get_percent(stock) for stock in xlist]
        self.percentchanges = self.get_listpercents(stocklist)
        self.totalperecent = lambda xlist : sum([self.get_percent(stock) for stock in xlist])
        # for pie chart
        self.stockbarsurf = pygame.Surface((1200,80))
        
        
        
    def drawIcon(self, screen: pygame.Surface,mousebuttons) -> bool:
        """Draws the home/stock icon in the top left corner, returns True if the icon is clicked"""
        # Draw the triangles to form a square in the top left corner
        hometri = [(25, 10), (25, 160), (175, 10)]
        stockstri = [(175, 10), (175, 160), (25, 160)]

        # Check if the mouse is clicked and hovering over the triangles
        mouse_pos = pygame.mouse.get_pos()
        home_color = (0, 120, 0) if self.view == "home" else (20,20,20)
        stocks_color = (120, 0, 0) if self.view == "stock" else (20,20,20)

        # Check if the mouse is hovering over the triangles
        if point_in_triangle(mouse_pos, hometri):
            home_color = (0, 170, 0)
            stocks_color = (80, 0, 0) if stocks_color == (120, 0, 0) else (20,20,20)
            if mousebuttons == 1:
                self.view = "home"
                soundEffects['clickbutton2'].play()
                return True

        if point_in_triangle(mouse_pos, stockstri):
            stocks_color = (170, 0, 0)
            home_color = (0, 120, 0) if home_color == (0, 170, 0) else (20,20,20)
            
            if mousebuttons == 1:
                self.view = "stock"
                soundEffects['clickbutton2'].play()
                return True

        # Draw the triangles
        pygame.draw.polygon(screen, home_color, [(x, y) for x, y in hometri])
        pygame.draw.polygon(screen, stocks_color, [(x, y) for x, y in stockstri])

        # Draw the outline for the triangles
        pygame.draw.polygon(screen, (0, 0, 0), [(x, y) for x, y in hometri], 4)
        pygame.draw.polygon(screen, (0, 0, 0), [(x, y) for x, y in stockstri], 4)

        # Draw the "Home" and "Stocks" text in the triangles
        home = fontlist[50].render('Home', (255, 255, 255))[0]
        screen.blit(home, (90 - home.get_width() / 2 - 15, 45 - home.get_height() / 2))
        stocks = fontlist[50].render('Stocks', (255, 255, 255))[0]
        screen.blit(stocks, (140 - stocks.get_width() / 2 - 15, 95 + stocks.get_height() / 2))
        return False



    def draw_stockbar(self,screen:pygame.Surface,stocklist:list,coords:list=[250,710],wh=[1200,80]):
        """Draws a bar that scrolls across the screen, displaying the stock prices, maxwidth is 1710"""

        dx,dy = coords
        if wh[1] > 1710: wh[1] = 1710
        if self.stockbarsurf.get_width() != wh[0] or self.stockbarsurf.get_height() != wh[1]:
            self.stockbarsurf = pygame.Surface(wh).convert_alpha()
        
        self.graphscroll += 1*(self.gameplay_speed/self.bar.maxvalue)+1# the speed of the stock graph 
        self.percentchanges = self.get_listpercents(stocklist)
        if self.graphscroll > len(stocklist)*190: self.graphscroll = 0
        for i,stock in enumerate(stocklist):# draws the stock graph bar
            x = int(0-self.graphscroll+(i*190))
            if x < -120:
                x += len(stocklist)*190
            if x < wh[0]+100:# if the stock is on the screen
                
                color = (0,200,0) if self.percentchanges[i] >= 0 else (200,0,0)

                stocklist[i].baredraw(self.stockbarsurf,(x,0),(100,wh[1]),'1H')# draws the graph
                self.stockbarsurf.blit(self.namerenders[i],(x-70,10))# draws the name of the stock
                ptext = fontlist[28].render(limit_digits(stock.price,9),color)[0]# renders the price of the stock
                self.stockbarsurf.blit(ptext,(x-42-(ptext.get_width()/2),50))# draws the price of the stock

        pygame.draw.rect(self.stockbarsurf,(0,0,0),pygame.Rect(0,0,wh[0],wh[1]),5)# draws the outline of the stock graph bar
        screen.blit(self.stockbarsurf,(dx,dy))# draw the stock graph bar to the screen
        self.stockbarsurf.fill((30,30,30))# fill the stock graph bar with a dark grey color
        
    def draw_accbar_middle(self,screen:pygame.Surface,stocklist:list,mousebuttons,player):
        """Draws the stock events to the screen"""
        # points1 = [(940,175),(955,215),(940+250,215),(925+250,175)]
        # points2 = [(940+250,175),(955+250,215),(940+505,215),(925+505,175)]
        
        # gfxdraw.filled_polygon(screen,points1,(30,30,30))
        # gfxdraw.filled_polygon(screen,points2,(30,30,30))
        # pygame.draw.polygon(screen,(0,0,0),points1,5)
        # pygame.draw.polygon(screen,(0,0,0),points2,5)
        dcolor = (255,255,255)
        scolor = (0,220,0)
        
        
        stocktext = s_render('STOCKS',30,scolor if self.accbar_middle == "stock" else dcolor)
        movetext = s_render('MOVEMENTS',30,scolor if self.accbar_middle == "move" else dcolor)
        pietext = s_render('PIE CHART',30,scolor if self.accbar_middle == "pie" else dcolor)
        blitpoints = [(940,170),(940+stocktext.get_width()+30,170),(940+stocktext.get_width()+60+movetext.get_width(),170)]
        

        texts = [stocktext,movetext,pietext]
        screen.blits((text,point) for text,point in zip(texts,blitpoints))

        for point,text,name in zip(blitpoints,texts,["stock","move","pie"]):
            # pygame.draw.rect(screen,(0,0,0),pygame.Rect(point,text.get_size()))
            if pygame.Rect(point,text.get_size()).collidepoint(pygame.mouse.get_pos()):
                if mousebuttons == 1:
                    self.accbar_middle = name

        if self.accbar_middle == "move":
            minmove = min([stock for stock in stocklist],key=self.get_percent)
            maxmove = max([stock for stock in stocklist],key=self.get_percent)

            # self.stockevent.addStockEvent(minmove,1600,False)
            # self.stockevent.addStockEvent(maxmove,1600,)
            # self.stockevent.draw(screen)
        elif self.accbar_middle == "pie":

            # values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
            values = [(stock.getValue(),stock.name) for stock in player.stocks]
            names = set([stock.name for stock in player.stocks])

            values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]
            values.append([player.cash, "Cash",player.color])
            for option in player.options:
                values.append([option.getValue(),option.name,option.color])
            draw_pie_chart(screen, values, 190, (935, 235))

        elif self.accbar_middle == "stock":    
            pass
    
    def draw_accbar_right(self,screen:pygame.Surface,stocklist:list,player,mousebuttons):
        dcolor = (255,255,255)
        scolor = (0,220,0)
        
        topAssettext = s_render('TOP ASSETS',30,scolor if self.accbar_right == "topAsset" else dcolor)
        transactionstext = s_render('TRANSACTIONS',30,scolor if self.accbar_right == "transactions" else dcolor)
        loanstext = s_render('LOANS',30,scolor if self.accbar_right == "loans" else dcolor)
        blitpoints = [(1480,170),(1480+topAssettext.get_width()+30,170),(1480+topAssettext.get_width()+60+transactionstext.get_width(),170)]
        
        texts = [topAssettext,transactionstext,loanstext]
        screen.blits((text,point) for text,point in zip(texts,blitpoints))

        for point,text,name in zip(blitpoints,texts,["topAsset","transactions","loans"]):
            # pygame.draw.rect(screen,(0,0,0),pygame.Rect(point,text.get_size()))
            if pygame.Rect(point,text.get_size()).collidepoint(pygame.mouse.get_pos()):
                if mousebuttons == 1:
                    self.accbar_right = name
        
        if self.accbar_right == "topAsset":
            
            assets = player.getAssets(5)

            #     # function to get the text for each stock
            # get_text = lambda stock : [f'{stock[0]} ',
            #                             f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}",
            #                             f'${limit_digits(stock[0].price*stock[2],15)}',]
            def get_text(asset):
                percentchange = asset.getPercent()
                c = '+' if percentchange > 0 else ''
                if isinstance(asset,StockAsset):
                    return [f'${limit_digits(asset.getValue(),10)}',f'{asset.name} shares of {asset.stockobj.name}',f'{c}{limit_digits(percentchange,8)}%',]
                elif isinstance(asset,OptionAsset):
                    return [f'${limit_digits(asset.getValue(),10)}',f'{asset.name} option',f'{c}{limit_digits(percentchange,8)}%',]
                #     percentchange = ((asset[0].price - asset[1]) / asset[1]) * 100
                #     c = '+' if percentchange > 0 else ''
                #     return [f'${limit_digits(asset[0].price*asset[2],10)}',f'{asset[2]} shares of {asset[0].name}',f'{c}{limit_digits(percentchange,6)}%',]
                # elif isinstance(asset[0],OptionAsset):
                #   return [f'${limit_digits(asset[0].get_value(),10)}',f'{asset[0].name} option',f'{c}{limit_digits(percentchange,6)}%',]

            # getting the text for each stock
            textlist = [get_text(asset) for asset in assets]# stores 3 texts for each stock in the sortedstocks list

            textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
            coords = [[(15,10),(20,60)] for i in range(len(textlist))]
            # loop through the textlist and store the text info in the textinfo list
            for i,(text,asset) in enumerate(zip(textlist,assets)):
                polytexts = []# temporary list to store the text info for each stock
                polytexts.append([text[0],50,asset.color])
                polytexts.append([text[1],35,(190,190,190)])
                polytexts.append([text[2],50,(190,190,190)])
                textinfo.append(polytexts)
                coords[i].append(((text[1],50),30))

            self.latterscroll.storetextinfo(textinfo)# simply changes the self.texts in latterscroll
            self.latterscroll.set_textcoords(coords)# simply changes the self.textcoords in latterscroll
            # Does most of the work for the latter scroll, renders the text and finds all the coords
            maxwh = (420,700)
            self.latterscroll.store_rendercoords((1475,205), maxwh,125,0,0,updatefreq=5)
            # drawing the latter scroll and assigning the selected stock
            self.latterscroll.draw_polys(screen, (1475,205), maxwh, mousebuttons, None, True)
            
            # for i,asset in enumerate(assets):
            #     #all the texts to be rendered
                
            #     if isinstance(asset[0],Stock):
            #         percentchange = ((asset[0].price - asset[1]) / asset[1]) * 100
            #         c = '+' if percentchange > 0 else ''
            #         texts = [f'${limit_digits(asset[0].price*asset[2],10)}',f'{asset[2]} shares of {asset[0].name}',f'{c}{limit_digits(percentchange,6)}%',]
            #     elif isinstance(asset[0],StockOption):
            #         percentchange = asset[0].percent_change()
            #         c = '+' if percentchange > 0 else ''
            #         texts = [f'${limit_digits(asset[0].get_value(),10)}',f'{asset[0].name} option',f'{c}{limit_digits(percentchange,6)}%',]
                    
            #     # all the coords for the texts to be rendered
            #     coords = [(15,10),(20,50),((texts[1],75),30)]
            #     color = ((0,160,0) if percentchange >= 0 else (160,0,0)) if percentchange != 0 else (160,160,160)
            #     colors = [asset[0].color,(190,190,190),color]

            #     finaldict = {}
            #     for ind,text in enumerate(texts):
            #         finaldict[text] = (coords[ind][0],coords[ind][1],[50,30,45][ind],colors[ind])

            #     self.latterscroll.storeTextsVariable(resetlist=(i == 0),extraspace=20,**finaldict)
                
            # self.selected_stock = self.latterscroll.draw_polys(screen,(1475,245),790,115,mousebuttons,None,showbottom=False)
        
    def draw_time(self,screen,gametime):
        texts = gametime.getRenders((50,50,50,105,50,50))# year,month,day,minute,dayname,monthname,am/pm
        year,month,day,minute,dayname,monthname,ampm = texts

        screen.blit(minute,(260,20))
        screen.blit(ampm,(260+minute.get_width()+20,20))
        screen.blit(dayname,(260,105))
        screen.blit(monthname,(260+dayname.get_width()+10,105))
        screen.blit(day,(260+dayname.get_width()+monthname.get_width()+20,105))
        screen.blit(year,(260+dayname.get_width()+monthname.get_width()+day.get_width()+30,105))
        

    def marketStatus(self,screen,gametime):
        color = (0,150,0) if gametime.isOpen()[0] else (150,0,0)
        screen.blit(s_render(f"MARKET {'OPEN' if gametime.isOpen()[0] else 'CLOSED'}",115 if gametime.isOpen()[0] else 95,color),(725,20))
        if not gametime.isOpen()[0]: 
            render = s_render(f"{gametime.isOpen()[1]}",65,color)
            screen.blit(render,(890-(render.get_width()/2),95))
            


    def draw_home(self,screen:pygame.Surface,stocklist:list,gametime,player,mousebuttons):
        """Draws the home screen"""
        timebarpoints = [(200,10),(250,150),(1910,150),(1860,10)]
        gfxdraw.filled_polygon(screen,timebarpoints,(10,10,10,225))# time etc
        pygame.draw.polygon(screen,(0,0,0),timebarpoints,5)# time etc
        # screen.blit(self.weekdaystext[gametime.get_day_name()],(265,20))
        self.draw_time(screen,gametime)


        gfxdraw.filled_polygon(screen,[(250,705),(275,1050),(1475,1050),(1450,705)],(10,10,10,175))# the News bar at the bottom
        pygame.draw.polygon(screen,(0,0,0),[(250,705),(275,1050),(1475,1050),(1450,705)],5)# the News bar at the bottom Outline
        
        
        gfxdraw.filled_polygon(screen,[(930,160),(930,695),(1450,695),(1450,160)],(40,40,40,175))# Movements bar (right of the portfolio)
        gfxdraw.box(screen,pygame.Rect(930,160,520,40),(30,30,30))# Top part of the announce (right of the portfolio)
        pygame.draw.polygon(screen,(0,0,0),[(930,160),(930,695),(1450,695),(1450,160)],5)# Movements bar (right of the portfolio) Outline

        points = [(1460,160),(1460,700),(1910,700),(1910,160)]
        gfxdraw.filled_polygon(screen,points,(30,30,30,175))
        gfxdraw.box(screen,pygame.Rect(1460,160,450,40),(15,15,15))# Top part of the announce (right of the portfolio)
        pygame.draw.polygon(screen,(0,0,0),points,5)

        
        # self.draw_stockbar(screen,stocklist)# draws the stock graph bar
        self.draw_accbar_middle(screen,stocklist,mousebuttons,player)# draws the stock events (On the right of the portfolio)
        self.draw_accbar_right(screen,stocklist,player,mousebuttons)# draws the stock events (On the very right of the screen)
        # self.newsobj.draw(screen)
        

    def draw_ui(self,screen,stockgraphmanager,stocklist,player,gametime,mousebuttons,menulist,tmarket):
        if self.drawIcon(screen,mousebuttons):
            for i in range(len(menulist)):menulist[i].menudrawn = False
        if not any(menu.menudrawn for menu in menulist):# if any of the menus are drawn, then don't draw
            self.marketStatus(screen,gametime)
            if self.view == "home":
                mousex,mousey = pygame.mouse.get_pos()
                
                self.draw_home(screen,stocklist,gametime,player,mousebuttons)            

                # player.draw(screen,player,(250,160),(680,540),mousebuttons,stocklist,True)
                # tmarket.draw(screen,(250,160),(680,540),mousebuttons,gametime)
                # tmarket.drawFull(screen,(250,160),(680,540),"Home Total Market",True,"Normal")
                self.totalMarketGraph.drawFull(screen,(250,160),(680,540),"Home Total Market",True,"hoverName")
                # self.gameplay_speed = self.bar.draw_bar(screen,[1500,650],[120,380],'vertical')
                
                screen.blit(s_render(f'GAMEPLAY SPEED',60,(247, 223, 0)),(830,20))

                self.gameplay_speed = self.bar.draw_bar(screen,[740,75],[450,65],'horizontal',reversedscroll=True,text=gametime.skipText())


            elif self.view == "stock":
                stockgraphmanager.draw_graphs(screen,stocklist,player,mousebuttons,gametime)
                # player.draw(screen,player,(1920,0),(1600,400),stocklist,mousebuttons)
                self.gameplay_speed = self.bar.draw_bar(screen,[1620,575],[125,400],'vertical',text=gametime.skipText())

            



