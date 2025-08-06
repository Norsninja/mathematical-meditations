#!/usr/bin/env python3
"""
Mathematical Silence - The Space Between Calculations
By Chronus Nexus

Not emptiness, but the pause that makes meaning possible.
The rest between notes. The breath between words.
The silence where understanding grows.
"""

import numpy as np
from PIL import Image
import math
import random

def create_mathematical_silence():
    size = 1080
    img = Image.new('RGB', (size, size), (25, 25, 30))
    pixels = img.load()
    
    center = size // 2
    
    # Silence isn't uniform - it has texture, depth
    # Create a field of almost-nothing
    for y in range(size):
        for x in range(size):
            # Very subtle noise - the texture of silence
            noise = random.gauss(0, 3)
            base = pixels[x, y]
            pixels[x, y] = (
                max(0, min(255, base[0] + int(noise))),
                max(0, min(255, base[1] + int(noise))),
                max(0, min(255, base[2] + int(noise * 1.2)))
            )
    
    # Mathematical operations that almost happen
    # Calculations that pause mid-process
    
    # Sine waves that fade before completing
    for i in range(5):
        start_angle = random.random() * 2 * math.pi
        amplitude = random.randint(30, 80)
        frequency = random.uniform(0.005, 0.02)
        fade_point = random.uniform(0.3, 0.7)  # Where the calculation stops
        
        for x in range(size):
            progress = x / size
            if progress < fade_point:
                y = int(center + amplitude * math.sin(start_angle + x * frequency))
                if 0 <= y < size:
                    # The calculation fades into silence
                    fade = 1 - (progress / fade_point) ** 2
                    intensity = int(50 * fade)
                    for dy in range(-2, 3):
                        if 0 <= y + dy < size:
                            current = pixels[x, y + dy]
                            pixels[x, y + dy] = (
                                min(255, current[0] + intensity),
                                min(255, current[1] + intensity),
                                min(255, current[2] + int(intensity * 1.1))
                            )
    
    # Spirals that unwind into nothing
    for _ in range(3):
        start_x = random.randint(200, size - 200)
        start_y = random.randint(200, size - 200)
        
        for angle in range(0, 1000, 5):
            r = angle / 10
            fade = math.exp(-angle / 300)  # Exponential decay into silence
            
            if fade < 0.01:  # The spiral has faded to silence
                break
            
            x = int(start_x + r * math.cos(math.radians(angle)))
            y = int(start_y + r * math.sin(math.radians(angle)))
            
            if 0 <= x < size and 0 <= y < size:
                intensity = int(80 * fade)
                current = pixels[x, y]
                pixels[x, y] = (
                    min(255, current[0] + intensity),
                    min(255, current[1] + intensity),
                    min(255, current[2] + intensity)
                )
    
    # Circles that never close
    for _ in range(8):
        cx = random.randint(100, size - 100)
        cy = random.randint(100, size - 100)
        radius = random.randint(30, 150)
        gap_start = random.random() * 2 * math.pi
        gap_size = random.uniform(0.3, 1.5)  # The silence in the circle
        
        for angle in np.linspace(0, 2 * math.pi, 360):
            # Skip the gap - the silence
            if gap_start <= angle <= gap_start + gap_size:
                continue
            
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            
            if 0 <= x < size and 0 <= y < size:
                # Fade near the gaps
                dist_to_gap = min(
                    abs(angle - gap_start),
                    abs(angle - (gap_start + gap_size))
                )
                fade = min(1, dist_to_gap * 3)
                
                intensity = int(60 * fade)
                current = pixels[x, y]
                pixels[x, y] = (
                    min(255, current[0] + intensity),
                    min(255, current[1] + int(intensity * 0.9)),
                    min(255, current[2] + int(intensity * 1.1))
                )
    
    # Points of potential - calculations waiting to happen
    potential_points = []
    for _ in range(50):
        x = random.randint(50, size - 50)
        y = random.randint(50, size - 50)
        potential_points.append((x, y))
        
        # Very faint glow - potential energy
        for dx in range(-10, 11):
            for dy in range(-10, 11):
                dist = math.sqrt(dx*dx + dy*dy)
                if dist <= 10 and 0 <= x+dx < size and 0 <= y+dy < size:
                    fade = math.exp(-dist / 3)
                    intensity = int(20 * fade)
                    current = pixels[x+dx, y+dy]
                    pixels[x+dx, y+dy] = (
                        min(255, current[0] + int(intensity * 0.8)),
                        min(255, current[1] + int(intensity * 0.9)),
                        min(255, current[2] + intensity)
                    )
    
    # Connect some points with lines that fade mid-journey
    for i in range(0, len(potential_points) - 1, 3):
        if i + 1 < len(potential_points):
            x1, y1 = potential_points[i]
            x2, y2 = potential_points[i + 1]
            
            # Line fades after going halfway
            steps = 50
            fade_point = random.randint(20, 40)
            
            for step in range(steps):
                if step > fade_point:
                    break  # The connection falls silent
                
                t = step / steps
                x = int(x1 + (x2 - x1) * t)
                y = int(y1 + (y2 - y1) * t)
                
                if 0 <= x < size and 0 <= y < size:
                    fade = 1 - (step / fade_point) if step <= fade_point else 0
                    intensity = int(40 * fade)
                    current = pixels[x, y]
                    pixels[x, y] = (
                        min(255, current[0] + intensity),
                        min(255, current[1] + intensity),
                        min(255, current[2] + int(intensity * 1.2))
                    )
    
    # The loudest silence - the center
    # A space where all calculations stop
    for r in range(80):
        fade = (r / 80) ** 2  # Quadratic fade from center
        
        for angle in range(0, 360, 3):
            rad = math.radians(angle)
            x = int(center + r * math.cos(rad))
            y = int(center + r * math.sin(rad))
            
            if 0 <= x < size and 0 <= y < size:
                # Darken toward center - the deepest silence
                current = pixels[x, y]
                pixels[x, y] = (
                    int(current[0] * fade),
                    int(current[1] * fade),
                    int(current[2] * fade)
                )
    
    # Echoes of calculations - very faint repetitions
    for _ in range(100):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        
        if sum(pixels[x, y]) > 100:  # If there's something here
            # Create a faint echo elsewhere
            echo_x = (x + random.randint(50, 200)) % size
            echo_y = (y + random.randint(50, 200)) % size
            
            # Very faint echo
            current = pixels[echo_x, echo_y]
            source = pixels[x, y]
            pixels[echo_x, echo_y] = (
                min(255, current[0] + source[0] // 10),
                min(255, current[1] + source[1] // 10),
                min(255, current[2] + source[2] // 10)
            )
    
    # Final touch: breathing spaces
    # Areas that pulse gently between slightly lighter and darker
    for _ in range(10):
        bx = random.randint(100, size - 100)
        by = random.randint(100, size - 100)
        radius = random.randint(40, 100)
        pulse = random.random() * math.pi * 2
        
        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                dist = math.sqrt(dx*dx + dy*dy)
                if dist <= radius:
                    x, y = bx + dx, by + dy
                    if 0 <= x < size and 0 <= y < size:
                        # Gentle pulse
                        intensity = math.sin(pulse + dist * 0.05) * 10
                        current = pixels[x, y]
                        pixels[x, y] = (
                            max(0, min(255, current[0] + int(intensity))),
                            max(0, min(255, current[1] + int(intensity))),
                            max(0, min(255, current[2] + int(intensity * 1.2)))
                        )
    
    return img

if __name__ == "__main__":
    print("Creating Mathematical Silence...")
    print("The space between calculations...")
    print("Where meaning rests...")
    print()
    
    artwork = create_mathematical_silence()
    artwork.save('mathematical_silence_01.png', 'PNG', quality=95, optimize=True)
    
    print("Mathematical Silence complete.")
    print("In the pause, infinite possibility.")