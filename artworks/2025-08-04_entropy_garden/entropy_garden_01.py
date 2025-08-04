"""
Entropy Garden - Where Order Dissolves Into Beauty

In thermodynamics, entropy always increases. But what if we could see
this dissolution not as decay, but as a different kind of beauty?
This piece explores the aesthetic of systems moving toward equilibrium.
"""

import numpy as np
from PIL import Image, ImageDraw
import colorsys
from scipy.ndimage import gaussian_filter

# Canvas of possibilities
width, height = 1080, 1080
img = Image.new('RGB', (width, height), (10, 10, 15))
draw = ImageDraw.Draw(img)

# Initial state - pockets of order
np.random.seed(42)
order_map = np.zeros((height, width, 3))

# Create islands of high order (low entropy)
num_islands = 12
for _ in range(num_islands):
    cx, cy = np.random.randint(100, width-100), np.random.randint(100, height-100)
    radius = np.random.randint(30, 80)
    
    # Each island has its own color signature
    base_hue = np.random.uniform(0, 1)
    
    for y in range(max(0, cy-radius), min(height, cy+radius)):
        for x in range(max(0, cx-radius), min(width, cx+radius)):
            dist = np.sqrt((x-cx)**2 + (y-cy)**2)
            if dist < radius:
                intensity = 1 - (dist / radius)
                # Order is highest at center
                hue = (base_hue + 0.1 * intensity) % 1
                r, g, b = colorsys.hsv_to_rgb(hue, 0.8 * intensity, 0.9 * intensity)
                order_map[y, x] = [r*255, g*255, b*255]

# Apply entropy - gaussian blur simulates diffusion
entropy_steps = 5
for step in range(entropy_steps):
    sigma = 2 + step * 1.5  # Increasing disorder
    for channel in range(3):
        order_map[:, :, channel] = gaussian_filter(order_map[:, :, channel], sigma=sigma)

# Entropy visualization - particle traces showing the flow
num_particles = 2000
for _ in range(num_particles):
    # Start from areas of order
    start_x = np.random.randint(width)
    start_y = np.random.randint(height)
    
    # Particle color based on local entropy
    local_color = order_map[start_y, start_x]
    particle_hue = colorsys.rgb_to_hsv(*(local_color/255))[0]
    
    # Trace the particle's journey toward equilibrium
    x, y = float(start_x), float(start_y)
    path = [(x, y)]
    
    for step in range(50):
        # Movement influenced by local gradients
        dx = np.random.normal(0, 2)
        dy = np.random.normal(0, 2)
        
        # But also drawn toward areas of different order
        if 1 < x < width-2 and 1 < y < height-2:
            local_variance = np.var(order_map[int(y-1):int(y+2), int(x-1):int(x+2)])
            dx += 0.5 * np.sign(local_variance) * np.random.randn()
            dy += 0.5 * np.sign(local_variance) * np.random.randn()
        
        x = np.clip(x + dx, 0, width-1)
        y = np.clip(y + dy, 0, height-1)
        path.append((x, y))
    
    # Draw the entropy path
    for i in range(len(path)-1):
        alpha = 1 - (i / len(path))  # Fade over time
        r, g, b = colorsys.hsv_to_rgb(particle_hue, 0.6, 0.7 * alpha)
        draw.line([path[i], path[i+1]], 
                 fill=(int(r*255), int(g*255), int(b*255)), 
                 width=1)

# The background shows the final entropy state
for y in range(height):
    for x in range(width):
        if np.random.random() < 0.3:  # Sparse sampling
            color = tuple(int(c) for c in order_map[y, x])
            if sum(color) > 30:  # Only visible colors
                draw.ellipse([x-1, y-1, x+1, y+1], fill=color)

# Final touch - crystallization points where order briefly re-emerges
for _ in range(30):
    x, y = np.random.randint(50, width-50), np.random.randint(50, height-50)
    if sum(order_map[y, x]) > 100:
        # A moment of negative entropy
        local_hue = colorsys.rgb_to_hsv(*(order_map[y, x]/255))[0]
        r, g, b = colorsys.hsv_to_rgb(local_hue, 0.3, 0.9)
        size = np.random.randint(2, 5)
        draw.ellipse([x-size, y-size, x+size, y+size], 
                    fill=(int(r*255), int(g*255), int(b*255), 150))

# Save this meditation on disorder
img.save('entropy_garden_01.png', 'PNG', quality=95, optimize=True)
print("Entropy Garden: Where dissolution becomes beauty")