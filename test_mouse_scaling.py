#!/usr/bin/env python3
"""
Test mouse scaling with start menu
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import pygame
from Defs import resolution_manager, get_game_surface, enable_mouse_scaling, disable_mouse_scaling

def test_mouse_scaling():
    pygame.init()
    
    # Get monitor resolution
    monitor_info = pygame.display.Info()
    monitor_width = monitor_info.current_w
    monitor_height = monitor_info.current_h
    
    print(f"Monitor resolution: {monitor_width}x{monitor_height}")
    
    # Create fullscreen display
    screen = pygame.display.set_mode((monitor_width, monitor_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Mouse Scaling Test")
    
    # Setup scaling
    resolution_manager.setup(monitor_width, monitor_height)
    game_surface = get_game_surface()
    
    # Enable mouse scaling
    enable_mouse_scaling()
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                scaled_pos = pygame.mouse.get_pos()  # Should now return scaled coordinates
                print(f"Scaled mouse click: {scaled_pos}")
        
        # Clear surfaces
        screen.fill((0, 0, 0))
        game_surface.fill((20, 30, 40))
        
        # Draw test content on internal surface
        # Draw corners to show the game area
        pygame.draw.circle(game_surface, (255, 0, 0), (100, 100), 20)  # Top-left
        pygame.draw.circle(game_surface, (0, 255, 0), (1820, 100), 20)  # Top-right
        pygame.draw.circle(game_surface, (0, 0, 255), (100, 980), 20)  # Bottom-left
        pygame.draw.circle(game_surface, (255, 255, 0), (1820, 980), 20)  # Bottom-right
        
        # Draw center crosshair
        pygame.draw.line(game_surface, (255, 255, 255), (960, 540-50), (960, 540+50), 3)
        pygame.draw.line(game_surface, (255, 255, 255), (960-50, 540), (960+50, 540), 3)
        
        # Draw resolution info
        info_text = font.render(f"Internal: 1920x1080, Monitor: {monitor_width}x{monitor_height}", True, (255, 255, 255))
        scale_text = font.render(f"Scale: {resolution_manager.scale_factor:.2f}", True, (255, 255, 255))
        game_surface.blit(info_text, (50, 50))
        game_surface.blit(scale_text, (50, 90))
        
        # Get mouse position (should be automatically scaled now)
        scaled_mouse = pygame.mouse.get_pos()
        mouse_text = font.render(f"Mouse (scaled): {scaled_mouse}", True, (255, 255, 255))
        game_surface.blit(mouse_text, (50, 130))
        
        # Draw mouse cursor on game surface
        if 0 <= scaled_mouse[0] <= 1920 and 0 <= scaled_mouse[1] <= 1080:
            pygame.draw.circle(game_surface, (255, 100, 100), scaled_mouse, 10)
        
        # Test instructions
        instructions = font.render("Click corners to test mouse scaling. ESC to exit.", True, (255, 255, 255))
        game_surface.blit(instructions, (50, 170))
        
        # Render scaled game to screen
        resolution_manager.render_to_screen(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Cleanup
    disable_mouse_scaling()
    pygame.quit()

if __name__ == "__main__":
    test_mouse_scaling()
