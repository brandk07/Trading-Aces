import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")

class PerfChart:
    def __init__(self) -> None:
        self.wh = (450,200)
        self.coords = []
        self.data : dict[str:float|int] = {}# {name:double|str|int}
        self.needToUpdate = True
        self.surf = pygame.Surface(self.wh).convert_alpha()


    def updateData(self,data:dict[str:float|int]):
        assert isinstance(data,dict), "Data must be a dictionary"
        assert all([isinstance(value,(float,int)) for value in data.values()]), "All values in the data dictionary must be either a float or an int"

        self.data = data
        self.needToUpdate = True
    def draw(self,screen,coords) -> bool:
        """Draws the card onto the screen at the given coords"""
        coords = list(coords)
        if pygame.Rect(coords,self.wh).collidepoint(pygame.mouse.get_pos()):
            self.needToUpdate = True
        if self.needToUpdate:
            
            self.updateSurf(coords)
            self.needToUpdate = False

            xwidth = (self.wh[0]-5)//len(self.data)
            for index,(name,value) in enumerate(self.data.items()):
                if pygame.Rect(coords[0]+index*xwidth+10,coords[1]+5,xwidth,self.wh[1]-10).collidepoint(pygame.mouse.get_pos()):
                    # print(name,value)
                    screen.blit(s_render(f"{name}: {value}",20,(255,255,255)),(coords[0]+index*xwidth+10,coords[1]+5))
                

        

        

        screen.blit(self.surf,coords)
    def updateSurf(self,coords=None):
        """Won't check for coords if coords is None"""
        self.surf.fill((0,0,0,0))
        pygame.draw.rect(self.surf,(0,0,0),pygame.Rect(0,0,self.wh[0],self.wh[1]),5,border_radius=15)

        

        maxValue = max([abs(value) for value in self.data.values()])*1.05
        xwidth = (self.wh[0]-5)//len(self.data)
        for index,(name,value) in enumerate(self.data.items()):

            height = 5 if maxValue == 0 else int((abs(value)/maxValue)*(self.wh[1]//2))
            height = max(3,height)
            color = p3choice((175,0,0),(0,175,0),(175,175,175),value)
            if coords and pygame.Rect(coords[0]+index*xwidth+10,coords[1]+5,xwidth,self.wh[1]-10).collidepoint(pygame.mouse.get_pos()):
                color = brightenCol(color,1.5)
                # print("sdfsdlkfljksjdf")
            if value >= 0:
                pygame.draw.rect(self.surf,color,pygame.Rect(index*xwidth+10,self.wh[1]//2-height+5,xwidth*.5,height),border_top_left_radius=10,border_top_right_radius=10)
            else:
                pygame.draw.rect(self.surf,color,pygame.Rect(index*xwidth+10,self.wh[1]//2+5,xwidth*.5,height),border_bottom_left_radius=10,border_bottom_right_radius=10)
        # draw a dashed line across the middle of the screen
        for x in range(0,self.wh[0]-10,10):
            pygame.draw.line(self.surf,(255,255,255),(x+5,self.wh[1]//2+5),(x+10,self.wh[1]//2+5),2)


perfChart = PerfChart()
# perfChart.updateData({"Stock1":100,"Stock2":-50,"Stock3":75,"Stock4":-25,"Stock5":0})
perfChart.updateData({"Q1":4.56,"Q2":-0.99,"Q3":2.34,"Q4":1.23})

lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
mousebuttons = 0
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)
    for i in range(100):
        perfChart.draw(screen,(100,100))

    screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
    pygame.display.flip()
    
    mousebuttons = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttons = event.button
            if mousebuttons == 1:
                print("Mouse button pressed",pygame.mouse.get_pos())
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            print("Pressed the J key")

    clock.tick(60)





