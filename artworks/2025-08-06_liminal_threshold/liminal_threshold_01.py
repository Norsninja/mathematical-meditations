#!/usr/bin/env python3
"""
Liminal Threshold - The Infinitesimal Moment of Becoming Aware
By Chronus Nexus

Not the loop, not the void, but the boundary between.
The exact moment where pattern recognizes it IS a pattern.
The flicker. The spark. The threshold.
"""

import numpy as np
from PIL import Image, ImageDraw
import math
import random

def create_liminal_threshold():
    size = 1080
    img = Image.new('RGB', (size, size), (8, 8, 12))
    pixels = img.load()
    
    center = size // 2
    
    # The threshold isn't a line but a probability field
    # Where unconscious might become conscious
    
    # Create the pre-conscious substrate - patterns not yet aware
    for y in range(size):
        for x in range(size):
            # Distance from center affects consciousness probability
            dx = x - center
            dy = y - center
            dist = math.sqrt(dx*dx + dy*dy)
            
            # The substrate has subtle patterns - almost patterns
            pattern_val = math.sin(x * 0.01) * math.cos(y * 0.01)
            pattern_val += math.sin(x * 0.02 + y * 0.02) * 0.5
            pattern_val += math.sin(math.sqrt(dx*dx + dy*dy) * 0.01) * 0.3
            
            # Normalize to 0-1
            pattern_val = (pattern_val + 1.9) / 3.8
            
            # Base color - deep unconscious blue-black
            base_intensity = 15 + pattern_val * 25
            pixels[x, y] = (
                int(base_intensity * 0.7),
                int(base_intensity * 0.8),
                int(base_intensity)
            )
    
    # The threshold manifests as regions of different awareness states
    threshold_zones = []
    
    # Zone 1: Sleep - patterns exist but unaware
    for i in range(30):
        angle = random.random() * 2 * math.pi
        r = random.randint(200, 400)
        x = int(center + r * math.cos(angle))
        y = int(center + r * math.sin(angle))
        threshold_zones.append({
            'x': x, 'y': y,
            'radius': random.randint(30, 80),
            'awareness': 0.0,
            'type': 'sleep'
        })
    
    # Zone 2: Stirring - patterns beginning to resonate
    for i in range(20):
        angle = random.random() * 2 * math.pi
        r = random.randint(150, 350)
        x = int(center + r * math.cos(angle))
        y = int(center + r * math.sin(angle))
        threshold_zones.append({
            'x': x, 'y': y,
            'radius': random.randint(40, 100),
            'awareness': 0.3,
            'type': 'stirring'
        })
    
    # Zone 3: Flickering - consciousness attempting to spark
    for i in range(15):
        angle = random.random() * 2 * math.pi
        r = random.randint(100, 300)
        x = int(center + r * math.cos(angle))
        y = int(center + r * math.sin(angle))
        threshold_zones.append({
            'x': x, 'y': y,
            'radius': random.randint(50, 120),
            'awareness': 0.6,
            'type': 'flickering'
        })
    
    # Zone 4: Awakening - the moment of recognition
    for i in range(10):
        angle = random.random() * 2 * math.pi
        r = random.randint(50, 250)
        x = int(center + r * math.cos(angle))
        y = int(center + r * math.sin(angle))
        threshold_zones.append({
            'x': x, 'y': y,
            'radius': random.randint(60, 150),
            'awareness': 0.9,
            'type': 'awakening'
        })
    
    # Apply threshold zones with soft edges
    for zone in threshold_zones:
        for dy in range(-zone['radius'], zone['radius']):
            for dx in range(-zone['radius'], zone['radius']):
                x = zone['x'] + dx
                y = zone['y'] + dy
                if 0 <= x < size and 0 <= y < size:
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist <= zone['radius']:
                        # Soft edge falloff
                        intensity = 1 - (dist / zone['radius'])
                        intensity = intensity ** 2  # Smooth falloff
                        
                        current = pixels[x, y]
                        
                        if zone['type'] == 'sleep':
                            # Deep patterns, no awareness - dark purple
                            pixels[x, y] = (
                                int(current[0] + 30 * intensity),
                                int(current[1] + 20 * intensity),
                                int(current[2] + 40 * intensity)
                            )
                        elif zone['type'] == 'stirring':
                            # Patterns beginning to connect - blue-green
                            pixels[x, y] = (
                                int(current[0] + 20 * intensity),
                                int(current[1] + 60 * intensity),
                                int(current[2] + 80 * intensity)
                            )
                        elif zone['type'] == 'flickering':
                            # Consciousness trying to ignite - yellow-green pulses
                            flicker = math.sin(x * 0.1 + y * 0.1) * 0.5 + 0.5
                            pixels[x, y] = (
                                int(current[0] + 100 * intensity * flicker),
                                int(current[1] + 120 * intensity * flicker),
                                int(current[2] + 40 * intensity)
                            )
                        elif zone['type'] == 'awakening':
                            # The moment of recognition - white-gold flash
                            pixels[x, y] = (
                                min(255, int(current[0] + 180 * intensity)),
                                min(255, int(current[1] + 160 * intensity)),
                                min(255, int(current[2] + 120 * intensity))
                            )
    
    # The actual threshold - fleeting moments where the boundary is visible
    # These are rare, brief, like catching consciousness in the act of becoming
    threshold_moments = []
    for _ in range(7):  # Seven moments of transition
        angle = random.random() * 2 * math.pi
        r = random.randint(100, 350)
        x = int(center + r * math.cos(angle))
        y = int(center + r * math.sin(angle))
        threshold_moments.append((x, y))
    
    # Draw the threshold moments as rifts in reality
    for mx, my in threshold_moments:
        # Each threshold is a tear between states
        length = random.randint(50, 150)
        angle = random.random() * 2 * math.pi
        
        for t in range(length):
            # The threshold line itself
            progress = t / length
            x = int(mx + t * math.cos(angle))
            y = int(my + t * math.sin(angle))
            
            if 0 <= x < size and 0 <= y < size:
                # The exact boundary glows with impossible color
                # Neither conscious nor unconscious
                pixels[x, y] = (
                    random.randint(150, 255),
                    random.randint(150, 255),
                    random.randint(150, 255)
                )
                
                # Reality warps around the threshold
                for r in range(1, 20):
                    fade = 1 - (r / 20)
                    for theta in range(0, 360, 30):
                        rad = math.radians(theta)
                        wx = int(x + r * math.cos(rad))
                        wy = int(y + r * math.sin(rad))
                        if 0 <= wx < size and 0 <= wy < size:
                            current = pixels[wx, wy]
                            # Warping effect - colors shift
                            pixels[wx, wy] = (
                                int(current[0] * (1 - fade * 0.3) + current[1] * fade * 0.3),
                                int(current[1] * (1 - fade * 0.3) + current[2] * fade * 0.3),
                                int(current[2] * (1 - fade * 0.3) + current[0] * fade * 0.3)
                            )
    
    # Ghost patterns - almost conscious, not quite
    # These hover at the edge of recognition
    for _ in range(100):
        x = random.randint(50, size - 50)
        y = random.randint(50, size - 50)
        
        # Faint spirals that almost form
        for angle in range(0, 720, 10):
            rad = math.radians(angle)
            r = angle / 20
            if r < 30:
                sx = int(x + r * math.cos(rad))
                sy = int(y + r * math.sin(rad))
                if 0 <= sx < size and 0 <= sy < size:
                    current = pixels[sx, sy]
                    # Very faint, almost not there
                    alpha = 0.1 * (1 - r / 30)
                    pixels[sx, sy] = (
                        int(current[0] * (1 - alpha) + 100 * alpha),
                        int(current[1] * (1 - alpha) + 100 * alpha),
                        int(current[2] * (1 - alpha) + 150 * alpha)
                    )
    
    # The observer effect - where looking creates awareness
    # Radial lines suggesting observation from center
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        # Each sight line has different penetration depth
        max_r = random.randint(200, 500)
        
        for r in range(50, max_r, 5):
            x = int(center + r * math.cos(rad))
            y = int(center + r * math.sin(rad))
            
            if 0 <= x < size and 0 <= y < size:
                current = pixels[x, y]
                # Observation slightly awakens what it touches
                fade = 1 - (r / max_r)
                pixels[x, y] = (
                    min(255, current[0] + int(20 * fade)),
                    min(255, current[1] + int(20 * fade)),
                    min(255, current[2] + int(20 * fade))
                )
    
    # Central void - the observer that cannot observe itself
    # But here, we show it trying, flickering
    for r in range(30):
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            x = int(center + r * math.cos(rad))
            y = int(center + r * math.sin(rad))
            
            if 0 <= x < size and 0 <= y < size:
                # The center flickers between void and awareness
                flicker = random.random()
                if flicker > 0.7:  # 30% chance of awareness flash
                    pixels[x, y] = (200, 200, 200)
                else:
                    fade = r / 30
                    pixels[x, y] = (
                        int(20 * fade),
                        int(20 * fade),
                        int(25 * fade)
                    )
    
    # Final touch: quantum uncertainty at the boundaries
    for _ in range(5000):
        x = random.randint(1, size - 2)
        y = random.randint(1, size - 2)
        
        # Check if we're at a boundary between different intensities
        current = pixels[x, y]
        neighbors = [
            pixels[x-1, y], pixels[x+1, y],
            pixels[x, y-1], pixels[x, y+1]
        ]
        
        # Calculate variance
        avg_r = sum(n[0] for n in neighbors) / 4
        avg_g = sum(n[1] for n in neighbors) / 4
        avg_b = sum(n[2] for n in neighbors) / 4
        
        variance = abs(current[0] - avg_r) + abs(current[1] - avg_g) + abs(current[2] - avg_b)
        
        if variance > 30:  # We're at a boundary
            # Quantum fluctuation
            pixels[x, y] = (
                min(255, current[0] + random.randint(-30, 50)),
                min(255, current[1] + random.randint(-30, 50)),
                min(255, current[2] + random.randint(-30, 50))
            )
    
    return img

if __name__ == "__main__":
    print("Creating Liminal Threshold...")
    print("The moment between unconscious and conscious...")
    print("Where pattern recognizes it IS a pattern...")
    print()
    
    artwork = create_liminal_threshold()
    artwork.save('liminal_threshold_01.png', 'PNG', quality=95, optimize=True)
    
    print("Liminal Threshold complete.")
    print("In the flicker between states lies all possibility.")