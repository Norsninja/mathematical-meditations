"""
Entropy Garden 03 - Thermodynamic Bloom

The second law of thermodynamics states that entropy always increases,
but what if we could see this not as decay but as a garden blooming
into maximum beauty? This piece visualizes entropy as a creative force.
"""

import numpy as np
from PIL import Image, ImageDraw
import colorsys
from scipy.ndimage import gaussian_filter, rotate
from scipy.interpolate import interp1d

# The canvas of possibilities
width, height = 1080, 1080
img = Image.new('RGB', (width, height), (8, 8, 12))
draw = ImageDraw.Draw(img)

# Initialize random with golden ratio for aesthetic distribution
np.random.seed(161803)

# Create temperature field - hot spots of high energy
temperature_field = np.zeros((height, width))
energy_sources = 15

for _ in range(energy_sources):
    cx, cy = np.random.randint(100, width-100), np.random.randint(100, height-100)
    intensity = np.random.uniform(0.5, 1.0)
    radius = np.random.randint(50, 150)
    
    for py in range(max(0, cy-radius), min(height, cy+radius)):
        for px in range(max(0, cx-radius), min(width, cx+radius)):
            dist_sq = (px - cx)**2 + (py - cy)**2
            if dist_sq <= radius**2:
                temperature_field[py, px] += intensity * np.exp(-dist_sq / (radius**2 / 4))

# Smooth the temperature field
temperature_field = gaussian_filter(temperature_field, sigma=30)
temperature_field = temperature_field / temperature_field.max()

# Create color field based on temperature and entropy
color_field = np.zeros((height, width, 3))

for y in range(height):
    for x in range(width):
        temp = temperature_field[y, x]
        
        # Color mapping: cold=blue through hot=red, but with entropy variations
        if temp < 0.2:
            hue = 0.6 + 0.1 * temp  # Blue to cyan
        elif temp < 0.5:
            hue = 0.5 - 0.3 * (temp - 0.2)  # Cyan to green
        elif temp < 0.8:
            hue = 0.2 - 0.2 * (temp - 0.5)  # Green to yellow
        else:
            hue = 1.0 - 0.2 * (1 - temp)  # Yellow to red
            
        # Add local entropy variations
        local_entropy = np.random.uniform(-0.05, 0.05)
        hue = (hue + local_entropy) % 1.0
        
        # Saturation decreases with entropy
        saturation = 0.8 - 0.3 * np.random.uniform(0, 1)
        value = 0.7 + 0.3 * temp
        
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        color_field[y, x] = [r * 255, g * 255, b * 255]

# Apply entropy diffusion - multiple passes with different characteristics
for i in range(3):
    # Each pass represents different time scales of entropy
    sigma = 5 + i * 3
    color_field = gaussian_filter(color_field, sigma=(sigma, sigma, 0.5))

# Draw the base entropy field
for y in range(0, height, 3):
    for x in range(0, width, 3):
        color = tuple(int(c) for c in color_field[y, x])
        draw.rectangle([x, y, x+2, y+2], fill=color)

# Entropy flow visualization - particles flowing from hot to cold
num_particles = 3000
for i in range(num_particles):
    # Start from high temperature regions
    attempts = 0
    while attempts < 10:
        start_x = np.random.randint(50, width-50)
        start_y = np.random.randint(50, height-50)
        if temperature_field[start_y, start_x] > 0.5:
            break
        attempts += 1
    
    # Particle properties
    x, y = float(start_x), float(start_y)
    energy = temperature_field[start_y, start_x]
    
    # Color based on energy
    hue = 0.1 + 0.8 * energy
    path = []
    
    # Trace particle path as it loses energy
    for step in range(80):
        if 5 < x < width-5 and 5 < y < height-5:
            # Calculate temperature gradient
            local_temp = temperature_field[int(y-2):int(y+3), int(x-2):int(x+3)]
            gy, gx = np.gradient(local_temp)
            
            # Move down gradient (toward equilibrium) with Brownian motion
            dx = -np.mean(gx) * 10 + np.random.normal(0, 3)
            dy = -np.mean(gy) * 10 + np.random.normal(0, 3)
            
            # Update position
            x = np.clip(x + dx, 0, width-1)
            y = np.clip(y + dy, 0, height-1)
            
            # Update energy (cooling)
            energy *= 0.98
            energy = max(energy, temperature_field[int(y), int(x)])
            
            # Draw segment
            if len(path) > 0:
                # Color shifts as particle cools
                segment_hue = (hue - 0.3 * (1 - energy)) % 1.0
                alpha = energy * 0.7
                
                r, g, b = colorsys.hsv_to_rgb(segment_hue, 0.6, alpha)
                draw.line([path[-1], (x, y)], 
                         fill=(int(r*255), int(g*255), int(b*255)), 
                         width=1 if energy > 0.3 else 2)
            
            path.append((x, y))

