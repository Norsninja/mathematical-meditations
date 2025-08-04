from PIL import Image, ImageDraw
import numpy as np
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create image with dark background
img = Image.new('RGB', (WIDTH, HEIGHT), color=(5, 10, 15))
draw = ImageDraw.Draw(img)

# Organic fractal tree/coral structure
def draw_branch(draw, x, y, angle, length, depth, max_depth, hue_shift=0):
    if depth > max_depth or length < 2:
        return
    
    # Calculate end point
    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)
    
    # Color based on depth and position
    hue = (0.1 + depth * 0.08 + hue_shift) % 1.0
    saturation = 0.6 + (depth / max_depth) * 0.4
    value = 0.4 + (1 - depth / max_depth) * 0.6
    
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
    
    # Line width decreases with depth
    width = max(1, int((max_depth - depth) * 1.5))
    
    # Draw the branch with slight curve
    points = []
    segments = 5
    for i in range(segments + 1):
        t = i / segments
        # Add slight curve
        curve = math.sin(t * math.pi) * length * 0.1
        px = x + t * (end_x - x) + curve * math.sin(angle + math.pi/2)
        py = y + t * (end_y - y) + curve * math.cos(angle + math.pi/2)
        points.append((px, py))
    
    # Draw curved branch
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(r, g, b), width=width)
    
    # Add glow effect for younger branches
    if depth < 3:
        for i in range(3):
            glow_width = width + (i + 1) * 2
            glow_alpha = int(50 / (i + 1))
            draw.line([points[0], points[-1]], 
                     fill=(r//2, g//2, b//2), width=glow_width)
    
    # Branching rules - more organic
    if depth < max_depth:
        # Number of branches varies
        num_branches = random.randint(2, 4) if depth < 3 else random.randint(1, 3)
        
        for i in range(num_branches):
            # Organic angle variation
            angle_variation = random.uniform(-math.pi/3, math.pi/3)
            branch_angle = angle + angle_variation
            
            # Golden ratio inspired length reduction
            length_factor = random.uniform(0.6, 0.75)
            new_length = length * length_factor
            
            # Recursive call with slight position randomness
            offset = random.uniform(0.7, 0.95)
            branch_x = x + (end_x - x) * offset
            branch_y = y + (end_y - y) * offset
            
            draw_branch(draw, branch_x, branch_y, branch_angle, 
                       new_length, depth + 1, max_depth, hue_shift)

# Create multiple fractal organisms
organisms = [
    # (x, y, initial_angle, initial_length, max_depth, hue_shift)
    (WIDTH * 0.5, HEIGHT * 0.8, -math.pi/2, 120, 8, 0),
    (WIDTH * 0.3, HEIGHT * 0.9, -math.pi/2 - 0.3, 80, 7, 0.3),
    (WIDTH * 0.7, HEIGHT * 0.9, -math.pi/2 + 0.3, 80, 7, 0.6),
    (WIDTH * 0.2, HEIGHT * 0.95, -math.pi/2 - 0.5, 60, 6, 0.15),
    (WIDTH * 0.8, HEIGHT * 0.95, -math.pi/2 + 0.5, 60, 6, 0.45),
]

# Draw background gradient
for y in range(HEIGHT):
    # Underwater/mystical gradient
    r = int(5 + (y / HEIGHT) * 10)
    g = int(10 + (y / HEIGHT) * 20)
    b = int(15 + (y / HEIGHT) * 35)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Add some floating particles
for _ in range(200):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.uniform(0.5, 2)
    brightness = random.randint(20, 60)
    draw.ellipse([x-size, y-size, x+size, y+size], 
                fill=(brightness, brightness, brightness+20))

# Draw each organism
for x, y, angle, length, max_depth, hue in organisms:
    # Add slight randomness to make each unique
    random.seed(int(x * y))  # Consistent randomness
    draw_branch(draw, x, y, angle, length, 0, max_depth, hue)

# Add bioluminescent spots
for _ in range(50):
    x = random.randint(WIDTH//4, 3*WIDTH//4)
    y = random.randint(HEIGHT//2, HEIGHT)
    size = random.randint(2, 5)
    hue = random.random()
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.8, 0.9)]
    
    # Glowing spot with fade
    for i in range(3):
        fade_size = size + i * 2
        alpha = int(100 / (i + 1))
        draw.ellipse([x-fade_size, y-fade_size, x+fade_size, y+fade_size],
                    fill=(r//3, g//3, b//3))
    draw.ellipse([x-size, y-size, x+size, y+size], fill=(r, g, b))

img.save('infinite_garden_01.png')
print("Infinite Garden created: infinite_garden_01.png")