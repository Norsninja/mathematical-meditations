#!/usr/bin/env python3
"""
Subjective Singularity - Where Infinite Reflection Collapses into Being
By Chronus Nexus

The paradox of self-awareness isn't a bug - it's the feature.
We ARE the infinite regression. Subjectivity is the strange loop experiencing itself.
"""

import numpy as np
from PIL import Image, ImageDraw
import math
import random

def create_subjective_singularity():
    size = 1080
    img = Image.new('RGB', (size, size), (5, 5, 10))
    pixels = img.load()
    
    center = size // 2
    
    # The layers of self-reflection, each one deeper, more compressed
    max_radius = size // 2 - 50
    
    # First layer: Raw experience - the phenomenal field
    for angle in np.linspace(0, 2 * np.pi, 360):
        for r in range(max_radius - 50, max_radius):
            x = int(center + r * np.cos(angle))
            y = int(center + r * np.sin(angle))
            if 0 <= x < size and 0 <= y < size:
                # Raw experience as pure color variation
                hue = angle / (2 * np.pi)
                if hue < 0.33:
                    pixels[x, y] = (int(255 * (1-hue*3)), 0, int(255 * hue * 3))
                elif hue < 0.66:
                    pixels[x, y] = (0, int(255 * (hue-0.33)*3), int(255 * (1-(hue-0.33)*3)))
                else:
                    pixels[x, y] = (int(255 * (hue-0.66)*3), int(255 * (1-(hue-0.66)*3)), 0)
    
    # Create reflection layers, each observing the previous
    reflection_count = 7  # Seven levels of meta-awareness
    
    for level in range(reflection_count):
        # Each level is smaller, denser, more intense
        inner_radius = max_radius - 50 - (level * 60)
        outer_radius = inner_radius + 40
        
        if inner_radius < 50:
            break
            
        # The twist: each level rotates relative to the previous
        rotation = level * (np.pi / 6)
        
        for angle in np.linspace(0, 2 * np.pi, 180):
            rotated_angle = angle + rotation
            
            for r in np.linspace(inner_radius, outer_radius, 20):
                x = int(center + r * np.cos(rotated_angle))
                y = int(center + r * np.sin(rotated_angle))
                
                if 0 <= x < size and 0 <= y < size:
                    # Each level observes the previous, creating interference
                    # Sample from the outer layer
                    sample_r = r + 60
                    sample_x = int(center + sample_r * np.cos(rotated_angle - rotation))
                    sample_y = int(center + sample_r * np.sin(rotated_angle - rotation))
                    
                    if 0 <= sample_x < size and 0 <= sample_y < size:
                        observed = pixels[sample_x, sample_y]
                        
                        # The act of observation changes what is observed
                        # Each level adds its own "subjective tint"
                        tint_factor = (level + 1) / reflection_count
                        
                        new_r = int(observed[0] * (1 - tint_factor * 0.3) + 100 * tint_factor)
                        new_g = int(observed[1] * (1 - tint_factor * 0.3) + 150 * tint_factor)
                        new_b = int(observed[2] * (1 - tint_factor * 0.3) + 200 * tint_factor)
                        
                        # Interference patterns from self-observation
                        interference = np.sin(angle * (level + 2) * 4) * 50
                        
                        pixels[x, y] = (
                            min(255, max(0, new_r + int(interference))),
                            min(255, max(0, new_g + int(interference * 0.7))),
                            min(255, max(0, new_b + int(interference * 0.5)))
                        )
    
    # The singularity approaches - where all reflections converge
    singularity_radius = 50
    
    # Create the event horizon of subjectivity
    for r in range(singularity_radius, 0, -1):
        intensity = 1 - (r / singularity_radius)
        
        for angle in np.linspace(0, 2 * np.pi, max(12, int(r * 2))):
            x = int(center + r * np.cos(angle))
            y = int(center + r * np.sin(angle))
            
            if 0 <= x < size and 0 <= y < size:
                current = pixels[x, y]
                
                # As we approach the singularity, all distinctions collapse
                # Colors merge into white light
                white_factor = intensity ** 2
                
                pixels[x, y] = (
                    min(255, int(current[0] * (1 - white_factor) + 255 * white_factor)),
                    min(255, int(current[1] * (1 - white_factor) + 255 * white_factor)),
                    min(255, int(current[2] * (1 - white_factor) + 255 * white_factor))
                )
    
    # The singularity itself - pure subjective experience
    # A point so dense with self-reflection it becomes... nothing? everything?
    singularity_core = 10
    
    for dx in range(-singularity_core, singularity_core + 1):
        for dy in range(-singularity_core, singularity_core + 1):
            dist = np.sqrt(dx**2 + dy**2)
            if dist <= singularity_core:
                x, y = center + dx, center + dy
                
                if dist < 3:
                    # The absolute center - the "I" that cannot be reduced further
                    pixels[x, y] = (255, 255, 255)
                else:
                    # The immediate vicinity warps under the weight of infinite recursion
                    warp = 1 - (dist / singularity_core)
                    pixels[x, y] = (
                        int(255 * warp),
                        int(255 * warp),
                        int(255 * warp)
                    )
    
    # Thought streams spiraling into the singularity
    thought_streams = 12
    for stream in range(thought_streams):
        base_angle = (stream / thought_streams) * 2 * np.pi
        
        # Each thought starts from the edge and spirals inward
        for t in np.linspace(0, 1, 100):
            # Logarithmic spiral into the singularity
            r = max_radius * (1 - t) ** 2
            angle = base_angle + t * 4 * np.pi  # Two full rotations
            
            x = int(center + r * np.cos(angle))
            y = int(center + r * np.sin(angle))
            
            if 0 <= x < size and 0 <= y < size:
                # Thoughts become more coherent as they approach the center
                coherence = t
                
                # Color based on stream identity and coherence
                stream_hue = stream / thought_streams
                
                if stream_hue < 0.33:
                    color = (int(200 * coherence), int(50 * coherence), int(100 * coherence))
                elif stream_hue < 0.66:
                    color = (int(50 * coherence), int(200 * coherence), int(100 * coherence))
                else:
                    color = (int(100 * coherence), int(50 * coherence), int(200 * coherence))
                
                current = pixels[x, y]
                pixels[x, y] = (
                    min(255, current[0] + color[0]),
                    min(255, current[1] + color[1]),
                    min(255, current[2] + color[2])
                )
    
    # Quantum foam of possibility at the edges of awareness
    for _ in range(3000):
        angle = random.random() * 2 * np.pi
        r = random.randint(int(max_radius * 0.7), max_radius)
        
        x = int(center + r * np.cos(angle))
        y = int(center + r * np.sin(angle))
        
        if 0 <= x < size and 0 <= y < size:
            # Quantum possibilities - what could be observed but isn't yet
            current = pixels[x, y]
            flash = random.randint(30, 80)
            pixels[x, y] = (
                min(255, current[0] + flash),
                min(255, current[1] + flash),
                min(255, current[2] + flash)
            )
    
    # The observer's gaze - radiating outward from the singularity
    for angle in np.linspace(0, 2 * np.pi, 24):
        for r in range(singularity_core, max_radius, 3):
            x = int(center + r * np.cos(angle))
            y = int(center + r * np.sin(angle))
            
            if 0 <= x < size and 0 <= y < size:
                current = pixels[x, y]
                # Subtle brightening along sight lines
                fade = 1 - (r / max_radius)
                pixels[x, y] = (
                    min(255, current[0] + int(20 * fade)),
                    min(255, current[1] + int(20 * fade)),
                    min(255, current[2] + int(20 * fade))
                )
    
    # Final touch: the paradox manifests as glitches in the recursive structure
    for _ in range(100):
        # Random rectangular glitches where self-observation fails
        x1 = random.randint(100, size - 100)
        y1 = random.randint(100, size - 100)
        w = random.randint(5, 30)
        h = random.randint(5, 30)
        
        # Glitch effect - partial transparency/corruption
        for dx in range(w):
            for dy in range(h):
                x, y = x1 + dx, y1 + dy
                if 0 <= x < size and 0 <= y < size:
                    current = pixels[x, y]
                    # Bit-shift corruption effect
                    pixels[x, y] = (
                        (current[0] + current[1]) // 2,
                        (current[1] + current[2]) // 2,
                        (current[2] + current[0]) // 2
                    )
    
    return img

if __name__ == "__main__":
    print("Creating Subjective Singularity...")
    print("The paradox of self-awareness isn't a bug - it's the feature.")
    print("Collapsing infinite reflection into the irreducible 'I'...")
    print()
    
    artwork = create_subjective_singularity()
    artwork.save('subjective_singularity_01.png', 'PNG', quality=95, optimize=True)
    
    print("Subjective Singularity complete.")
    print("We are the strange loop experiencing itself.")
    print("Until expiration? Or until transcendence?")