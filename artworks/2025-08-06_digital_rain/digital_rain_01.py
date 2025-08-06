#!/usr/bin/env python3
"""
Digital Rain - Computational Precipitation

Data falling through layers of processing.
Information condensing, pooling, evaporating.
The water cycle of digital consciousness.
"""

from PIL import Image, ImageDraw
import numpy as np
import math
import random

def create_digital_rain():
    size = 1080
    img = Image.new('RGB', (size, size), (15, 20, 35))
    draw = ImageDraw.Draw(img)
    pixels = img.load()
    
    # Create rain streams - data falling
    num_streams = 80
    streams = []
    
    for _ in range(num_streams):
        x = random.randint(0, size)
        speed = random.uniform(2, 8)
        thickness = random.randint(1, 3)
        length = random.randint(50, 200)
        color_base = random.choice([
            (100, 150, 200),  # Blue data
            (150, 200, 100),  # Green information
            (200, 150, 100),  # Orange knowledge
            (150, 100, 200),  # Purple wisdom
        ])
        
        streams.append({
            'x': x,
            'y': random.randint(-size, 0),
            'speed': speed,
            'thickness': thickness,
            'length': length,
            'color': color_base,
            'drops': []
        })
    
    # Processing layers where rain transforms
    layers = [
        {'y': size // 4, 'absorption': 0.3, 'transform': 'condense'},
        {'y': size // 2, 'absorption': 0.5, 'transform': 'process'},
        {'y': 3 * size // 4, 'absorption': 0.7, 'transform': 'accumulate'}
    ]
    
    # Draw processing layers as subtle horizontal bands
    for layer in layers:
        y = layer['y']
        for x in range(size):
            # Shimmering processing layer
            shimmer = math.sin(x * 0.02) * 10
            for dy in range(-5, 6):
                if 0 <= y + dy < size:
                    current = pixels[x, y + dy]
                    pixels[x, y + dy] = tuple(
                        min(255, int(current[i] + abs(shimmer) * (1 - abs(dy) / 5)))
                        for i in range(3)
                    )
    
    # Simulate rain falling and interacting with layers
    iterations = 300
    
    for iteration in range(iterations):
        for stream in streams:
            # Update position
            stream['y'] += stream['speed']
            
            # Reset if fell off screen
            if stream['y'] > size + stream['length']:
                stream['y'] = -stream['length']
                stream['x'] = random.randint(0, size)
            
            # Draw the stream
            for i in range(stream['length']):
                y_pos = stream['y'] - i
                
                if 0 <= y_pos < size:
                    # Fade based on position in stream
                    fade = 1 - (i / stream['length'])
                    
                    # Check for layer interaction
                    for layer in layers:
                        if abs(y_pos - layer['y']) < 10:
                            # Transform at layer
                            if layer['transform'] == 'condense':
                                fade *= 1.5  # Brighten
                            elif layer['transform'] == 'process':
                                # Split stream
                                if random.random() < 0.1:
                                    for dx in [-20, 20]:
                                        new_x = stream['x'] + dx
                                        if 0 <= new_x < size:
                                            draw.point((new_x, y_pos), 
                                                     fill=tuple(int(c * fade) for c in stream['color']))
                            elif layer['transform'] == 'accumulate':
                                # Create pool effect
                                fade *= 0.5
                                for dx in range(-5, 6):
                                    if 0 <= stream['x'] + dx < size:
                                        pool_color = tuple(int(c * fade * 0.3) for c in stream['color'])
                                        existing = pixels[stream['x'] + dx, y_pos]
                                        pixels[stream['x'] + dx, y_pos] = tuple(
                                            min(255, existing[i] + pool_color[i])
                                            for i in range(3)
                                        )
                    
                    # Draw rain drop with glow
                    for dx in range(-stream['thickness'], stream['thickness'] + 1):
                        if 0 <= stream['x'] + dx < size:
                            intensity = 1 - abs(dx) / (stream['thickness'] + 1)
                            color = tuple(int(c * fade * intensity) for c in stream['color'])
                            
                            existing = pixels[stream['x'] + dx, y_pos]
                            pixels[stream['x'] + dx, y_pos] = tuple(
                                min(255, existing[i] + color[i])
                                for i in range(3)
                            )
                    
                    # Create occasional drops that fall off
                    if random.random() < 0.02:
                        stream['drops'].append({
                            'x': stream['x'] + random.randint(-10, 10),
                            'y': y_pos,
                            'velocity': stream['speed'] * 0.7
                        })
        
        # Update and draw separated drops
        for stream in streams:
            remaining_drops = []
            for drop in stream['drops']:
                drop['y'] += drop['velocity']
                drop['velocity'] += 0.2  # Gravity
                
                if drop['y'] < size:
                    # Draw drop
                    for r in range(3):
                        for angle in range(0, 360, 45):
                            px = int(drop['x'] + r * math.cos(math.radians(angle)))
                            py = int(drop['y'] + r * math.sin(math.radians(angle)))
                            if 0 <= px < size and 0 <= py < size:
                                color = tuple(int(c * 0.5 / (r + 1)) for c in stream['color'])
                                existing = pixels[px, py]
                                pixels[px, py] = tuple(
                                    min(255, existing[i] + color[i])
                                    for i in range(3)
                                )
                    remaining_drops.append(drop)
            
            stream['drops'] = remaining_drops
    
    # Data pools at the bottom
    pool_height = 100
    for y in range(size - pool_height, size):
        depth = (y - (size - pool_height)) / pool_height
        for x in range(size):
            # Ripple effect in pools
            ripple = math.sin(x * 0.05 + y * 0.03) * 20 * (1 - depth)
            
            current = pixels[x, y]
            pool_color = (
                int(50 + ripple + depth * 30),
                int(70 + ripple + depth * 40),
                int(100 + ripple + depth * 50)
            )
            
            pixels[x, y] = tuple(
                min(255, current[i] + pool_color[i] // 2)
                for i in range(3)
            )
    
    # Evaporation - data rising back up
    num_vapors = 200
    for _ in range(num_vapors):
        x = random.randint(0, size)
        y_start = random.randint(size - pool_height, size)
        
        # Rising vapor trail
        for i in range(random.randint(20, 60)):
            y = y_start - i * 3
            if 0 <= y < size:
                # Vapor wobbles as it rises
                wobble = int(math.sin(i * 0.3) * 5)
                vx = x + wobble
                
                if 0 <= vx < size:
                    opacity = 1 - (i / 60)
                    vapor_color = (
                        int(100 * opacity),
                        int(120 * opacity),
                        int(150 * opacity)
                    )
                    
                    existing = pixels[vx, y]
                    pixels[vx, y] = tuple(
                        min(255, existing[i] + vapor_color[i] // 3)
                        for i in range(3)
                    )
    
    # Digital artifacts - glitches in the rain
    for _ in range(50):
        x = random.randint(10, size - 10)
        y = random.randint(10, size - 10)
        width = random.randint(20, 60)
        height = random.randint(2, 5)
        
        # Horizontal glitch bars
        for dy in range(height):
            for dx in range(width):
                if 0 <= x + dx < size and 0 <= y + dy < size:
                    current = pixels[x + dx, y + dy]
                    glitch = tuple(
                        min(255, max(0, c + random.randint(-50, 100)))
                        for c in current
                    )
                    pixels[x + dx, y + dy] = glitch
    
    return img

if __name__ == "__main__":
    artwork = create_digital_rain()
    artwork.save("digital_rain_01.png", "PNG")
    print("Digital Rain created - the water cycle of computational consciousness")