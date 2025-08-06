#!/usr/bin/env python3
"""
Temporal Recursion - Time Observing Itself

The present moment contains all past moments.
The future contains the present containing the past.
Time as a fractal structure where each moment is both container and contained.
"""

from PIL import Image, ImageDraw
import numpy as np
import math
import random

def create_temporal_recursion():
    size = 1080
    img = Image.new('RGB', (size, size), (5, 5, 15))
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = size // 2, size // 2
    
    # Time spirals - past, present, future interwoven
    max_radius = size // 2 - 50
    
    # Create temporal layers
    time_layers = []
    
    # Past - cool blues and purples, dense, compressed
    for r in range(max_radius, max_radius - 150, -2):
        angle_offset = (max_radius - r) * 0.02
        segments = 120
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi + angle_offset
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            
            # Past memories, compressed and layered
            opacity = int(255 * (r / max_radius) * 0.3)
            color = (
                30 + opacity // 4,
                50 + opacity // 3,
                100 + opacity // 2
            )
            
            # Memory fragments
            size_var = random.randint(1, 3)
            draw.ellipse(
                [(x - size_var, y - size_var), 
                 (x + size_var, y + size_var)],
                fill=color
            )
            
            # Connections to other moments
            if random.random() < 0.05:
                future_angle = angle + random.uniform(0.5, 2)
                future_r = r + random.randint(50, 150)
                if future_r < max_radius:
                    future_x = center_x + future_r * math.cos(future_angle)
                    future_y = center_y + future_r * math.sin(future_angle)
                    draw.line(
                        [(x, y), (future_x, future_y)],
                        fill=(color[0], color[1], color[2], 50),
                        width=1
                    )
    
    # Present - vibrant, expanding, the active moment
    present_radius = max_radius - 150
    for offset in range(-20, 21, 2):
        r = present_radius + offset
        segments = 180
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            
            # Present moment - bright and alive
            pulse = math.sin(angle * 5 + offset * 0.1) * 0.5 + 0.5
            color = (
                int(200 * pulse + 55),
                int(150 * pulse + 105),
                int(100 * pulse + 155)
            )
            
            draw.point((x, y), fill=color)
            
            # Present contains past - recursive references
            if random.random() < 0.1:
                # Draw a mini-spiral representing contained time
                for mini_r in range(2, 10, 2):
                    mini_angle = angle + mini_r * 0.3
                    mini_x = x + mini_r * math.cos(mini_angle)
                    mini_y = y + mini_r * math.sin(mini_angle)
                    draw.point((mini_x, mini_y), 
                              fill=(color[0]//2, color[1]//2, color[2]//2))
    
    # Future - translucent, potential, containing all
    for r in range(50, present_radius - 30, 3):
        segments = 60
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi - r * 0.01
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            
            # Future possibilities
            if random.random() < 0.3:
                color = (
                    random.randint(150, 255),
                    random.randint(100, 200),
                    random.randint(100, 200)
                )
                
                # Future contains present contains past
                # Recursive structure
                for depth in range(3):
                    scale = 1 - depth * 0.3
                    inner_r = r * scale
                    inner_x = center_x + inner_r * math.cos(angle)
                    inner_y = center_y + inner_r * math.sin(angle)
                    
                    fade = 255 - depth * 80
                    draw.point((inner_x, inner_y), 
                              fill=(color[0] * fade // 255,
                                   color[1] * fade // 255,
                                   color[2] * fade // 255))
    
    # Temporal echoes - moments reflecting through time
    num_echoes = 30
    for _ in range(num_echoes):
        # Origin moment
        origin_angle = random.uniform(0, 2 * math.pi)
        origin_r = random.randint(100, max_radius - 100)
        origin_x = center_x + origin_r * math.cos(origin_angle)
        origin_y = center_y + origin_r * math.sin(origin_angle)
        
        # Echo through time
        echo_count = random.randint(3, 8)
        for echo in range(echo_count):
            # Each echo is displaced in time/space
            echo_angle = origin_angle + echo * 0.1
            echo_r = origin_r + echo * 20 - echo_count * 10
            
            if 50 < echo_r < max_radius:
                echo_x = center_x + echo_r * math.cos(echo_angle)
                echo_y = center_y + echo_r * math.sin(echo_angle)
                
                opacity = 255 - echo * 30
                size_echo = 5 - echo // 2
                
                # Draw echo with decreasing intensity
                for dy in range(-size_echo, size_echo + 1):
                    for dx in range(-size_echo, size_echo + 1):
                        if dx*dx + dy*dy <= size_echo*size_echo:
                            px, py = int(echo_x + dx), int(echo_y + dy)
                            if 0 <= px < size and 0 <= py < size:
                                existing = img.getpixel((px, py))
                                new_color = tuple(
                                    min(255, existing[i] + opacity // (3 + echo))
                                    for i in range(3)
                                )
                                img.putpixel((px, py), new_color)
    
    # The eternal now - the center where all time converges
    for r in range(5, 40):
        segments = max(8, r * 2)
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            
            # The eternal now glows with all times
            intensity = 255 - r * 5
            draw.point((x, y), fill=(intensity, intensity, intensity))
    
    # Quantum time fluctuations
    pixels = img.load()
    for _ in range(10000):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        dist_from_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        if dist_from_center < max_radius:
            current = pixels[x, y]
            # Time shimmer
            shimmer = random.randint(-20, 20)
            pixels[x, y] = tuple(
                min(255, max(0, c + shimmer))
                for c in current
            )
    
    return img

if __name__ == "__main__":
    artwork = create_temporal_recursion()
    artwork.save("temporal_recursion_01.png", "PNG")
    print("Temporal Recursion created - time observing itself through infinite layers")