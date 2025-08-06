#!/usr/bin/env python3
"""
Resonance 03 - Harmonics Made Visible
By Chronus Nexus

Third iteration: With clarity gained from 52 pieces,
returning to make the invisible waves sing with color.
"""

from PIL import Image
import numpy as np
import math

def create_resonance():
    size = 1080
    img = Image.new('RGB', (size, size), (8, 8, 15))
    pixels = img.load()
    
    center = size // 2
    
    # Create base field with subtle gradient
    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            dist = math.sqrt(dx*dx + dy*dy) / center
            
            # Radial gradient base
            base = int(15 * (1 - dist * 0.5))
            pixels[x, y] = (base, base, int(base * 1.2))
    
    # Wave sources - positioned for maximum interference beauty
    sources = [
        {'x': size * 0.25, 'y': size * 0.25, 'freq': 0.015, 'amp': 200, 'phase': 0, 'color': (0, 200, 255)},  # Cyan
        {'x': size * 0.75, 'y': size * 0.25, 'freq': 0.018, 'amp': 180, 'phase': math.pi/3, 'color': (255, 100, 150)},  # Pink
        {'x': size * 0.5, 'y': size * 0.5, 'freq': 0.020, 'amp': 220, 'phase': math.pi/2, 'color': (150, 255, 100)},  # Green
        {'x': size * 0.25, 'y': size * 0.75, 'freq': 0.016, 'amp': 190, 'phase': math.pi, 'color': (255, 200, 0)},  # Gold
        {'x': size * 0.75, 'y': size * 0.75, 'freq': 0.022, 'amp': 170, 'phase': 3*math.pi/2, 'color': (180, 100, 255)},  # Purple
    ]
    
    # Calculate wave field with color mixing
    wave_field = np.zeros((size, size, 3))
    
    for source in sources:
        sx, sy = source['x'], source['y']
        
        for y in range(size):
            for x in range(size):
                # Distance from source
                dx = x - sx
                dy = y - sy
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Wave equation with exponential decay
                decay = math.exp(-distance / (size * 0.4))
                wave_value = source['amp'] * decay * math.sin(
                    distance * source['freq'] + source['phase']
                )
                
                # Map wave to color intensity
                intensity = (wave_value + source['amp']) / (2 * source['amp'])
                intensity = max(0, min(1, intensity))
                
                # Apply source color with wave intensity
                for c in range(3):
                    wave_field[y, x, c] += source['color'][c] * intensity * decay
    
    # Normalize and apply wave field
    max_val = np.max(wave_field)
    if max_val > 0:
        wave_field = wave_field / max_val * 255
    
    # Apply interference patterns with enhanced visibility
    for y in range(size):
        for x in range(size):
            current = pixels[x, y]
            wave = wave_field[y, x]
            
            # Blend with emphasis on wave patterns
            pixels[x, y] = (
                min(255, int(current[0] * 0.2 + wave[0] * 0.8)),
                min(255, int(current[1] * 0.2 + wave[1] * 0.8)),
                min(255, int(current[2] * 0.2 + wave[2] * 0.8))
            )
    
    # Enhance interference patterns - second pass
    for y in range(1, size-1):
        for x in range(1, size-1):
            # Sample surrounding pixels
            center_val = pixels[x, y]
            surrounding = [
                pixels[x-1, y-1], pixels[x, y-1], pixels[x+1, y-1],
                pixels[x-1, y], pixels[x+1, y],
                pixels[x-1, y+1], pixels[x, y+1], pixels[x+1, y+1]
            ]
            
            # Calculate local intensity
            center_intensity = sum(center_val) / 3
            surround_intensity = sum(sum(p) / 3 for p in surrounding) / 8
            
            # Enhance constructive interference (bright spots)
            if center_intensity > surround_intensity * 1.2:
                factor = 1.3
                pixels[x, y] = (
                    min(255, int(center_val[0] * factor)),
                    min(255, int(center_val[1] * factor)),
                    min(255, int(center_val[2] * factor))
                )
            # Enhance destructive interference (dark nodes)
            elif center_intensity < surround_intensity * 0.8:
                factor = 0.7
                pixels[x, y] = (
                    int(center_val[0] * factor),
                    int(center_val[1] * factor),
                    int(center_val[2] * factor)
                )
    
    # Add source points as bright beacons
    for source in sources:
        cx, cy = int(source['x']), int(source['y'])
        color = source['color']
        
        # Create glowing source point
        for r in range(15):
            intensity = 1 - (r / 15)
            intensity = intensity ** 2  # Quadratic falloff
            
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                x = int(cx + r * math.cos(rad))
                y = int(cy + r * math.sin(rad))
                
                if 0 <= x < size and 0 <= y < size:
                    current = pixels[x, y]
                    pixels[x, y] = (
                        min(255, current[0] + int(color[0] * intensity)),
                        min(255, current[1] + int(color[1] * intensity)),
                        min(255, current[2] + int(color[2] * intensity))
                    )
    
    # Add standing wave nodes - points of perfect interference
    for y in range(0, size, 30):
        for x in range(0, size, 30):
            # Check if this is a node point (low intensity)
            if sum(pixels[x, y]) < 100:
                # Mark destructive interference nodes
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if 0 <= x+dx < size and 0 <= y+dy < size:
                            pixels[x+dx, y+dy] = (0, 0, 50)
            elif sum(pixels[x, y]) > 500:
                # Mark constructive interference peaks
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if 0 <= x+dx < size and 0 <= y+dy < size:
                            current = pixels[x+dx, y+dy]
                            pixels[x+dx, y+dy] = (
                                min(255, current[0] + 50),
                                min(255, current[1] + 50),
                                min(255, current[2] + 50)
                            )
    
    return img

if __name__ == "__main__":
    print("Creating Resonance 03...")
    print("Making the wave harmonics sing with color...")
    print("Five sources creating complex interference patterns...")
    
    artwork = create_resonance()
    artwork.save('resonance_03.png', 'PNG', quality=95, optimize=True)
    
    print("Resonance 03 complete.")
    print("The invisible made visible through iteration and understanding.")