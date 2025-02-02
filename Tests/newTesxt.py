import pygame
import pygame.freetype
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import random

# Initialize pygame and OpenGL
pygame.init()
WINDOW_SIZE = (1920, 1080)
pygame.display.set_mode(WINDOW_SIZE, pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

# Setup OpenGL projection
glViewport(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, WINDOW_SIZE[0], WINDOW_SIZE[1], 0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Enable alpha blending and texture support
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_TEXTURE_2D)

class TextureAtlas:
    def __init__(self, size=(2048, 2048)):
        self.size = size
        # Create a Surface with per-pixel alpha
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.texture_id = glGenTextures(1)
        self.positions = {}
        self.next_x = 0
        self.next_y = 0
        self.row_height = 0

    def add_text(self, text, font):
        # If text already added, return its position and size
        if text in self.positions:
            return self.positions[text]
        
        # Render the text using pygame font
        text_surface = font.render(text, True, (255, 255, 255))
        w, h = text_surface.get_width(), text_surface.get_height()
        
        # If current row can’t fit the text, wrap to next line
        if self.next_x + w > self.size[0]:
            self.next_x = 0
            self.next_y += self.row_height
            self.row_height = 0
        
        pos = (self.next_x, self.next_y)
        self.surface.blit(text_surface, pos)
        self.positions[text] = (pos, (w, h))
        
        self.next_x += w + 2  # Add a small padding
        self.row_height = max(self.row_height, h)
        return self.positions[text]

def test_atlas_rendering():
    NUM_ELEMENTS = 500
    font = pygame.font.Font(None, 32)
    atlas = TextureAtlas()
    # Pre-calculate positions for rendering
    positions = [(x, y) for x in range(50, 1800, 100) for y in range(50, 900, 30)]
    
    # Pre-generate some texts into the atlas
    for i in range(NUM_ELEMENTS):
        text = f"Value: {random.random():.3f}"
        atlas.add_text(text, font)
    
    # Setup texture parameters once
    glBindTexture(GL_TEXTURE_2D, atlas.texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    start_time = time.time()
    frames = 0
    running = True
    
    while running and frames < 6000:
        clock.tick(600)
        frames += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
    
        # Update the atlas texture each frame in case new texts are added.
        # Use get_view with conversion to bytes (new method instead of deprecated tostring)
        texture_data = bytes(atlas.surface.get_view("1"))
        glBindTexture(GL_TEXTURE_2D, atlas.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, atlas.size[0], atlas.size[1],
                     0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        
        # Set current color to white
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        # Render text using OpenGL and the atlas texture
        glBegin(GL_QUADS)
        for i, pos in enumerate(positions[:NUM_ELEMENTS]):
            text = f"Value: {random.random():.3f}"
            tex_pos, size = atlas.add_text(text, font)
            
            x, y = pos
            w, h = size
            tx = tex_pos[0] / atlas.size[0]
            ty = tex_pos[1] / atlas.size[1]
            tw = w / atlas.size[0]
            th = h / atlas.size[1]
            
            glTexCoord2f(tx, ty)
            glVertex2f(x, y)
            glTexCoord2f(tx + tw, ty)
            glVertex2f(x + w, y)
            glTexCoord2f(tx + tw, ty + th)
            glVertex2f(x + w, y + h)
            glTexCoord2f(tx, ty + th)
            glVertex2f(x, y + h)
        glEnd()
        
        pygame.display.flip()
        
    return frames / (time.time() - start_time)

print("\nTesting OpenGL atlas-based rendering...")
atlas_fps = test_atlas_rendering()
print(f"Atlas-based FPS: {atlas_fps:.1f}")

pygame.quit()