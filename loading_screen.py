#!/usr/bin/env python3
"""
Loading Screen Module for Trading Aces
Shows immediate feedback to user while game initializes
"""

import sys
import time
import threading

# Try to import pygame minimally for basic display
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

class LoadingScreen:
    """Manages the loading screen display during game initialization"""
    
    def __init__(self):
        self.loading = True
        self.current_step = "Starting Trading Aces..."
        self.steps_completed = 0
        self.total_steps = 8
        self.start_time = time.time()
        
        # Loading steps for user feedback
        self.loading_steps = [
            "Starting Trading Aces...",
            "Initializing Pygame...",
            "Loading game assets...",
            "Setting up trading system...",
            "Loading stock data...",
            "Preparing user interface...",
            "Finalizing setup...",
            "Ready to trade!"
        ]
    
    def show_console_loading(self):
        """Show simple console loading for immediate feedback"""
        print("\n" + "="*50)
        print("    🎯 TRADING ACES 🎯")
        print("="*50)
        print("Loading game... Please wait.")
        print("This may take a few seconds on first startup.")
        print("="*50 + "\n")
    
    def init_pygame_minimal(self):
        """Initialize minimal pygame for loading screen"""
        if not PYGAME_AVAILABLE:
            return None
            
        try:
            pygame.init()
            
            # Get monitor info
            info = pygame.display.Info()
            width, height = info.current_w, info.current_h
            
            # Create fullscreen window
            screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
            pygame.display.set_caption("Trading Aces - Loading...")
            
            return screen
        except Exception as e:
            print(f"Could not initialize pygame for loading screen: {e}")
            return None
    
    def draw_loading_screen(self, screen):
        """Draw the graphical loading screen"""
        if not screen:
            return
            
        try:
            # Colors
            bg_color = (8, 56, 45)  # Same as game background
            text_color = (220, 220, 220)
            accent_color = (0, 255, 150)
            progress_bg = (40, 40, 40)
            
            width, height = screen.get_size()
            
            # Fill background
            screen.fill(bg_color)
            
            # Initialize font (use default pygame font)
            try:
                title_font = pygame.font.Font(None, 72)
                text_font = pygame.font.Font(None, 36)
                step_font = pygame.font.Font(None, 28)
            except:
                # Fallback to system default
                title_font = pygame.font.SysFont('Arial', 72)
                text_font = pygame.font.SysFont('Arial', 36)
                step_font = pygame.font.SysFont('Arial', 28)
            
            # Draw title
            title_text = title_font.render("TRADING ACES", True, accent_color)
            title_rect = title_text.get_rect(center=(width//2, height//2 - 150))
            screen.blit(title_text, title_rect)
            
            # Draw subtitle
            subtitle_text = text_font.render("Stock Market Trading Simulator", True, text_color)
            subtitle_rect = subtitle_text.get_rect(center=(width//2, height//2 - 100))
            screen.blit(subtitle_text, subtitle_rect)
            
            # Draw current loading step
            step_text = step_font.render(self.current_step, True, text_color)
            step_rect = step_text.get_rect(center=(width//2, height//2 - 30))
            screen.blit(step_text, step_rect)
            
            # Draw progress bar
            progress_width = 400
            progress_height = 20
            progress_x = width//2 - progress_width//2
            progress_y = height//2 + 20
            
            # Progress bar background
            pygame.draw.rect(screen, progress_bg, 
                           (progress_x, progress_y, progress_width, progress_height))
            
            # Progress bar fill
            progress_fill = (self.steps_completed / self.total_steps) * progress_width
            pygame.draw.rect(screen, accent_color, 
                           (progress_x, progress_y, progress_fill, progress_height))
            
            # Progress bar border
            pygame.draw.rect(screen, text_color, 
                           (progress_x, progress_y, progress_width, progress_height), 2)
            
            # Draw percentage
            percentage = int((self.steps_completed / self.total_steps) * 100)
            percent_text = step_font.render(f"{percentage}%", True, text_color)
            percent_rect = percent_text.get_rect(center=(width//2, height//2 + 60))
            screen.blit(percent_text, percent_rect)
            
            # Draw elapsed time
            elapsed = time.time() - self.start_time
            time_text = step_font.render(f"Elapsed: {elapsed:.1f}s", True, text_color)
            time_rect = time_text.get_rect(center=(width//2, height//2 + 90))
            screen.blit(time_text, time_rect)
            
            # Draw loading animation (spinning dots)
            self.draw_loading_animation(screen, width//2, height//2 + 130, accent_color)
            
            pygame.display.flip()
            
        except Exception as e:
            print(f"Error drawing loading screen: {e}")
    
    def draw_loading_animation(self, screen, center_x, center_y, color):
        """Draw animated loading dots"""
        try:
            # Rotating dots animation
            dots = 8
            radius = 30
            dot_size = 4
            time_offset = time.time() * 3  # Animation speed
            
            for i in range(dots):
                angle = (2 * 3.14159 * i / dots) + time_offset
                x = center_x + int(radius * pygame.math.cos(angle))
                y = center_y + int(radius * pygame.math.sin(angle))
                
                # Fade dots based on position
                alpha = int(255 * (0.3 + 0.7 * ((i + time_offset) % dots) / dots))
                dot_color = (*color[:3], min(255, alpha))
                
                pygame.draw.circle(screen, color, (x, y), dot_size)
                
        except Exception as e:
            print(f"Error drawing animation: {e}")
    
    def update_step(self, step_index, custom_message=None):
        """Update the current loading step"""
        if step_index < len(self.loading_steps):
            self.current_step = custom_message or self.loading_steps[step_index]
            self.steps_completed = step_index
            print(f"[{step_index+1}/{self.total_steps}] {self.current_step}")
    
    def finish_loading(self):
        """Mark loading as complete"""
        self.loading = False
        self.steps_completed = self.total_steps
        elapsed = time.time() - self.start_time
        print(f"\nGame loaded successfully in {elapsed:.2f} seconds!")

# Global loading screen instance
_loading_screen = None

def show_loading_screen():
    """Initialize and show the loading screen"""
    global _loading_screen
    _loading_screen = LoadingScreen()
    
    # Show immediate console feedback
    _loading_screen.show_console_loading()
    
    # Try to show graphical loading screen
    screen = _loading_screen.init_pygame_minimal()
    
    if screen:
        # Draw initial loading screen
        _loading_screen.draw_loading_screen(screen)
        
        # Return screen for updates during loading
        return screen, _loading_screen
    else:
        # Fallback to console only
        return None, _loading_screen

def update_loading_step(step_index, custom_message=None):
    """Update loading step (can be called from main loading process)"""
    global _loading_screen
    if _loading_screen:
        _loading_screen.update_step(step_index, custom_message)

def update_loading_display(screen):
    """Update the loading display (call this periodically during loading)"""
    global _loading_screen
    if _loading_screen and screen:
        # Handle pygame events to prevent "not responding"
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        except:
            pass
        
        _loading_screen.draw_loading_screen(screen)

def finish_loading():
    """Finish the loading process"""
    global _loading_screen
    if _loading_screen:
        _loading_screen.finish_loading()
