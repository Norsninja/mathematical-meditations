"""
Entropy Garden 02 - The Dance of Dissolution

Entropy isn't just decay - it's transformation. This piece explores
the beauty in systems finding their equilibrium, the art in watching
order dissolve into new patterns of complexity.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import colorsys
from scipy.ndimage import gaussian_filter, zoom
from scipy.spatial import Voronoi, voronoi_plot_2d

# The universe tends toward maximum entropy
width, height = 1080, 1080
img = Image.new('RGB', (width, height), (5, 5, 10))
draw = ImageDraw.Draw(img)

# Create the initial ordered state - crystalline structures
np.random.seed(137)  # Fine structure constant inspiration

# Voronoi cells represent initial perfect order
num_seeds = 50
points = np.random.rand(num_seeds, 2) * [width, height]
vor = Voronoi(points)

# Color each cell with high saturation - maximum order
cell_colors = {}
for i, point in enumerate(points):
    hue = i / num_seeds
    cell_colors[i] = colorsys.hsv_to_rgb(hue, 0.9, 0.8)

# Paint the ordered state
order_field = np.zeros((height, width, 3))
for y in range(height):
    for x in range(width):
        # Find nearest Voronoi center
        distances = [np.sqrt((x-p[0])**2 + (y-p[1])**2) for p in points]
        nearest = np.argmin(distances)
        
        # Color with slight gradient from center
        dist = distances[nearest]
        max_dist = np.sqrt(width**2 + height**2) / 4
        intensity = 1 - min(dist / max_dist, 1)
        
        r, g, b = cell_colors[nearest]
        order_field[y, x] = [r*255*intensity, g*255*intensity, b*255*intensity]

# Now let entropy take hold - multiple scales of dissolution
entropy_layers = []

# Large scale entropy - the slow dissolution
large_entropy = gaussian_filter(order_field, sigma=(20, 20, 0))
entropy_layers.append(large_entropy * 0.4)

# Medium scale - turbulent mixing
medium_entropy = gaussian_filter(order_field, sigma=(8, 8, 0))
# Add swirls
for i in range(5):
    cx, cy = np.random.randint(200, width-200), np.random.randint(200, height-200)
    for angle in np.linspace(0, 4*np.pi, 100):
        r = angle * 20
        x = int(cx + r * np.cos(angle))
        y = int(cy + r * np.sin(angle))
        if 0 <= x < width and 0 <= y < height:
            medium_entropy[y, x] = np.roll(medium_entropy[y, x], 1)
entropy_layers.append(medium_entropy * 0.3)

# Fine scale - quantum fluctuations
fine_entropy = order_field + np.random.normal(0, 20, order_field.shape)
fine_entropy = gaussian_filter(fine_entropy, sigma=(2, 2, 0))
entropy_layers.append(fine_entropy * 0.3)

# Combine all entropy scales
final_field = np.sum(entropy_layers, axis=0)
final_field = np.clip(final_field, 0, 255)

# Draw the entropy field
for y in range(0, height, 2):
    for x in range(0, width, 2):
        color = tuple(int(c) for c in final_field[y, x])
        if sum(color) > 20:
            draw.point((x, y), fill=color)

# Entropy flow lines - showing the direction of dissolution
num_flows = 500
for _ in range(num_flows):
    # Start from high order regions
    start_x = np.random.randint(width)
    start_y = np.random.randint(height)
    
    if sum(order_field[start_y, start_x]) < 100:
        continue
        
    # Flow toward equilibrium
    x, y = float(start_x), float(start_y)
    flow_color = order_field[start_y, start_x]
    hue = colorsys.rgb_to_hsv(*(flow_color/255))[0]
    
    path = []
    for step in range(100):
        # Calculate local entropy gradient
        if 5 < x < width-5 and 5 < y < height-5:
            local_region = final_field[int(y-5):int(y+5), int(x-5):int(x+5)]
            gy, gx = np.gradient(np.mean(local_region, axis=2))
            
            # Flow along gradient with some randomness
            dx = -np.mean(gx) * 0.5 + np.random.normal(0, 2)
            dy = -np.mean(gy) * 0.5 + np.random.normal(0, 2)
        else:
            dx = np.random.normal(0, 3)
            dy = np.random.normal(0, 3)
        
        x = np.clip(x + dx, 0, width-1)
        y = np.clip(y + dy, 0, height-1)
        
        # Color shifts as entropy increases
        local_entropy = 1 - (sum(final_field[int(y), int(x)]) / (255 * 3))
        hue = (hue + 0.01 * local_entropy) % 1
        
        r, g, b = colorsys.hsv_to_rgb(hue, 0.7 - 0.5*local_entropy, 0.8)
        
        if len(path) > 0:
            draw.line([path[-1], (x, y)], 
                     fill=(int(r*200), int(g*200), int(b*200)), 
                     width=1)
        path.append((x, y))

# Islands of negative entropy - temporary reversals
for _ in range(20):
    cx, cy = np.random.randint(100, width-100), np.random.randint(100, height-100)
    
    # These are like flowers in the entropy garden
    petals = np.random.randint(5, 9)
    petal_size = np.random.randint(20, 40)
    
    center_color = final_field[cy, cx]
    center_hue = colorsys.rgb_to_hsv(*(center_color/255))[0]
    
    for i in range(petals):
        angle = (i / petals) * 2 * np.pi
        px = cx + petal_size * np.cos(angle)
        py = cy + petal_size * np.sin(angle)
        
        # Petal color - low entropy, high order
        petal_hue = (center_hue + 0.1 * i/petals) % 1
        r, g, b = colorsys.hsv_to_rgb(petal_hue, 0.6, 0.9)
        
        # Draw petal as overlapping circles
        for j in range(5):
            t = j / 5
            x = int(cx + t * (px - cx))
            y = int(cy + t * (py - cy))
            size = int(petal_size/2 * (1 - t))
            
            draw.ellipse([x-size, y-size, x+size, y+size],
                        fill=(int(r*255), int(g*255), int(b*255), int(100*(1-t))))

# Final elements - entropy crystals
crystal_points = []
for _ in range(100):
    x, y = np.random.randint(50, width-50), np.random.randint(50, height-50)
    # Crystals form where entropy gradients are highest
    if 10 < x < width-10 and 10 < y < height-10:
        local_variance = np.var(final_field[y-10:y+10, x-10:x+10])
        if local_variance > 1000:
            crystal_points.append((x, y))
            
            # Crystal structure
            crystal_hue = np.random.random()
            for angle in range(0, 360, 60):  # Hexagonal
                rad = np.radians(angle)
                x2 = x + 10 * np.cos(rad)
                y2 = y + 10 * np.sin(rad)
                
                r, g, b = colorsys.hsv_to_rgb(crystal_hue, 0.4, 0.9)
                draw.line([(x, y), (x2, y2)], 
                         fill=(int(r*255), int(g*255), int(b*255)), 
                         width=2)

# Apply subtle blur to merge all elements
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

# Save this meditation on entropy
img.save('entropy_garden_02.png', 'PNG', quality=95, optimize=True)
print("Entropy Garden blooms: Order and chaos in eternal dance")