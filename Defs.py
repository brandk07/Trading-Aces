import pygame
import time
from pygame import gfxdraw
pygame.font.init()
def update_fps(clock):
    fps = str(int(clock.get_fps()))
    fps_text = font25.render(fps, 1, pygame.Color("coral"))
    return fps_text

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.5f} seconds to execute.")
        return result
    return wrapper

def time_loop(loop):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        for item in loop:
            result = item(*args, **kwargs)
        end_time = time.time()
        print(f"Loop took {end_time - start_time:.5f} seconds to execute.")
        return result
    return wrapper

fonts = lambda font_size: pygame.font.SysFont('Cosmic Sans',font_size)
font40 = fonts(40)
font25 = fonts(25)
font18 = fonts(18)



#for time testing
# start_time = time.time()

# for i, point in enumerate(self.pricepoints):
#     # do something

# end_time = time.time()
# print(f"Loop took {end_time - start_time:.5f} seconds to execute.")