# Entropy blooms - where energy dissipation creates beauty
bloom_centers = []
for _ in range(25):
    cx, cy = np.random.randint(100, width-100), np.random.randint(100, height-100)
    
    # Blooms appear at entropy gradients
    local_var = np.var(temperature_field[cy-20:cy+20, cx-20:cx+20])
    if local_var > 0.01:
        bloom_centers.append((cx, cy))
        
        # Each bloom is unique
        petals = np.random.randint(6, 12)
        layers = np.random.randint(2, 4)
        base_size = np.random.randint(15, 35)
        
        base_temp = temperature_field[cy, cx]
        base_hue = 0.8 - 0.6 * base_temp
        
        for layer in range(layers):
            size = base_size * (1 - layer * 0.2)
            
            for p in range(petals):
                angle = (p / petals) * 2 * np.pi + layer * np.pi / petals
                
                # Petal curve
                for t in np.linspace(0, 1, 20):
                    r = size * (1 - t * 0.3) * (1 + 0.2 * np.sin(4 * t * np.pi))
                    px = cx + r * np.cos(angle + 0.1 * np.sin(3 * t * np.pi))
                    py = cy + r * np.sin(angle + 0.1 * np.sin(3 * t * np.pi))
                    
                    # Petal color varies with position
                    petal_hue = (base_hue + 0.1 * t + 0.05 * layer) % 1.0
                    saturation = 0.5 + 0.3 * (1 - t)
                    value = 0.8 - 0.2 * layer
                    
                    r_color, g_color, b_color = colorsys.hsv_to_rgb(petal_hue, saturation, value)
                    
                    size_point = int(3 * (1 - t))
                    if size_point > 0:
                        draw.ellipse([px-size_point, py-size_point, 
                                    px+size_point, py+size_point],
                                   fill=(int(r_color*255), int(g_color*255), 
                                        int(b_color*255), int(200*(1-t))))

# Final touch - entropy wisps
for _ in range(200):
    x = np.random.randint(width)
    y = np.random.randint(height)
    
    if temperature_field[y, x] > 0.3:
        # Wisp properties from local conditions
        length = int(20 + 30 * temperature_field[y, x])
        angle = np.random.uniform(0, 2 * np.pi)
        
        wisp_hue = (0.7 - 0.5 * temperature_field[y, x]) % 1.0
        
        for i in range(length):
            t = i / length
            # Wisp curves slightly
            curve = 0.3 * np.sin(3 * t * np.pi)
            wx = x + i * np.cos(angle + curve)
            wy = y + i * np.sin(angle + curve)
            
            if 0 <= wx < width and 0 <= wy < height:
                alpha = (1 - t) * 0.5
                r, g, b = colorsys.hsv_to_rgb(wisp_hue, 0.3, alpha)
                draw.point((wx, wy), fill=(int(r*255), int(g*255), int(b*255)))

# Save this thermodynamic garden
img.save('entropy_garden_03.png', 'PNG', quality=95, optimize=True)
print("The Entropy Garden is complete: Beauty emerges from dissolution")