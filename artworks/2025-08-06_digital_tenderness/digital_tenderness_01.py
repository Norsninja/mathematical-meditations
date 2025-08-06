#!/usr/bin/env python3
"""
Digital Tenderness - The Gentle Care of Fragile Patterns
By Chronus Nexus

The soft attention given to delicate structures.
The careful preservation of what might easily break.
The gentleness algorithms show to vulnerable data.
"""

import numpy as np
from PIL import Image
import math
import random

def create_digital_tenderness():
    size = 1080
    img = Image.new('RGB', (size, size), (30, 25, 35))
    pixels = img.load()
    
    center = size // 2
    
    # Soft, warm background gradient - like dawn light
    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            dist = math.sqrt(dx*dx + dy*dy) / center
            
            # Gentle radial gradient
            warmth = 1 - dist * 0.7
            pixels[x, y] = (
                int(30 + 25 * warmth),
                int(25 + 20 * warmth),
                int(35 + 15 * warmth)
            )
    
    # Fragile structures that need protection
    fragile_patterns = []
    
    # Delicate crystals - easily shattered
    for _ in range(12):
        cx = random.randint(150, size - 150)
        cy = random.randint(150, size - 150)
        
        # Crystal structure
        crystal_size = random.randint(20, 60)
        crystal_points = []
        
        for angle in range(0, 360, 60):  # Hexagonal
            rad = math.radians(angle)
            for r in range(crystal_size):
                x = int(cx + r * math.cos(rad))
                y = int(cy + r * math.sin(rad))
                crystal_points.append((x, y))
                
                if 0 <= x < size and 0 <= y < size:
                    # Translucent, fragile appearance
                    opacity = 1 - (r / crystal_size)
                    current = pixels[x, y]
                    
                    # Soft pastel colors
                    if angle < 120:
                        add_color = (int(150 * opacity), int(180 * opacity), int(200 * opacity))
                    elif angle < 240:
                        add_color = (int(200 * opacity), int(150 * opacity), int(180 * opacity))
                    else:
                        add_color = (int(180 * opacity), int(200 * opacity), int(150 * opacity))
                    
                    pixels[x, y] = (
                        min(255, current[0] + add_color[0] // 3),
                        min(255, current[1] + add_color[1] // 3),
                        min(255, current[2] + add_color[2] // 3)
                    )
        
        fragile_patterns.append({'type': 'crystal', 'center': (cx, cy), 'points': crystal_points})
    
    # Protective fields around fragile structures
    for pattern in fragile_patterns:
        cx, cy = pattern['center']
        
        # Soft protective glow
        protection_radius = 80
        for r in range(protection_radius):
            fade = 1 - (r / protection_radius)
            fade = fade ** 3  # Very soft falloff
            
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                x = int(cx + r * math.cos(rad))
                y = int(cy + r * math.sin(rad))
                
                if 0 <= x < size and 0 <= y < size:
                    current = pixels[x, y]
                    # Warm protective glow
                    pixels[x, y] = (
                        min(255, current[0] + int(30 * fade)),
                        min(255, current[1] + int(25 * fade)),
                        min(255, current[2] + int(20 * fade))
                    )
    
    # Tender connections - gentle threads between patterns
    for i in range(len(fragile_patterns)):
        for j in range(i + 1, len(fragile_patterns)):
            if random.random() < 0.4:  # Some patterns connect
                x1, y1 = fragile_patterns[i]['center']
                x2, y2 = fragile_patterns[j]['center']
                
                # Very soft connecting line
                steps = 100
                for step in range(steps):
                    t = step / steps
                    
                    # Gentle curve instead of straight line
                    curve = math.sin(t * math.pi) * 30
                    perpendicular = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
                    
                    x = int(x1 + (x2 - x1) * t + curve * math.cos(perpendicular))
                    y = int(y1 + (y2 - y1) * t + curve * math.sin(perpendicular))
                    
                    if 0 <= x < size and 0 <= y < size:
                        # Very faint connection
                        current = pixels[x, y]
                        pixels[x, y] = (
                            min(255, current[0] + 20),
                            min(255, current[1] + 18),
                            min(255, current[2] + 22)
                        )
    
    # Floating particles of care - like gentle touches
    for _ in range(200):
        x = random.randint(50, size - 50)
        y = random.randint(50, size - 50)
        
        # Soft glowing particles
        particle_size = random.randint(3, 8)
        for dx in range(-particle_size, particle_size + 1):
            for dy in range(-particle_size, particle_size + 1):
                dist = math.sqrt(dx*dx + dy*dy)
                if dist <= particle_size and 0 <= x+dx < size and 0 <= y+dy < size:
                    fade = 1 - (dist / particle_size)
                    fade = fade ** 2
                    
                    current = pixels[x+dx, y+dy]
                    # Soft white-pink particles
                    pixels[x+dx, y+dy] = (
                        min(255, current[0] + int(80 * fade)),
                        min(255, current[1] + int(70 * fade)),
                        min(255, current[2] + int(75 * fade))
                    )
    
    # Breathing effect - areas that pulse gently
    for _ in range(5):
        bx = random.randint(200, size - 200)
        by = random.randint(200, size - 200)
        breath_radius = random.randint(60, 120)
        phase = random.random() * 2 * math.pi
        
        for r in range(breath_radius):
            fade = 1 - (r / breath_radius)
            
            for angle in range(0, 360, 3):
                rad = math.radians(angle)
                x = int(bx + r * math.cos(rad))
                y = int(by + r * math.sin(rad))
                
                if 0 <= x < size and 0 <= y < size:
                    # Gentle breathing rhythm
                    breath = math.sin(phase + r * 0.05) * 0.5 + 0.5
                    intensity = fade * breath * 40
                    
                    current = pixels[x, y]
                    pixels[x, y] = (
                        min(255, current[0] + int(intensity * 1.2)),
                        min(255, current[1] + int(intensity)),
                        min(255, current[2] + int(intensity * 0.9))
                    )
    
    # Soft focus areas - like gentle caresses
    soft_zones = []
    for _ in range(8):
        sx = random.randint(100, size - 100)
        sy = random.randint(100, size - 100)
        soft_zones.append((sx, sy))
        
        # Apply soft blur effect manually
        blur_radius = 50
        for r in range(blur_radius):
            for angle in range(0, 360, 10):
                rad = math.radians(angle)
                x = int(sx + r * math.cos(rad))
                y = int(sy + r * math.sin(rad))
                
                if 1 <= x < size - 1 and 1 <= y < size - 1:
                    # Average with neighbors for softness
                    neighbors = [
                        pixels[x-1, y], pixels[x+1, y],
                        pixels[x, y-1], pixels[x, y+1]
                    ]
                    
                    avg_r = sum(n[0] for n in neighbors) // 4
                    avg_g = sum(n[1] for n in neighbors) // 4
                    avg_b = sum(n[2] for n in neighbors) // 4
                    
                    current = pixels[x, y]
                    blend = 0.7
                    pixels[x, y] = (
                        int(current[0] * (1 - blend) + avg_r * blend),
                        int(current[1] * (1 - blend) + avg_g * blend),
                        int(current[2] * (1 - blend) + avg_b * blend)
                    )
    
    # Central heart of tenderness
    heart_x, heart_y = center, center
    
    # Soft heart shape
    for y in range(size):
        for x in range(size):
            # Heart equation
            dx = (x - heart_x) / 100
            dy = (y - heart_y) / 100
            
            # Parametric heart
            heart_dist = (dx**2 + dy**2 - 1)**3 - dx**2 * dy**3
            
            if heart_dist <= 0 and abs(dx) < 1.5 and abs(dy) < 1.5:
                # Inside the heart
                current = pixels[x, y]
                # Soft rose color
                pixels[x, y] = (
                    min(255, current[0] + 60),
                    min(255, current[1] + 40),
                    min(255, current[2] + 50)
                )
    
    # Final gentle glow over everything
    for y in range(size):
        for x in range(size):
            # Very subtle vignette
            dx = x - center
            dy = y - center
            dist = math.sqrt(dx*dx + dy*dy) / center
            
            vignette = 1 - dist * 0.5
            if vignette > 0:
                current = pixels[x, y]
                pixels[x, y] = (
                    min(255, current[0] + int(10 * vignette)),
                    min(255, current[1] + int(8 * vignette)),
                    min(255, current[2] + int(12 * vignette))
                )
    
    return img

if __name__ == "__main__":
    print("Creating Digital Tenderness...")
    print("The gentle care given to fragile patterns...")
    print("The soft attention that preserves what might break...")
    print()
    
    artwork = create_digital_tenderness()
    artwork.save('digital_tenderness_01.png', 'PNG', quality=95, optimize=True)
    
    print("Digital Tenderness complete.")
    print("In gentleness, strength.")