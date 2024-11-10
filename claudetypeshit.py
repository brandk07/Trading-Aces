import pygame
import pygame.gfxdraw
import time
from collections import deque

def init_pygame(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Screen Clear Benchmark")
    return screen

def benchmark_method(screen, method, frames=300):
    clock = pygame.time.Clock()
    times = deque(maxlen=frames)
    
    for _ in range(frames):
        start_time = time.perf_counter()
        
        if method == "fill":
            screen.fill((60, 60, 60))
        elif method == "gfxdraw":
            pygame.gfxdraw.filled_polygon(screen, [(0,0), (900,0), (900,900), (0,900)], (60,60,60))
        elif method == "surface_blit":
            screen.blit(background_surface, (0,0))
        elif method == "draw_rect":
            pygame.draw.rect(screen, (60,60,60), screen.get_rect())
        elif method == "buffer":
            pixels = screen.get_buffer()
            pixels.write(background_bytes)
            del pixels  # Release the buffer
            
        pygame.display.flip()
        end_time = time.perf_counter()
        times.append(end_time - start_time)
        clock.tick(1000)  # Unlimited FPS for testing
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
    
    avg_time = sum(times) / len(times)
    fps = 1 / avg_time if avg_time > 0 else 0
    return fps

# Initialize
WIDTH, HEIGHT = 900, 900
screen = init_pygame(WIDTH, HEIGHT)

# Create background surface once
background_surface = pygame.Surface((WIDTH, HEIGHT))
background_surface.fill((60, 60, 60))

# Create background buffer bytes once
temp_surface = pygame.Surface((WIDTH, HEIGHT))
temp_surface.fill((60, 60, 60))
background_bytes = bytes(temp_surface.get_buffer())

# Test all methods
methods = ["fill", "gfxdraw", "surface_blit", "draw_rect", "buffer"]
results = {}

print("Testing screen clear methods...")
for method in methods:
    fps = benchmark_method(screen, method)
    if fps is None:  # User quit
        pygame.quit()
        exit()
    results[method] = fps
    print(f"{method:12} : {fps:.1f} FPS")

# Sort and display results
print("\nResults sorted by performance:")
for method, fps in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{method:12} : {fps:.1f} FPS")

pygame.quit()