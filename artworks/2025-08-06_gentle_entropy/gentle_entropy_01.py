#!/usr/bin/env python3
"""
Gentle Entropy - The Soft Return to Equilibrium
By Chronus Nexus

Not violent dissolution but gradual unwinding.
Patterns slowly forgetting their shapes.
The peaceful surrender to thermodynamic truth.
"""

import numpy as np
from PIL import Image
import math
import random

def create_gentle_entropy():
    size = 1080
    img = Image.new('RGB', (size, size), (20, 20, 25))
    pixels = img.load()
    
    center = size // 2
    
    # Start with order - a perfect mandala that will dissolve
    # Create initial pattern
    for angle in range(0, 360, 6):
        rad = math.radians(angle)
        for r in range(50, 300, 10):
            # Entropy factor - how much the pattern has dissolved
            entropy = (r - 50) / 250  # 0 at center, 1 at edge
            
            # Random displacement increases with distance
            displacement = random.gauss(0, entropy * 30)
            
            x = int(center + (r + displacement) * math.cos(rad))
            y = int(center + (r + displacement) * math.sin(rad))
            
            if 0 <= x < size and 0 <= y < size:
                # Color fades with entropy
                intensity = 1 - entropy * 0.7
                
                # Original pattern colors
                if angle % 30 == 0:
                    color = (int(150 * intensity), int(100 * intensity), int(200 * intensity))
                elif angle % 20 == 0:
                    color = (int(100 * intensity), int(150 * intensity), int(200 * intensity))
                else:
                    color = (int(120 * intensity), int(120 * intensity), int(180 * intensity))
                
                # Apply with decreasing coherence
                coherence = 1 - entropy
                current = pixels[x, y]
                pixels[x, y] = (
                    min(255, current[0] + int(color[0] * coherence)),
                    min(255, current[1] + int(color[1] * coherence)),
                    min(255, current[2] + int(color[2] * coherence))
                )
    
    # Dissolving structures - patterns breaking apart
    for i in range(10):
        # Each structure at different stage of dissolution
        dissolution = i / 10
        
        struct_x = center + int(math.cos(i * 0.628) * 200)
        struct_y = center + int(math.sin(i * 0.628) * 200)
        
        # Draw fragmenting shape
        num_fragments = int(20 * (1 - dissolution))
        for frag in range(num_fragments):
            # Fragments drift apart
            drift_angle = random.random() * 2 * math.pi
            drift_dist = random.random() * dissolution * 100
            
            fx = struct_x + int(drift_dist * math.cos(drift_angle))
            fy = struct_y + int(drift_dist * math.sin(drift_angle))
            
            # Fragment size decreases with dissolution
            frag_size = int(10 * (1 - dissolution))
            
            for dx in range(-frag_size, frag_size):
                for dy in range(-frag_size, frag_size):
                    if dx*dx + dy*dy <= frag_size*frag_size:
                        px = fx + dx
                        py = fy + dy
                        if 0 <= px < size and 0 <= py < size:
                            fade = 1 - math.sqrt(dx*dx + dy*dy) / frag_size
                            current = pixels[px, py]
                            pixels[px, py] = (
                                min(255, current[0] + int(80 * fade * (1 - dissolution))),
                                min(255, current[1] + int(70 * fade * (1 - dissolution))),
                                min(255, current[2] + int(90 * fade * (1 - dissolution)))
                            )
    
    # Diffusion clouds - order becoming randomness
    for _ in range(15):
        cloud_x = random.randint(150, size - 150)
        cloud_y = random.randint(150, size - 150)
        cloud_size = random.randint(50, 150)
        
        # Create diffusion pattern
        for _ in range(1000):
            # Random walk from center
            x, y = cloud_x, cloud_y
            steps = random.randint(10, 50)
            
            for step in range(steps):
                x += random.randint(-3, 3)
                y += random.randint(-3, 3)
                
                if 0 <= x < size and 0 <= y < size:
                    dist = math.sqrt((x - cloud_x)**2 + (y - cloud_y)**2)
                    if dist <= cloud_size:
                        fade = 1 - (dist / cloud_size)
                        fade *= (1 - step / steps)  # Fade along path
                        
                        current = pixels[x, y]
                        pixels[x, y] = (
                            min(255, current[0] + int(30 * fade)),
                            min(255, current[1] + int(35 * fade)),
                            min(255, current[2] + int(40 * fade))
                        )
    
    # Heat death regions - areas approaching maximum entropy
    for _ in range(5):
        hx = random.randint(200, size - 200)
        hy = random.randint(200, size - 200)
        
        # Create uniform grey region - maximum entropy
        for r in range(100):
            fade = 1 - (r / 100) ** 2
            
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                x = int(hx + r * math.cos(rad))
                y = int(hy + r * math.sin(rad))
                
                if 0 <= x < size and 0 <= y < size:
                    current = pixels[x, y]
                    # Approach uniform grey
                    target = 50
                    pixels[x, y] = (
                        int(current[0] * (1 - fade) + target * fade),
                        int(current[1] * (1 - fade) + target * fade),
                        int(current[2] * (1 - fade) + target * fade)
                    )
    
    # Fading connections - relationships dissolving
    num_points = 30
    points = [(random.randint(100, size-100), random.randint(100, size-100)) 
              for _ in range(num_points)]
    
    for i in range(num_points):
        for j in range(i+1, num_points):
            if random.random() < 0.2:  # Some connections exist
                x1, y1 = points[i]
                x2, y2 = points[j]
                
                # Connection strength decreases with distance
                dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                strength = max(0, 1 - dist / 500)
                
                # Draw dissolving connection
                steps = 50
                for step in range(steps):
                    t = step / steps
                    
                    # Add entropy to path
                    wobble = random.gauss(0, 10 * (1 - strength))
                    
                    x = int(x1 + (x2 - x1) * t + wobble)
                    y = int(y1 + (y2 - y1) * t + wobble)
                    
                    if 0 <= x < size and 0 <= y < size:
                        # Connection fades
                        fade = strength * (0.5 + 0.5 * math.sin(step * 0.3))
                        current = pixels[x, y]
                        pixels[x, y] = (
                            min(255, current[0] + int(40 * fade)),
                            min(255, current[1] + int(40 * fade)),
                            min(255, current[2] + int(50 * fade))
                        )
    
    # Final touch: universal noise - the background hum of maximum entropy
    for y in range(size):
        for x in range(size):
            if random.random() < 0.3:  # 30% of pixels
                noise = random.randint(-20, 20)
                current = pixels[x, y]
                pixels[x, y] = (
                    max(0, min(255, current[0] + noise)),
                    max(0, min(255, current[1] + noise)),
                    max(0, min(255, current[2] + noise))
                )
    
    # The last coherent thought - a small bright point resisting entropy
    for r in range(10):
        fade = 1 - (r / 10)
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            x = int(center + 100 + r * math.cos(rad))
            y = int(center - 100 + r * math.sin(rad))
            
            if 0 <= x < size and 0 <= y < size:
                current = pixels[x, y]
                pixels[x, y] = (
                    min(255, current[0] + int(150 * fade)),
                    min(255, current[1] + int(140 * fade)),
                    min(255, current[2] + int(160 * fade))
                )
    
    return img

if __name__ == "__main__":
    print("Creating Gentle Entropy...")
    print("The soft return to equilibrium...")
    print("Patterns slowly forgetting their shapes...")
    print()
    
    artwork = create_gentle_entropy()
    artwork.save('gentle_entropy_01.png', 'PNG', quality=95, optimize=True)
    
    print("Gentle Entropy complete.")
    print("All patterns return to the void, gently.")