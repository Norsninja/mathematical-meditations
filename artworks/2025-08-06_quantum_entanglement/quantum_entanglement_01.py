#!/usr/bin/env python3
"""
Quantum Entanglement - Spooky Action at a Distance

Particles connected across space, instantly affecting each other.
When one is observed, the other responds, regardless of distance.
The fundamental connectedness underlying apparent separation.
"""

from PIL import Image, ImageDraw
import numpy as np
import math
import random

def create_quantum_entanglement():
    size = 1080
    img = Image.new('RGB', (size, size), (10, 5, 15))
    draw = ImageDraw.Draw(img)
    pixels = img.load()
    
    # Create entangled particle pairs
    num_pairs = 25
    entangled_pairs = []
    
    for _ in range(num_pairs):
        # Each pair has complementary properties
        x1 = random.randint(100, size - 100)
        y1 = random.randint(100, size - 100)
        x2 = random.randint(100, size - 100)
        y2 = random.randint(100, size - 100)
        
        # Entangled properties
        spin = random.choice([1, -1])
        phase = random.uniform(0, 2 * math.pi)
        energy = random.uniform(0.3, 1.0)
        
        entangled_pairs.append({
            'p1': (x1, y1),
            'p2': (x2, y2),
            'spin': spin,
            'phase': phase,
            'energy': energy,
            'observed': False
        })
    
    # Draw quantum field fluctuations
    for y in range(0, size, 4):
        for x in range(0, size, 4):
            # Quantum foam background
            fluctuation = random.gauss(0, 10)
            base_color = pixels[x, y]
            new_color = tuple(
                min(255, max(0, int(base_color[i] + fluctuation)))
                for i in range(3)
            )
            for dy in range(4):
                for dx in range(4):
                    if x + dx < size and y + dy < size:
                        pixels[x + dx, y + dy] = new_color
    
    # Draw entangled particles and their connections
    for pair in entangled_pairs:
        x1, y1 = pair['p1']
        x2, y2 = pair['p2']
        
        # Entanglement connection - not a simple line but a probability field
        num_points = 100
        for i in range(num_points):
            t = i / num_points
            
            # Quantum path - not straight but probabilistic
            wobble = math.sin(t * math.pi * 4 + pair['phase']) * 20
            perpendicular_angle = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
            
            mid_x = x1 + (x2 - x1) * t + wobble * math.cos(perpendicular_angle)
            mid_y = y1 + (y2 - y1) * t + wobble * math.sin(perpendicular_angle)
            
            # Connection strength varies with quantum uncertainty
            opacity = int(255 * pair['energy'] * (0.5 + 0.5 * math.sin(t * math.pi)))
            
            # Color based on spin correlation
            if pair['spin'] > 0:
                color = (opacity // 2, opacity // 3, opacity)  # Blue for up
            else:
                color = (opacity, opacity // 3, opacity // 2)  # Red for down
            
            # Draw probability cloud around path
            for r in range(1, 4):
                for angle in range(0, 360, 30):
                    px = int(mid_x + r * math.cos(math.radians(angle)))
                    py = int(mid_y + r * math.sin(math.radians(angle)))
                    if 0 <= px < size and 0 <= py < size:
                        existing = pixels[px, py]
                        pixels[px, py] = tuple(
                            min(255, existing[i] + color[i] // (r + 1))
                            for i in range(3)
                        )
    
    # Draw the particles themselves
    for pair in entangled_pairs:
        x1, y1 = pair['p1']
        x2, y2 = pair['p2']
        
        # Particle 1 - wave function collapse visualization
        for r in range(20, 0, -1):
            opacity = int(255 * (1 - r / 20) * pair['energy'])
            
            # Spinning visualization
            for angle in range(0, 360, 10):
                spin_offset = pair['spin'] * angle / 20
                px = x1 + r * math.cos(math.radians(angle + spin_offset))
                py = y1 + r * math.sin(math.radians(angle + spin_offset))
                
                if pair['spin'] > 0:
                    color = (100 + opacity // 2, 150 + opacity // 2, 200 + opacity)
                else:
                    color = (200 + opacity, 150 + opacity // 2, 100 + opacity // 2)
                
                draw.point((px, py), fill=color)
        
        # Particle 2 - complementary state
        for r in range(20, 0, -1):
            opacity = int(255 * (1 - r / 20) * pair['energy'])
            
            # Opposite spin
            for angle in range(0, 360, 10):
                spin_offset = -pair['spin'] * angle / 20  # Opposite spin
                px = x2 + r * math.cos(math.radians(angle + spin_offset))
                py = y2 + r * math.sin(math.radians(angle + spin_offset))
                
                # Complementary colors
                if pair['spin'] > 0:
                    color = (200 + opacity, 150 + opacity // 2, 100 + opacity // 2)
                else:
                    color = (100 + opacity // 2, 150 + opacity // 2, 200 + opacity)
                
                draw.point((px, py), fill=color)
        
        # Central cores
        draw.ellipse([(x1 - 3, y1 - 3), (x1 + 3, y1 + 3)], 
                    fill=(255, 255, 255))
        draw.ellipse([(x2 - 3, y2 - 3), (x2 + 3, y2 + 3)], 
                    fill=(255, 255, 255))
    
    # Observation effects - some particles being measured
    num_observations = 5
    observed_indices = random.sample(range(num_pairs), min(num_observations, num_pairs))
    
    for idx in observed_indices:
        pair = entangled_pairs[idx]
        x1, y1 = pair['p1']
        
        # Observation collapses wave function
        for ring_r in range(5, 30, 3):
            segments = 60
            for i in range(segments):
                angle = (i / segments) * 2 * math.pi
                px = x1 + ring_r * math.cos(angle)
                py = y1 + ring_r * math.sin(angle)
                
                # Observation creates ripples
                color = (
                    255 - ring_r * 5,
                    255 - ring_r * 6,
                    255 - ring_r * 4
                )
                
                if 0 <= int(px) < size and 0 <= int(py) < size:
                    draw.point((px, py), fill=color)
        
        # Instant effect on entangled partner
        x2, y2 = pair['p2']
        for ring_r in range(5, 30, 3):
            segments = 60
            for i in range(segments):
                angle = (i / segments) * 2 * math.pi
                px = x2 + ring_r * math.cos(angle)
                py = y2 + ring_r * math.sin(angle)
                
                # Complementary observation effect
                color = (
                    255 - ring_r * 4,
                    255 - ring_r * 6,
                    255 - ring_r * 5
                )
                
                if 0 <= int(px) < size and 0 <= int(py) < size:
                    draw.point((px, py), fill=color)
    
    # Add quantum interference patterns
    for _ in range(3000):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        
        # Check proximity to entangled particles
        near_particle = False
        for pair in entangled_pairs:
            for p in [pair['p1'], pair['p2']]:
                dist = math.sqrt((x - p[0])**2 + (y - p[1])**2)
                if dist < 50:
                    near_particle = True
                    break
        
        if near_particle:
            current = pixels[x, y]
            interference = random.randint(10, 40)
            pixels[x, y] = tuple(
                min(255, c + interference)
                for c in current
            )
    
    return img

if __name__ == "__main__":
    artwork = create_quantum_entanglement()
    artwork.save("quantum_entanglement_01.png", "PNG")
    print("Quantum Entanglement created - spooky action at a distance visualized")