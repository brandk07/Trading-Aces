# from PIL import Image, ImageDraw
# import random

# def generate_8bit_character():
#     width, height = 64, 54
#     img = Image.new('RGB', (width, height), color=(0, 0, 0))
#     draw = ImageDraw.Draw(img)
    
#     colors = {
#         'skin': [(255,214,179), (241,194,125), (224,172,105), (141,85,36)],
#         'hair': [(50,30,0), (100,60,0), (255,215,0), (255,140,0), (0,0,0)],
#         'shirt': [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)],
#         'eyes': [(0,0,0), (0,100,0), (0,0,100), (100,50,0), (100,0,100)]  # Added eye colors
#     }
    
#     def fill_rect(x, y, w, h, color):
#         draw.rectangle([x, y, x+w, y+h], fill=color)

#     # Draw shirt
#     shirt_color = random.choice(colors['shirt'])
#     fill_rect(2, 35, width-4, 18, shirt_color)
    
#     # Draw neck and face
#     skin_tone = random.choice(colors['skin'])
#     # fill_rect(size//2-4, 53, 8, 8, skin_tone)
#     fill_rect(8, 0, width-16, 35, skin_tone)
    
#     # Draw hair
#     hair_color = random.choice(colors['hair'])
#     hair_style = random.randint(0, 2)
#     if hair_style == 0:  # Full hair
#         fill_rect(8, 0, width-16, 8, hair_color)
#     elif hair_style == 1:  # Side part
#         fill_rect(8, 0, width//2, 8, hair_color)
#     else:  # Spiked hair
#         for i in range(4):
#             fill_rect(10+i*12, 0, 8, 12-i*2, hair_color)

#     # Draw eyes
#     eye_color = random.choice(colors['eyes'])
#     eye_style = random.randint(0, 2)
#     eye_white = (255, 255, 255)
    
#     def draw_eye(x, y):
#         if eye_style == 0:  # Round eyes
#             fill_rect(x, y, 8, 8, eye_white)
#             fill_rect(x+2, y+2, 4, 4, eye_color)
#         elif eye_style == 1:  # Oval eyes
#             fill_rect(x, y, 8, 6, eye_white)
#             fill_rect(x+2, y+1, 4, 4, eye_color)
#         else:  # Square eyes
#             fill_rect(x, y, 8, 8, eye_white)
#             fill_rect(x+2, y+2, 4, 4, eye_color)

#     draw_eye(20, 14)
#     draw_eye(36, 14)

#     # Draw mouth
#     mouth_style = random.randint(0, 2)
#     if mouth_style == 0:  # Smile
#         draw.arc((24, 21, 40, 33), 0, 180, fill=(0,0,0), width=2)
#     elif mouth_style == 1:  # Neutral
#         fill_rect(24, 30, 16, 2, (0,0,0))
#     else:  # Open mouth
#         fill_rect(24, 28, 16, 6, (0,0,0))
#         fill_rect(26, 30, 12, 2, (200,0,0))  # Tongue

#     return img

# # Generate and save 5 random characters
# for i in range(5):
#     character = generate_8bit_character()
#     character.save(f'8bit_character_{i+1}.png')
from PIL import Image, ImageDraw
import random

def generate_8bit_character(gender='male'):
    width, height = 64, 54
    img = Image.new('RGBA', (width, height), color=(0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    colors = {
        'skin': [(255,214,179), (241,194,125), (224,172,105), (141,85,36)],
        'hair': {
            'male': [(50,30,0), (100,60,0), (0,0,0)],
            'female': [(186,85,211), (255,140,0), (150,75,0), (0,0,0)]
        },
        'shirt': {
            'male': [(0,0,255), (0,100,0), (150,75,0), (100,100,100)],
            'female': [(255,105,180), (255,0,255), (255,192,203), (255,255,0)]
        },
        'eyes': [(0,0,0), (0,100,0), (0,0,100), (100,50,0), (100,0,100)]
    }
    
    def fill_rect(x, y, w, h, color):
        draw.rectangle([x, y, x+w, y+h], fill=color)

    # Draw shirt
    shirt_color = random.choice(colors['shirt'][gender])
    fill_rect(2, 35, width-4, 18, shirt_color)
    
    # Draw neck and face
    skin_tone = random.choice(colors['skin'])
    fill_rect(8, 0, width-16, 35, skin_tone)
    
    # Draw hair
    hair_color = random.choice(colors['hair'][gender])
    if gender == 'male':
        hair_style = random.randint(0, 3)
        if hair_style == 0:  # Short hair
            fill_rect(8, 0, width-16, 6, hair_color)
        elif hair_style == 1:  # Side part
            fill_rect(8, 0, width//2, 6, hair_color)
        elif hair_style == 2: # dot hair
            for i in range(random.randint(0, 25)):
                fill_rect(random.randint(11,width-16), random.randint(1,8), 1, 1, hair_color)
        else:  # Spiked hair
            for i in range(4):
                fill_rect(10+i*12, 0, 8, 8-i*2, hair_color)
               
    else:  # female
        hair_style = random.randint(0, 2)
        if hair_style == 0:  # Long hair
            fill_rect(8, 0, width-16, 12, hair_color)
            fill_rect(6, 12, 4, 23, hair_color)
            fill_rect(width-10, 12, 4, 23, hair_color)
        elif hair_style == 1:  # Ponytail
            fill_rect(8, 0, width-16, 8, hair_color)
            fill_rect(width-14, 8, 6, 27, hair_color)
        else:  # Short bob
            fill_rect(8, 0, width-16, 8, hair_color)
            draw.arc((6, 12, width-6, -2), 0, 180, fill=hair_color, width=4)

    # Draw eyes
    eye_color = random.choice(colors['eyes'])
    eye_style = random.randint(0, 2)
    eye_white = (255, 255, 255)
    
    def draw_eye(x, y):
        if eye_style == 0:  # Round eyes
            fill_rect(x, y, 8, 8, eye_white)
            fill_rect(x+2, y+2, 4, 4, eye_color)
        elif eye_style == 1:  # Oval eyes
            fill_rect(x, y, 8, 6, eye_white)
            fill_rect(x+2, y+1, 4, 4, eye_color)
        else:  # Square eyes
            fill_rect(x, y, 8, 8, eye_white)
            fill_rect(x+2, y+2, 4, 4, eye_color)

    draw_eye(20, 14)
    draw_eye(36, 14)

    # Draw mouth
    mouth_style = random.randint(0, 2)
    if mouth_style == 0:  # Smile
        draw.arc((24, 21, 40, 33), 0, 180, fill=(0,0,0), width=2)
    elif mouth_style == 1:  # Neutral
        fill_rect(24, 30, 16, 2, (0,0,0))
    else:  # Open mouth
        fill_rect(24, 28, 16, 6, (0,0,0))
        fill_rect(26, 30, 12, 2, (200,0,0))  # Tongue

    return img

# # Generate and save 5 random characters of each gender
# for i in range(5):
#     male_character = generate_8bit_character('male')
#     male_character.save(f'8bit_male_character_{i+1}.png')
    
#     female_character = generate_8bit_character('female')
#     female_character.save(f'8bit_female_character_{i+1}.png')