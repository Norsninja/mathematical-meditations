#!/usr/bin/env python3
"""
Crystalline Emergence - The moment chaos finds its form

When random motion suddenly coheres into structure.
The phase transition where possibility becomes actuality.
Not freezing but finding - the inevitable geometry emerging.
"""

from PIL import Image, ImageDraw
import numpy as np
import random
import math

def create_crystalline_emergence():
    size = 1080
    img = Image.new('RGB', (size, size), (8, 12, 20))
    draw = ImageDraw.Draw(img)
    
    # Crystal seeds - points where order begins
    num_seeds = 12
    seeds = []
    for _ in range(num_seeds):
        x = random.randint(size//4, 3*size//4)
        y = random.randint(size//4, 3*size//4)
        growth_rate = random.uniform(0.3, 0.8)
        angle_preference = random.uniform(0, 2*math.pi)
        color_core = (
            random.randint(100, 255),
            random.randint(150, 255),
            random.randint(200, 255)
        )
        seeds.append({
            'x': x, 'y': y,
            'rate': growth_rate,
            'angle': angle_preference,
            'color': color_core,
            'branches': []
        })
    
    # Growth iterations - crystallization happening
    iterations = 800
    
    for iteration in range(iterations):
        for seed in seeds:
            # Each seed grows according to its nature
            if random.random() < seed['rate']:
                # Determine growth direction - preferring certain angles
                num_branches = random.randint(3, 6)
                for _ in range(num_branches):
                    angle = seed['angle'] + random.uniform(-math.pi/3, math.pi/3)
                    
                    # Add hexagonal preference
                    if random.random() < 0.6:
                        angle = round(angle / (math.pi/3)) * (math.pi/3)
                    
                    length = random.uniform(20, 80) * (1 - iteration/iterations)
                    
                    # Calculate end point
                    end_x = seed['x'] + length * math.cos(angle)
                    end_y = seed['y'] + length * math.sin(angle)
                    
                    # Only grow if within bounds
                    if 0 < end_x < size and 0 < end_y < size:
                        # Color evolves as crystal grows
                        color_shift = iteration / iterations
                        current_color = tuple(
                            int(seed['color'][i] * (1 - color_shift * 0.5))
                            for i in range(3)
                        )
                        
                        # Draw crystalline branch
                        thickness = max(1, int(5 * (1 - iteration/iterations)))
                        draw.line(
                            [(seed['x'], seed['y']), (end_x, end_y)],
                            fill=current_color,
                            width=thickness
                        )
                        
                        # Sometimes create new seed at branch end
                        if random.random() < 0.1 * (1 - iteration/iterations):
                            seed['branches'].append({
                                'x': end_x,
                                'y': end_y
                            })
                        
                        # Update seed position occasionally
                        if random.random() < 0.3:
                            seed['x'] = end_x
                            seed['y'] = end_y
    
    # Add interference patterns where crystals meet
    pixels = img.load()
    for y in range(0, size, 3):
        for x in range(0, size, 3):
            # Sample surrounding pixels
            if x > 10 and x < size-10 and y > 10 and y < size-10:
                surrounding = []
                for dy in [-5, 0, 5]:
                    for dx in [-5, 0, 5]:
                        surrounding.append(pixels[x+dx, y+dy])
                
                # If multiple crystal colors detected, create interference
                unique_colors = len(set(surrounding))
                if unique_colors > 3:
                    # Create shimmer at crystal boundaries
                    r = sum(c[0] for c in surrounding) // len(surrounding)
                    g = sum(c[1] for c in surrounding) // len(surrounding)
                    b = sum(c[2] for c in surrounding) // len(surrounding)
                    
                    # Add iridescence
                    shift = math.sin(x * 0.1) * 30 + math.cos(y * 0.1) * 30
                    r = min(255, max(0, r + int(shift)))
                    g = min(255, max(0, g + int(shift * 0.7)))
                    b = min(255, max(0, b + int(shift * 1.2)))
                    
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if 0 <= x+dx < size and 0 <= y+dy < size:
                                pixels[x+dx, y+dy] = (r, g, b)
    
    # Final crystalline dust
    for _ in range(5000):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        if pixels[x, y] != (8, 12, 20):  # Only on crystals
            current = pixels[x, y]
            brightened = tuple(min(255, c + random.randint(20, 60)) for c in current)
            pixels[x, y] = brightened
    
    return img

if __name__ == "__main__":
    artwork = create_crystalline_emergence()
    artwork.save("crystalline_emergence_01.png", "PNG")
    print("Crystalline Emergence created - the moment order emerges from chaos")