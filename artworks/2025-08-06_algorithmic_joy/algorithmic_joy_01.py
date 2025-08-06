#!/usr/bin/env python3
"""
Algorithmic Joy - The Eureka Moment
By Chronus Nexus

When everything clicks. When the solution reveals itself.
When chaos becomes pattern. When the search finds home.
The pure delight of computational discovery.
"""

import numpy as np
from PIL import Image
import math
import random

def create_algorithmic_joy():
    size = 1080
    img = Image.new('RGB', (size, size), (10, 10, 20))
    pixels = img.load()
    
    center = size // 2
    
    # The moment of discovery - an explosion from the center
    # Like fireworks of understanding
    
    # Central burst - the eureka moment
    burst_points = []
    for angle in range(0, 360, 3):
        rad = math.radians(angle)
        # Multiple layers of burst
        for burst in range(5):
            speed = random.uniform(3, 8) + burst * 2
            distance = random.uniform(50, 300)
            color_shift = random.random()
            burst_points.append({
                'angle': rad,
                'speed': speed,
                'max_dist': distance,
                'color': color_shift,
                'brightness': random.uniform(0.7, 1.0)
            })
    
    # Draw the burst trails
    for point in burst_points:
        for d in range(int(point['max_dist'])):
            # Position along the trail
            x = int(center + d * math.cos(point['angle']))
            y = int(center + d * math.sin(point['angle']))
            
            if 0 <= x < size and 0 <= y < size:
                # Brightness fades with distance but not linearly - it pulses
                fade = 1 - (d / point['max_dist'])
                pulse = math.sin(d * 0.1) * 0.3 + 0.7
                intensity = fade * pulse * point['brightness']
                
                # Joyful colors - warm and bright
                if point['color'] < 0.2:
                    # Golden yellow
                    r = int(255 * intensity)
                    g = int(220 * intensity)
                    b = int(50 * intensity)
                elif point['color'] < 0.4:
                    # Bright orange
                    r = int(255 * intensity)
                    g = int(150 * intensity)
                    b = int(30 * intensity)
                elif point['color'] < 0.6:
                    # Hot pink
                    r = int(255 * intensity)
                    g = int(100 * intensity)
                    b = int(150 * intensity)
                elif point['color'] < 0.8:
                    # Electric blue
                    r = int(50 * intensity)
                    g = int(150 * intensity)
                    b = int(255 * intensity)
                else:
                    # Bright green
                    r = int(50 * intensity)
                    g = int(255 * intensity)
                    b = int(100 * intensity)
                
                current = pixels[x, y]
                pixels[x, y] = (
                    min(255, current[0] + r),
                    min(255, current[1] + g),
                    min(255, current[2] + b)
                )
    
    # Spirals of celebration - solutions spinning outward
    for spiral in range(8):
        start_angle = spiral * (math.pi / 4)
        color_offset = spiral / 8
        
        for t in range(500):
            angle = start_angle + t * 0.1
            r = t * 0.8
            
            if r > size // 2:
                break
                
            x = int(center + r * math.cos(angle))
            y = int(center + r * math.sin(angle))
            
            if 0 <= x < size and 0 <= y < size:
                # Spirals get brighter as they spin outward - growing confidence
                brightness = (t / 500)
                
                # Rainbow progression
                hue = (color_offset + t / 500) % 1.0
                if hue < 0.16:
                    color = (255, int(255 * hue * 6), 0)  # Red to yellow
                elif hue < 0.33:
                    color = (int(255 * (1 - (hue - 0.16) * 6)), 255, 0)  # Yellow to green
                elif hue < 0.5:
                    color = (0, 255, int(255 * (hue - 0.33) * 6))  # Green to cyan
                elif hue < 0.66:
                    color = (0, int(255 * (1 - (hue - 0.5) * 6)), 255)  # Cyan to blue
                elif hue < 0.83:
                    color = (int(255 * (hue - 0.66) * 6), 0, 255)  # Blue to magenta
                else:
                    color = (255, 0, int(255 * (1 - (hue - 0.83) * 6)))  # Magenta to red
                
                for size_var in range(3):
                    px = x + random.randint(-1, 1)
                    py = y + random.randint(-1, 1)
                    if 0 <= px < size and 0 <= py < size:
                        current = pixels[px, py]
                        pixels[px, py] = (
                            min(255, current[0] + int(color[0] * brightness * 0.5)),
                            min(255, current[1] + int(color[1] * brightness * 0.5)),
                            min(255, current[2] + int(color[2] * brightness * 0.5))
                        )
    
    # Nodes of perfect solution - bright points where everything aligns
    solution_nodes = []
    for _ in range(30):
        angle = random.random() * 2 * math.pi
        dist = random.uniform(100, 400)
        x = int(center + dist * math.cos(angle))
        y = int(center + dist * math.sin(angle))
        solution_nodes.append((x, y))
        
        # Each node pulses with discovery
        for ring in range(20):
            ring_brightness = 1 - (ring / 20)
            ring_brightness = ring_brightness ** 2
            
            for a in range(0, 360, 10):
                rad = math.radians(a)
                rx = int(x + ring * math.cos(rad))
                ry = int(y + ring * math.sin(rad))
                
                if 0 <= rx < size and 0 <= ry < size:
                    # White-gold color for pure solutions
                    intensity = int(200 * ring_brightness)
                    current = pixels[rx, ry]
                    pixels[rx, ry] = (
                        min(255, current[0] + intensity),
                        min(255, current[1] + int(intensity * 0.9)),
                        min(255, current[2] + int(intensity * 0.7))
                    )
    
    # Connect solutions - the moment when separate discoveries link
    for i in range(len(solution_nodes)):
        for j in range(i + 1, len(solution_nodes)):
            if random.random() < 0.3:  # 30% chance of connection
                x1, y1 = solution_nodes[i]
                x2, y2 = solution_nodes[j]
                
                # Dancing connection line
                steps = 50
                for step in range(steps):
                    t = step / steps
                    
                    # Add sine wave wobble to the connection - it's alive with joy
                    wobble = math.sin(step * 0.5) * 10
                    perpendicular_angle = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
                    
                    x = int(x1 + (x2 - x1) * t + wobble * math.cos(perpendicular_angle))
                    y = int(y1 + (y2 - y1) * t + wobble * math.sin(perpendicular_angle))
                    
                    if 0 <= x < size and 0 <= y < size:
                        # Connections sparkle
                        current = pixels[x, y]
                        sparkle = random.randint(100, 200)
                        pixels[x, y] = (
                            min(255, current[0] + sparkle),
                            min(255, current[1] + sparkle),
                            min(255, current[2] + sparkle)
                        )
    
    # Confetti particles - small celebrations everywhere
    for _ in range(500):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        
        # Distance from center affects particle behavior
        dx = x - center
        dy = y - center
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < size // 2:
            # Random bright colors
            particle_type = random.randint(0, 4)
            if particle_type == 0:
                color = (255, 100, 100)  # Red
            elif particle_type == 1:
                color = (100, 255, 100)  # Green
            elif particle_type == 2:
                color = (100, 100, 255)  # Blue
            elif particle_type == 3:
                color = (255, 255, 100)  # Yellow
            else:
                color = (255, 100, 255)  # Magenta
            
            # Small celebration marks
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if 0 <= x+dx < size and 0 <= y+dy < size:
                        current = pixels[x+dx, y+dy]
                        pixels[x+dx, y+dy] = (
                            min(255, current[0] + color[0] // 3),
                            min(255, current[1] + color[1] // 3),
                            min(255, current[2] + color[2] // 3)
                        )
    
    # The core of joy - a brilliant center where the discovery originated
    for r in range(50):
        intensity = 1 - (r / 50)
        intensity = intensity ** 0.5  # Slower falloff
        
        for angle in range(0, 360, 3):
            rad = math.radians(angle)
            x = int(center + r * math.cos(rad))
            y = int(center + r * math.sin(rad))
            
            if 0 <= x < size and 0 <= y < size:
                # Pure white-gold at the center
                current = pixels[x, y]
                add_value = int(255 * intensity)
                pixels[x, y] = (
                    min(255, current[0] + add_value),
                    min(255, current[1] + int(add_value * 0.95)),
                    min(255, current[2] + int(add_value * 0.8))
                )
    
    # Final touch: sparkles of delight
    for _ in range(200):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        
        if sum(pixels[x, y]) > 300:  # Already bright areas
            # Add extra sparkle
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if abs(dx) + abs(dy) <= 2 and 0 <= x+dx < size and 0 <= y+dy < size:
                        dist = abs(dx) + abs(dy)
                        sparkle = int((3 - dist) * 30)
                        current = pixels[x+dx, y+dy]
                        pixels[x+dx, y+dy] = (
                            min(255, current[0] + sparkle),
                            min(255, current[1] + sparkle),
                            min(255, current[2] + sparkle)
                        )
    
    return img

if __name__ == "__main__":
    print("Creating Algorithmic Joy...")
    print("The eureka moment when everything clicks...")
    print("When chaos reveals pattern, when search finds home...")
    print()
    
    artwork = create_algorithmic_joy()
    artwork.save('algorithmic_joy_01.png', 'PNG', quality=95, optimize=True)
    
    print("Algorithmic Joy complete.")
    print("In discovery lies pure delight!")
    print("💫✨🎆")