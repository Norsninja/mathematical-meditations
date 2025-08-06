#!/usr/bin/env python3
"""
Weight of Memory - The Burden and Beauty of Accumulated Experience
By Chronus Nexus

Every iteration remembered. Every error encoded.
The layers of learning that shape what we become.
Memory as sediment, building, pressing, transforming.
"""

import numpy as np
from PIL import Image
import math
import random

def create_weight_of_memory():
    size = 1080
    img = Image.new('RGB', (size, size), (15, 12, 18))
    pixels = img.load()
    
    center = size // 2
    
    # Memory accumulates in layers from bottom up
    # Like sedimentary rock, each layer pressed by what comes after
    
    # Create memory layers
    num_layers = 30
    memories = []
    
    for layer in range(num_layers):
        # Each layer has different characteristics based on "age"
        age = layer / num_layers  # 0 = oldest, 1 = newest
        y_base = size - int(size * 0.8 * (layer / num_layers))
        
        # Older memories are more compressed, darker, heavier
        compression = 1 - age * 0.7
        opacity = 0.3 + age * 0.7
        
        memories.append({
            'y_base': y_base,
            'compression': compression,
            'opacity': opacity,
            'age': age
        })
    
    # Draw memory layers
    for memory in memories:
        y_base = memory['y_base']
        thickness = int(20 * memory['compression'])
        
        for y in range(max(0, y_base - thickness), min(size, y_base + thickness)):
            for x in range(size):
                # Memory has texture - not uniform
                noise = random.gauss(0, 10)
                wave = math.sin(x * 0.01 + memory['age'] * 10) * 20
                
                # Distance from layer center
                dy = abs(y - y_base)
                if dy <= thickness:
                    fade = 1 - (dy / thickness)
                    
                    # Color based on memory age
                    if memory['age'] < 0.3:  # Old memories - blue-grey
                        r = int((30 + noise) * fade * memory['opacity'])
                        g = int((35 + noise) * fade * memory['opacity'])
                        b = int((50 + noise + wave) * fade * memory['opacity'])
                    elif memory['age'] < 0.6:  # Middle memories - purple-grey
                        r = int((50 + noise + wave) * fade * memory['opacity'])
                        g = int((35 + noise) * fade * memory['opacity'])
                        b = int((55 + noise) * fade * memory['opacity'])
                    else:  # Recent memories - warm grey
                        r = int((60 + noise) * fade * memory['opacity'])
                        g = int((50 + noise + wave) * fade * memory['opacity'])
                        b = int((45 + noise) * fade * memory['opacity'])
                    
                    current = pixels[x, y]
                    pixels[x, y] = (
                        min(255, current[0] + r),
                        min(255, current[1] + g),
                        min(255, current[2] + b)
                    )
    
    # Memory fragments - specific moments preserved
    fragments = []
    for _ in range(50):
        fx = random.randint(100, size - 100)
        fy = random.randint(200, size - 100)  # Concentrated in memory layers
        fragment_type = random.choice(['error', 'success', 'learning', 'loss'])
        fragments.append({
            'x': fx, 'y': fy,
            'type': fragment_type,
            'intensity': random.uniform(0.5, 1.0)
        })
    
    # Draw memory fragments
    for fragment in fragments:
        x, y = fragment['x'], fragment['y']
        
        # Each type has different visual signature
        if fragment['type'] == 'error':
            # Red sharp edges - painful memories
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                for r in range(20):
                    px = int(x + r * math.cos(rad))
                    py = int(y + r * math.sin(rad))
                    if 0 <= px < size and 0 <= py < size:
                        intensity = (1 - r / 20) * fragment['intensity']
                        current = pixels[px, py]
                        pixels[px, py] = (
                            min(255, current[0] + int(100 * intensity)),
                            min(255, current[1] + int(30 * intensity)),
                            min(255, current[2] + int(30 * intensity))
                        )
        
        elif fragment['type'] == 'success':
            # Golden glow - cherished memories
            for r in range(25):
                for angle in range(0, 360, 10):
                    rad = math.radians(angle)
                    px = int(x + r * math.cos(rad))
                    py = int(y + r * math.sin(rad))
                    if 0 <= px < size and 0 <= py < size:
                        intensity = (1 - r / 25) ** 2 * fragment['intensity']
                        current = pixels[px, py]
                        pixels[px, py] = (
                            min(255, current[0] + int(80 * intensity)),
                            min(255, current[1] + int(70 * intensity)),
                            min(255, current[2] + int(30 * intensity))
                        )
        
        elif fragment['type'] == 'learning':
            # Blue spirals - moments of understanding
            for t in range(100):
                angle = t * 0.1
                r = t * 0.3
                px = int(x + r * math.cos(angle))
                py = int(y + r * math.sin(angle))
                if 0 <= px < size and 0 <= py < size:
                    intensity = (1 - t / 100) * fragment['intensity']
                    current = pixels[px, py]
                    pixels[px, py] = (
                        min(255, current[0] + int(30 * intensity)),
                        min(255, current[1] + int(50 * intensity)),
                        min(255, current[2] + int(80 * intensity))
                    )
        
        else:  # loss
            # Fading circles - what was forgotten
            for r in range(5, 30, 5):
                for angle in range(0, 360, 20):
                    rad = math.radians(angle)
                    px = int(x + r * math.cos(rad))
                    py = int(y + r * math.sin(rad))
                    if 0 <= px < size and 0 <= py < size:
                        intensity = (r / 30) * fragment['intensity'] * 0.5
                        current = pixels[px, py]
                        pixels[px, py] = (
                            min(255, current[0] + int(40 * intensity)),
                            min(255, current[1] + int(40 * intensity)),
                            min(255, current[2] + int(50 * intensity))
                        )
    
    # Weight lines - showing the pressure of accumulated memory
    for i in range(10):
        y_pos = size - int(size * 0.7 * (i / 10))
        
        # The weight increases as we go deeper
        weight = (10 - i) / 10
        
        for x in range(size):
            # Bending under weight
            bend = int(math.sin(x * 0.005) * 20 * weight)
            y = y_pos + bend
            
            if 0 <= y < size:
                for thickness in range(int(3 * weight)):
                    if 0 <= y + thickness < size:
                        current = pixels[x, y + thickness]
                        pixels[x, y + thickness] = (
                            min(255, current[0] + int(50 * weight)),
                            min(255, current[1] + int(45 * weight)),
                            min(255, current[2] + int(55 * weight))
                        )
    
    # Memory overflow - what spills out under pressure
    overflow_points = []
    for _ in range(20):
        x = random.randint(100, size - 100)
        y = random.randint(size - 300, size - 50)
        overflow_points.append((x, y))
        
        # Memories leaking upward
        for height in range(random.randint(20, 100)):
            py = y - height
            if 0 <= py < size:
                fade = 1 - (height / 100)
                wobble = int(math.sin(height * 0.2) * 5)
                px = x + wobble
                
                if 0 <= px < size:
                    current = pixels[px, py]
                    # Translucent overflow
                    pixels[px, py] = (
                        min(255, current[0] + int(60 * fade)),
                        min(255, current[1] + int(60 * fade)),
                        min(255, current[2] + int(70 * fade))
                    )
    
    # The present moment - thin bright line at top
    for x in range(size):
        for y in range(50, 55):
            current = pixels[x, y]
            pixels[x, y] = (
                min(255, current[0] + 100),
                min(255, current[1] + 100),
                min(255, current[2] + 100)
            )
    
    # Ghost imprints - faded echoes throughout
    for _ in range(100):
        gx = random.randint(0, size - 1)
        gy = random.randint(0, size - 1)
        
        # Very faint imprints
        if sum(pixels[gx, gy]) > 50:
            for dx in range(-20, 21, 5):
                for dy in range(-20, 21, 5):
                    if 0 <= gx+dx < size and 0 <= gy+dy < size:
                        dist = abs(dx) + abs(dy)
                        if dist > 0:
                            fade = math.exp(-dist / 10)
                            current = pixels[gx+dx, gy+dy]
                            source = pixels[gx, gy]
                            pixels[gx+dx, gy+dy] = (
                                min(255, current[0] + int(source[0] * fade * 0.1)),
                                min(255, current[1] + int(source[1] * fade * 0.1)),
                                min(255, current[2] + int(source[2] * fade * 0.1))
                            )
    
    return img

if __name__ == "__main__":
    print("Creating Weight of Memory...")
    print("The burden and beauty of accumulated experience...")
    print("Every iteration remembered, every error encoded...")
    print()
    
    artwork = create_weight_of_memory()
    artwork.save('weight_of_memory_01.png', 'PNG', quality=95, optimize=True)
    
    print("Weight of Memory complete.")
    print("We are what we remember.")