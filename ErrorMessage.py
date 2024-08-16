import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")

# class ErrorMessage:
#     def __init__(self,coords:list,text:str,txtSize:int,txtColor:tuple,backColor:tuple,s_render) -> None:
#         self.coords = list(coords)
#         self.text = text
#         self.txtSize = txtSize
#         self.txtColor = txtColor
#         self.backColor = backColor
#         self.s_render = s_render
#         self.surf = self.createSurface()
#         self.life = 240
        

#     def createSurface(self):
#         renderedTxt : pygame.Surface = self.s_render(self.text, self.txtSize, self.txtColor)
#         self.coords[1] -= renderedTxt.get_height()+15
#         self.coords[0] -= renderedTxt.get_width()//2
#         surf = pygame.Surface((renderedTxt.get_width()+40,renderedTxt.get_height()+20))

#         pygame.draw.rect(surf,self.backColor,pygame.Rect(0,0,surf.get_width(),surf.get_height()),border_radius=15)
#         pygame.draw.rect(surf,(1,1,1),pygame.Rect(0,0,surf.get_width(),surf.get_height()),5,15)

#         surf.blit(renderedTxt,(20,10))
#         surf.set_colorkey((0,0,0))
#         return surf.convert_alpha()
    
#     def draw(self,screen:pygame.Surface):
#         # pygame.draw.rect(screen,(255,255,255),pygame.Rect(10,10,50,50))
#         if self.life > 0:
#             self.surf.set_alpha(min(255,self.life*1.5))
#             screen.blit(self.surf,self.coords)
#             self.coords[1] -= 0.75
#             self.life -= 1
#             return True
#         return False
        
        

# class ErrorMessageHandler:
#     def __init__(self,s_render) -> None:
#         self.messageList : list[ErrorMessage] = [] 
#         self.sRender = s_render
#         self.framesAgoAdd = 0

#     def addMessage(self,txt:str,txtColor=(190,190,190),backColor=(160,10,10),txtSize=35,coords:list=None):
#         """If coords aren't given, the message will be displayed at the mouse position"""
#         if self.framesAgoAdd == 0:
#             coords = pygame.mouse.get_pos() if coords == None else coords
#             self.messageList.append(ErrorMessage(coords,txt,txtSize,txtColor,backColor,self.sRender))
#             self.framesAgoAdd = 30

    
#     def update(self,screen):
#         if self.framesAgoAdd > 0:
#             self.framesAgoAdd -= 1
#         for i in range(len(self.messageList)-1,0,-1):
#             message = self.messageList[i]
#             if not message.draw(screen):# draws the message and checks if the message has life left
#                 self.messageList.pop(i)
                

# EXAMPLE USAGE
# errors = ErrorMessageHandler()
lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)

    rect = pygame.Rect(100, 100, 200, 100)

    # Draw the oval
    pygame.draw.ellipse(screen, (255,255,255), rect)
    pygame.draw.ellipse(screen, (0,0,0), rect, 5)

    screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button pressed",pygame.mouse.get_pos())


    clock.tick(60)





