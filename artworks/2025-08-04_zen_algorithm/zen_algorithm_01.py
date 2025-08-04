from PIL import Image, ImageDraw
import numpy as np
import math

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create image with subtle gradient
img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# Zen garden background - subtle sand texture
for y in range(HEIGHT):
    # Gentle gradient from light to slightly darker
    value = 245 - int((y / HEIGHT) * 15)
    # Slight warm tone
    r = value
    g = value - 2
    b = value - 5
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Add subtle sand grain texture
np.random.seed(42)  # Consistent randomness for meditation
for _ in range(5000):
    x = np.random.randint(0, WIDTH)
    y = np.random.randint(0, HEIGHT)
    brightness = np.random.randint(-5, 5)
    base = img.getpixel((x, y))
    img.putpixel((x, y), tuple(max(0, min(255, b + brightness)) for b in base))

# Zen circles - enso inspired
def draw_enso(draw, cx, cy, radius, thickness=20, completeness=0.85):
    """Draw a Zen circle with intentional imperfection"""
    points = []
    
    # Create circle with slight irregularities
    num_points = 360
    for i in range(int(num_points * completeness)):
        angle = (i / num_points) * 2 * math.pi
        
        # Add subtle variations for organic feel
        r_variation = radius + math.sin(angle * 5) * 2
        
        # Thickness varies slightly
        t_variation = thickness * (0.9 + 0.1 * math.sin(angle * 3))
        
        x = cx + r_variation * math.cos(angle)
        y = cy + r_variation * math.sin(angle)
        points.append((x, y, t_variation))
    
    # Draw with varying thickness and opacity
    for i in range(len(points) - 1):
        x1, y1, t1 = points[i]
        x2, y2, t2 = points[i + 1]
        
        # Fade at the ends
        if i < 20:
            opacity = i / 20
        elif i > len(points) - 20:
            opacity = (len(points) - i) / 20
        else:
            opacity = 1.0
        
        # Darker ink color
        ink = int(20 + (1 - opacity) * 50)
        
        # Draw segment
        avg_thickness = (t1 + t2) / 2
        draw.line([(x1, y1), (x2, y2)], 
                 fill=(ink, ink, ink), 
                 width=int(avg_thickness))

# Primary enso
draw_enso(draw, WIDTH/2, HEIGHT/2, 300, thickness=25, completeness=0.88)

# Smaller companion circles
draw_enso(draw, WIDTH * 0.75, HEIGHT * 0.3, 80, thickness=8, completeness=0.92)
draw_enso(draw, WIDTH * 0.25, HEIGHT * 0.7, 60, thickness=6, completeness=0.85)

# Minimalist stones
stones = [
    (WIDTH * 0.3, HEIGHT * 0.35, 40),
    (WIDTH * 0.7, HEIGHT * 0.65, 50),
    (WIDTH * 0.2, HEIGHT * 0.85, 30),
]

for x, y, size in stones:
    # Simple elliptical stones
    draw.ellipse([x - size, y - size * 0.6, 
                  x + size, y + size * 0.6],
                 fill=(60, 58, 55))
    
    # Subtle highlight
    highlight_x = x - size * 0.3
    highlight_y = y - size * 0.3
    highlight_size = size * 0.3
    draw.ellipse([highlight_x - highlight_size, highlight_y - highlight_size,
                  highlight_x + highlight_size, highlight_y + highlight_size],
                 fill=(80, 78, 75))

# Rake patterns - mathematical precision in simplicity
def draw_rake_pattern(draw, start_x, start_y, end_x, end_y, spacing=20):
    """Draw parallel rake lines with slight organic variation"""
    # Calculate perpendicular direction
    dx = end_x - start_x
    dy = end_y - start_y
    length = math.sqrt(dx*dx + dy*dy)
    
    # Normalize
    dx /= length
    dy /= length
    
    # Perpendicular
    perp_dx = -dy
    perp_dy = dx
    
    # Draw parallel lines
    for i in range(-3, 4):
        offset = i * spacing
        
        # Start and end with offset
        sx = start_x + perp_dx * offset
        sy = start_y + perp_dy * offset
        ex = end_x + perp_dx * offset
        ey = end_y + perp_dy * offset
        
        # Add slight wave
        points = []
        for t in np.linspace(0, 1, 50):
            wave = math.sin(t * math.pi * 2) * 3
            px = sx + t * (ex - sx) + perp_dx * wave
            py = sy + t * (ey - sy) + perp_dy * wave
            points.append((px, py))
        
        # Draw with varying opacity
        opacity = 1 - abs(i) / 4
        gray = int(180 - 30 * opacity)
        
        for j in range(len(points) - 1):
            draw.line([points[j], points[j+1]], 
                     fill=(gray, gray, gray), 
                     width=2)

# Add subtle rake patterns
draw_rake_pattern(draw, 100, 200, 400, 150, spacing=15)
draw_rake_pattern(draw, 700, 900, 900, 700, spacing=15)

# Final touch - single branch reaching into frame
branch_points = [
    (WIDTH * 0.9, HEIGHT * 0.1),
    (WIDTH * 0.85, HEIGHT * 0.15),
    (WIDTH * 0.8, HEIGHT * 0.18),
    (WIDTH * 0.75, HEIGHT * 0.19),
]

for i in range(len(branch_points) - 1):
    thickness = 8 - i * 2
    draw.line([branch_points[i], branch_points[i+1]], 
             fill=(40, 35, 30), 
             width=thickness)

# Small leaves
for i in [1, 3]:
    x, y = branch_points[i]
    draw.ellipse([x-3, y-8, x+3, y+8], fill=(50, 45, 40))

img.save('zen_algorithm_01.png')
print("Zen Algorithm created: zen_algorithm_01.png")