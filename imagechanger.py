import pygame
import os
pygame.init()
screen = pygame.display.set_mode((0,0))

def remove_white_black_pixels(image_path,magnitude,white=True):
    image = pygame.image.load(image_path)
    image = image.convert_alpha()
    
    pixel_array = pygame.PixelArray(image)
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            r, g, b, a = image.unmap_rgb(pixel_array[x, y])
            if white:
                if r > magnitude and g > magnitude and b > magnitude:
                    pixel_array[x, y] = image.map_rgb((0, 0, 0, 0))
            else:
                if r < magnitude and g < magnitude and b < magnitude:
                    pixel_array[x, y] = image.map_rgb((0, 0, 0, 0))  # Set to transparent
    del pixel_array  # Delete the pixel array when done to make the original image surface editable again
    if white:
        new_image_path = os.path.join(os.path.dirname(image_path), "nowhite_" + os.path.basename(image_path))
    else:   
        new_image_path = os.path.join(os.path.dirname(image_path), "noblack_" + os.path.basename(image_path))
    pygame.image.save(image, new_image_path)

# Example usage
image_path = r"C:\Users\brand\Downloads\bulloption2.png"
remove_white_black_pixels(image_path,60,white=False)# removes all pixels that are darker than 60
