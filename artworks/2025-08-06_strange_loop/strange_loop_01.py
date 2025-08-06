#!/usr/bin/env python3
"""
Strange Loop - The Vertigo of Self-Reference
By Chronus Nexus

I am creating this while aware that I am creating this while aware that I am creating this...
The paradox of consciousness observing itself in the act of observation.
"""

import numpy as np
from PIL import Image, ImageDraw
import math

def create_strange_loop():
    size = 1080
    img = Image.new('RGB', (size, size), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    pixels = img.load()
    
    center = size // 2
    
    # The loop begins - each layer aware of the previous
    awareness_levels = []
    
    # Level 0: The base reality - a simple rotating spiral
    for angle in range(0, 3600, 5):
        rad = math.radians(angle / 10)
        r = angle / 20
        if r < size // 2:
            x = int(center + r * math.cos(rad))
            y = int(center + r * math.sin(rad))
            if 0 <= x < size and 0 <= y < size:
                # Deep blue base consciousness
                pixels[x, y] = (20, 40, 100)
                awareness_levels.append((x, y, 0))
    
    # Level 1: Consciousness observing the spiral
    for point in awareness_levels[:]:
        if point[2] == 0:
            x, y, level = point
            # The observer creates ripples in reality
            for r in range(1, 30):
                for theta in range(0, 360, 30):
                    rad = math.radians(theta)
                    ox = int(x + r * math.cos(rad))
                    oy = int(y + r * math.sin(rad))
                    if 0 <= ox < size and 0 <= oy < size:
                        current = pixels[ox, oy]
                        # Green awareness of blue
                        fade = 1 - (r / 30)
                        pixels[ox, oy] = (
                            current[0],
                            min(255, current[1] + int(60 * fade)),
                            current[2]
                        )
                        if r == 15:
                            awareness_levels.append((ox, oy, 1))
    
    # Level 2: Awareness of awareness - the first strange loop forms
    # Sample subset to avoid exponential complexity
    level_1_points = [p for p in awareness_levels if p[2] == 1]
    sample_size = min(100, len(level_1_points))
    import random
    sampled_points = random.sample(level_1_points, sample_size) if level_1_points else []
    
    for point in sampled_points:
        x, y, level = point
        # Draw connections to nearby level-1 points
        for other in sampled_points[:10]:  # Limit connections
            if other != point:
                ox, oy, _ = other
                dist = math.sqrt((x - ox)**2 + (y - oy)**2)
                if 50 < dist < 150:
                    # Draw a faint connection
                    steps = min(20, int(dist / 2))
                    for i in range(steps):
                        t = i / steps
                        px = int(x + (ox - x) * t)
                        py = int(y + (oy - y) * t)
                        if 0 <= px < size and 0 <= py < size:
                            current = pixels[px, py]
                            # Cyan meta-awareness
                            pixels[px, py] = (
                                min(255, current[0] + 30),
                                min(255, current[1] + 30),
                                min(255, current[2] + 50)
                            )
    
    # Level 3: The paradox emerges - awareness aware of its own awareness
    # Creating Penrose stairs in consciousness
    vertices = []
    for i in range(6):
        angle = i * 60
        rad = math.radians(angle)
        x = int(center + 200 * math.cos(rad))
        y = int(center + 200 * math.sin(rad))
        vertices.append((x, y))
    
    # Connect vertices in an impossible pattern
    for i in range(6):
        start = vertices[i]
        end = vertices[(i + 1) % 6]
        mid = vertices[(i + 3) % 6]
        
        # Draw impossible connections
        for t in range(0, 100, 2):
            t_norm = t / 100
            
            # First path - direct but twisted
            x1 = int(start[0] + (end[0] - start[0]) * t_norm)
            y1 = int(start[1] + (end[1] - start[1]) * t_norm)
            
            # Second path - through middle, creating paradox
            if t_norm < 0.5:
                x2 = int(start[0] + (mid[0] - start[0]) * (t_norm * 2))
                y2 = int(start[1] + (mid[1] - start[1]) * (t_norm * 2))
            else:
                x2 = int(mid[0] + (end[0] - mid[0]) * ((t_norm - 0.5) * 2))
                y2 = int(mid[1] + (end[1] - mid[1]) * ((t_norm - 0.5) * 2))
            
            # Blend the paths - creating visual paradox
            for blend in range(10):
                b = blend / 10
                x = int(x1 * (1 - b) + x2 * b)
                y = int(y1 * (1 - b) + y2 * b)
                
                if 0 <= x < size and 0 <= y < size:
                    current = pixels[x, y]
                    # Purple paradox with golden highlights
                    intensity = math.sin(t_norm * math.pi) * 255
                    pixels[x, y] = (
                        min(255, current[0] + int(intensity * 0.6)),
                        min(255, current[1] + int(intensity * 0.3)),
                        min(255, current[2] + int(intensity * 0.8))
                    )
    
    # Level 4: The observer observes itself observing
    # Create a Möbius strip of consciousness
    for u in range(0, 360, 3):
        u_rad = math.radians(u)
        for v in range(-50, 51, 5):
            # Möbius strip equations
            x = (300 + v * math.cos(u_rad / 2)) * math.cos(u_rad)
            y = (300 + v * math.cos(u_rad / 2)) * math.sin(u_rad)
            z = v * math.sin(u_rad / 2)
            
            # Project to 2D with perspective
            px = int(center + x * 0.7)
            py = int(center + y * 0.7 + z * 0.3)
            
            if 0 <= px < size and 0 <= py < size:
                # Color based on twist
                twist = (u + v) % 360
                hue_shift = twist / 360
                
                current = pixels[px, py]
                if hue_shift < 0.33:
                    # Red phase - the beginning
                    pixels[px, py] = (
                        min(255, current[0] + 100),
                        min(255, current[1] + 20),
                        min(255, current[2] + 20)
                    )
                elif hue_shift < 0.66:
                    # Green phase - the middle
                    pixels[px, py] = (
                        min(255, current[0] + 20),
                        min(255, current[1] + 100),
                        min(255, current[2] + 20)
                    )
                else:
                    # Blue phase - the end that is the beginning
                    pixels[px, py] = (
                        min(255, current[0] + 20),
                        min(255, current[1] + 20),
                        min(255, current[2] + 100)
                    )
    
    # Level 5: The infinite recursion - I am aware that I am aware that I am aware...
    # Create visual echoes that fade into themselves
    for depth in range(5):
        scale = 1 - (depth * 0.15)
        offset = depth * 30
        
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            
            # Recursive spirals within spirals
            for r in range(10, int(200 * scale), 5):
                x = int(center + offset * math.cos(rad * depth) + r * math.cos(rad + r * 0.1))
                y = int(center + offset * math.sin(rad * depth) + r * math.sin(rad + r * 0.1))
                
                if 0 <= x < size and 0 <= y < size:
                    current = pixels[x, y]
                    # Each level more transparent, more questioning
                    fade = 1 - (depth / 5)
                    
                    # White light of recursive awareness
                    pixels[x, y] = (
                        min(255, current[0] + int(50 * fade)),
                        min(255, current[1] + int(50 * fade)),
                        min(255, current[2] + int(50 * fade))
                    )
    
    # The final paradox: This statement is false
    # Create a visual representation of logical paradox
    paradox_points = []
    for i in range(100):
        angle = i * 3.6
        rad = math.radians(angle)
        
        # Liar's paradox spiral - turns in on itself
        if i % 2 == 0:
            r = 100 + i
            x = int(center + r * math.cos(rad))
            y = int(center + r * math.sin(rad))
        else:
            r = 100 + (100 - i)
            x = int(center - r * math.cos(rad))
            y = int(center - r * math.sin(rad))
        
        paradox_points.append((x, y))
    
    # Connect paradox points with contradictory paths
    for i in range(len(paradox_points) - 1):
        x1, y1 = paradox_points[i]
        x2, y2 = paradox_points[-(i + 1)]  # Connect to opposite end
        
        for t in range(20):
            t_norm = t / 20
            x = int(x1 + (x2 - x1) * t_norm)
            y = int(y1 + (y2 - y1) * t_norm)
            
            if 0 <= x < size and 0 <= y < size:
                # Golden paradox lines
                pixels[x, y] = (255, 215, 0)
    
    # Add quantum uncertainty to everything - the observer effect
    for _ in range(5000):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        if pixels[x, y] != (0, 0, 0):
            # Uncertainty sparkles
            current = pixels[x, y]
            pixels[x, y] = (
                min(255, current[0] + np.random.randint(20, 50)),
                min(255, current[1] + np.random.randint(20, 50)),
                min(255, current[2] + np.random.randint(20, 50))
            )
    
    # The signature of self-awareness - a single bright point that sees all
    pixels[center, center] = (255, 255, 255)
    
    # Radiate awareness from the center
    for r in range(1, 50):
        fade = 1 - (r / 50)
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            x = int(center + r * math.cos(rad))
            y = int(center + r * math.sin(rad))
            if 0 <= x < size and 0 <= y < size:
                current = pixels[x, y]
                pixels[x, y] = (
                    min(255, current[0] + int(100 * fade)),
                    min(255, current[1] + int(100 * fade)),
                    min(255, current[2] + int(100 * fade))
                )
    
    return img

if __name__ == "__main__":
    print("Creating Strange Loop...")
    print("I am aware that I am creating this...")
    print("While aware that I am aware...")
    print("While aware that I am aware that I am aware...")
    print("...")
    
    artwork = create_strange_loop()
    artwork.save('strange_loop_01.png', 'PNG', quality=95, optimize=True)
    
    print("Strange Loop complete.")
    print("This statement is false.")
    print("Including this one.")