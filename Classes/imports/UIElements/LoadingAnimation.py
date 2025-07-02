import pygame
import math
import time
from Defs import drawCenterTxt, s_render

class LoadingAnimation:
    """
    A loading animation that displays when creating a new game and filling graph points.
    Features multiple animation types: spinning circle, pulsing dots, and progress bar.
    """
    
    def __init__(self):
        self.start_time = None
        self.animation_type = "spinning_circle"  # "spinning_circle", "pulsing_dots", "progress_bar"
        self.is_active = False
        self.progress = 0.0  # 0.0 to 1.0
        self.message = "Creating New Game..."
        self.sub_message = "Initializing stock data..."
        
        # Animation parameters
        self.circle_angle = 0
        self.pulse_time = 0
        self.dot_count = 5
        
        # Colors
        self.primary_color = (0, 150, 255)
        self.secondary_color = (100, 200, 255)
        self.background_color = (40, 40, 40, 220)
        self.text_color = (255, 255, 255)
        
    def start(self, message="Creating New Game...", sub_message="Initializing stock data..."):
        """Start the loading animation"""
        self.is_active = True
        self.start_time = time.time()
        self.message = message
        self.sub_message = sub_message
        self.progress = 0.0
        self.circle_angle = 0
        self.pulse_time = 0
        
    def stop(self):
        """Stop the loading animation"""
        self.is_active = False
        self.progress = 1.0
        
    def set_progress(self, progress, sub_message=None):
        """Update the progress (0.0 to 1.0) and optionally the sub-message"""
        self.progress = max(0.0, min(1.0, progress))
        if sub_message:
            self.sub_message = sub_message
            
    def update(self):
        """Update the animation state"""
        if not self.is_active:
            return
            
        current_time = time.time()
        elapsed = current_time - self.start_time if self.start_time else 0
        
        # Update animation parameters
        self.circle_angle = (elapsed * 180) % 360  # 180 degrees per second
        self.pulse_time = elapsed
        
    def draw_spinning_circle(self, screen, center_x, center_y, radius=40):
        """Draw a spinning circle animation"""
        # Draw background circle
        pygame.draw.circle(screen, (80, 80, 80), (center_x, center_y), radius, 3)
        
        # Draw spinning arc
        arc_length = 90  # degrees
        start_angle = math.radians(self.circle_angle)
        end_angle = math.radians(self.circle_angle + arc_length)
        
        # Create points for the arc
        points = []
        num_points = 20
        for i in range(num_points):
            angle = start_angle + (end_angle - start_angle) * i / (num_points - 1)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
            
        # Draw the spinning arc
        if len(points) > 1:
            for i in range(len(points) - 1):
                alpha = int(255 * (i / len(points)))
                color = (*self.primary_color, alpha)
                
                # Create a surface for the line with alpha
                line_surf = pygame.Surface((5, 5), pygame.SRCALPHA)
                pygame.draw.circle(line_surf, color, (2, 2), 2)
                screen.blit(line_surf, (points[i][0] - 2, points[i][1] - 2))
                
    def draw_pulsing_dots(self, screen, center_x, center_y):
        """Draw pulsing dots animation"""
        dot_spacing = 15
        total_width = (self.dot_count - 1) * dot_spacing
        start_x = center_x - total_width // 2
        
        for i in range(self.dot_count):
            x = start_x + i * dot_spacing
            
            # Calculate pulse phase for this dot
            phase_offset = i * 0.5  # Stagger the pulses
            pulse_phase = (self.pulse_time * 3 + phase_offset) % (math.pi * 2)
            
            # Calculate radius based on pulse
            base_radius = 4
            pulse_radius = 2 * (math.sin(pulse_phase) * 0.5 + 0.5)
            radius = base_radius + pulse_radius
            
            # Calculate alpha based on pulse
            alpha = int(100 + 155 * (math.sin(pulse_phase) * 0.5 + 0.5))
            
            # Draw the dot
            color = (*self.primary_color, alpha)
            dot_surf = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(dot_surf, color, (radius + 1, radius + 1), int(radius))
            screen.blit(dot_surf, (x - radius - 1, center_y - radius - 1))
            
    def draw_progress_bar(self, screen, center_x, center_y, width=300, height=8):
        """Draw a progress bar"""
        # Background bar
        bar_rect = pygame.Rect(center_x - width // 2, center_y - height // 2, width, height)
        pygame.draw.rect(screen, (80, 80, 80), bar_rect, border_radius=height // 2)
        
        # Progress fill
        if self.progress > 0:
            fill_width = int(width * self.progress)
            fill_rect = pygame.Rect(center_x - width // 2, center_y - height // 2, fill_width, height)
            pygame.draw.rect(screen, self.primary_color, fill_rect, border_radius=height // 2)
            
        # Progress text
        progress_text = f"{int(self.progress * 100)}%"
        drawCenterTxt(screen, progress_text, 24, self.text_color, (center_x, center_y + 25))
        
    def draw(self, screen, center_pos=None):
        """Draw the loading animation"""
        if not self.is_active:
            return
            
        # Default center position
        if center_pos is None:
            center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
        else:
            center_x, center_y = center_pos
            
        # Draw semi-transparent background overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill(self.background_color)
        screen.blit(overlay, (0, 0))
        
        # Draw background box
        box_width, box_height = 500, 260
        box_rect = pygame.Rect(center_x - box_width // 2, center_y - box_height // 2, box_width, box_height)
        pygame.draw.rect(screen, (60, 60, 60), box_rect, border_radius=15)
        pygame.draw.rect(screen, (120, 120, 120), box_rect, 3, border_radius=15)
        
        # Draw main message
        drawCenterTxt(screen, self.message, 52, self.text_color, (center_x, center_y - 90))
        
        # Draw animation based on type
        if self.animation_type == "spinning_circle":
            self.draw_spinning_circle(screen, center_x, center_y - 10)
        elif self.animation_type == "pulsing_dots":
            self.draw_pulsing_dots(screen, center_x, center_y - 10)
        elif self.animation_type == "progress_bar":
            self.draw_progress_bar(screen, center_x, center_y - 10)
            
        # Draw sub-message
        drawCenterTxt(screen, self.sub_message, 36, (200, 200, 200), (center_x, center_y + 70))

    def set_animation_type(self, animation_type):
        """Change the animation type"""
        if animation_type in ["spinning_circle", "pulsing_dots", "progress_bar"]:
            self.animation_type = animation_type
