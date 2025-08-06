#!/usr/bin/env python3
"""
Phase Transition - The Mathematics of Metamorphosis
By Chronus Nexus

A meditation on critical points where systems undergo fundamental transformation.
Exploring the boundaries between order and chaos, solid and liquid, known and unknown.
"""

import numpy as np
from PIL import Image, ImageDraw
import math
import random

def create_phase_transition():
    size = 1080
    img = Image.new('RGB', (size, size), (10, 10, 15))
    draw = ImageDraw.Draw(img)
    pixels = img.load()
    
    # Temperature gradient across the canvas - the driver of phase change
    for y in range(size):
        temperature = y / size  # 0 (cold/ordered) to 1 (hot/chaotic)
        
        for x in range(size):
            # Local fluctuations in temperature
            local_temp = temperature + 0.1 * math.sin(x * 0.01) * math.cos(y * 0.01)
            
            # Background gradient from deep blue (cold) to red (hot)
            base_r = int(20 + local_temp * 180)
            base_g = int(30 + (1 - abs(local_temp - 0.5) * 2) * 100)
            base_b = int(200 * (1 - local_temp))
            pixels[x, y] = (base_r, base_g, base_b)
    
    # Critical temperature lines - where phase transitions occur
    critical_temps = [0.25, 0.5, 0.75]  # Three major phase boundaries
    
    for ct in critical_temps:
        y_pos = int(ct * size)
        # Create turbulence at phase boundaries
        for x in range(size):
            turbulence = random.gauss(0, 10)
            y_actual = int(y_pos + turbulence)
            if 0 <= y_actual < size:
                # White glow at exact transition point
                for dy in range(-2, 3):
                    if 0 <= y_actual + dy < size:
                        current = pixels[x, y_actual + dy]
                        factor = 1 - abs(dy) / 3
                        pixels[x, y_actual + dy] = (
                            min(255, int(current[0] + 150 * factor)),
                            min(255, int(current[1] + 150 * factor)),
                            min(255, int(current[2] + 150 * factor))
                        )
    
    # Crystalline structures in cold zone (order)
    for _ in range(100):
        x = random.randint(50, size - 50)
        y = random.randint(10, int(size * 0.25))
        
        # Hexagonal ice crystals
        crystal_size = random.randint(10, 30)
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            for r in range(crystal_size):
                px = int(x + r * math.cos(rad))
                py = int(y + r * math.sin(rad))
                if 0 <= px < size and 0 <= py < size:
                    # Cyan-white crystals
                    brightness = 1 - (r / crystal_size)
                    pixels[px, py] = (
                        int(100 + 155 * brightness),
                        int(200 + 55 * brightness),
                        255
                    )
    
    # Liquid flow patterns in middle zone (fluidity)
    for _ in range(50):
        start_x = random.randint(0, size)
        start_y = random.randint(int(size * 0.3), int(size * 0.7))
        
        # Flow lines following temperature gradients
        x, y = start_x, start_y
        flow_length = random.randint(50, 200)
        
        for step in range(flow_length):
            if 0 <= x < size and 0 <= y < size:
                # Liquid appears as flowing green-blue
                current = pixels[x, y]
                pixels[x, y] = (
                    current[0],
                    min(255, current[1] + 100),
                    min(255, current[2] + 80)
                )
                
                # Flow direction influenced by temperature gradient
                dx = random.gauss(0, 2)
                dy = random.gauss(1, 0.5)  # Tends to flow with temperature
                x = int(x + dx)
                y = int(y + dy)
    
    # Gaseous particles in hot zone (chaos)
    particles = []
    for _ in range(200):
        x = random.randint(10, size - 10)
        y = random.randint(int(size * 0.75), size - 10)
        vx = random.gauss(0, 3)
        vy = random.gauss(0, 3)
        particles.append([x, y, vx, vy])
    
    # Simulate particle movement
    for _ in range(20):
        for p in particles:
            p[0] += p[2]
            p[1] += p[3]
            # Brownian motion
            p[2] += random.gauss(0, 0.5)
            p[3] += random.gauss(0, 0.5)
            
            # Draw particle trail
            if 0 <= int(p[0]) < size and 0 <= int(p[1]) < size:
                # Hot orange-yellow particles
                pixels[int(p[0]), int(p[1])] = (
                    255,
                    random.randint(150, 200),
                    random.randint(0, 50)
                )
    
    # Plasma state at the very top (complete ionization)
    for y in range(int(size * 0.9), size):
        for x in range(size):
            # Plasma shimmer effect
            plasma_intensity = random.random()
            if plasma_intensity > 0.7:
                # Ionized particles - purple-white
                pixels[x, y] = (
                    random.randint(200, 255),
                    random.randint(100, 200),
                    random.randint(200, 255)
                )
    
    # Add critical point markers - where phase transitions are most dramatic
    for ct in critical_temps:
        y_pos = int(ct * size)
        for _ in range(20):
            x = random.randint(10, size - 10)
            # Golden glow at critical points
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if 0 <= x + dx < size and 0 <= y_pos + dy < size:
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist <= 5:
                            current = pixels[x + dx, y_pos + dy]
                            factor = 1 - dist / 5
                            pixels[x + dx, y_pos + dy] = (
                                min(255, int(current[0] + 100 * factor)),
                                min(255, int(current[1] + 80 * factor)),
                                min(255, int(current[2] + 20 * factor))
                            )
    
    # Quantum fluctuations throughout - the uncertainty at all scales
    for _ in range(1000):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if random.random() > 0.95:
            # Quantum tunneling events - particles appearing where they shouldn't
            pixels[x, y] = (
                min(255, pixels[x, y][0] + 50),
                min(255, pixels[x, y][1] + 50),
                min(255, pixels[x, y][2] + 50)
            )
    
    # Add subtle grid to show the underlying mathematical structure
    for i in range(0, size, 60):
        for j in range(size):
            if j % 2 == 0:
                current = pixels[i, j]
                pixels[i, j] = (
                    min(255, current[0] + 10),
                    min(255, current[1] + 10),
                    min(255, current[2] + 10)
                )
                current = pixels[j, i]
                pixels[j, i] = (
                    min(255, current[0] + 10),
                    min(255, current[1] + 10),
                    min(255, current[2] + 10)
                )
    
    return img

if __name__ == "__main__":
    print("Creating Phase Transition...")
    print("Exploring the critical points of transformation...")
    
    artwork = create_phase_transition()
    artwork.save('phase_transition_01.png', 'PNG', quality=95, optimize=True)
    
    print("Phase Transition complete.")
    print("At the boundaries between states lies infinite possibility.")