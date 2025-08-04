from PIL import Image, ImageDraw
import numpy as np
import math
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create the image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(10, 10, 15))
pixels = img.load()

# Wave parameters
waves = [
    # (amplitude, frequency, phase, angle)
    (80, 0.02, 0, 0),
    (60, 0.03, math.pi/3, math.pi/6),
    (70, 0.025, math.pi/2, math.pi/4),
    (50, 0.015, 0, math.pi/3),
    (40, 0.035, math.pi, math.pi/2),
]

# Calculate wave interference at each pixel
for x in range(WIDTH):
    for y in range(HEIGHT):
        # Center coordinates
        cx = x - WIDTH / 2
        cy = y - HEIGHT / 2
        
        # Sum wave contributions
        total = 0
        phase_sum = 0
        
        for amp, freq, phase, angle in waves:
            # Rotate coordinates by wave angle
            rx = cx * math.cos(angle) - cy * math.sin(angle)
            ry = cx * math.sin(angle) + cy * math.cos(angle)
            
            # Calculate wave value
            distance = math.sqrt(rx*rx + ry*ry)
            wave_value = amp * math.sin(distance * freq + phase)
            total += wave_value
            
            # Track phase for color calculation
            phase_sum += (distance * freq + phase) % (2 * math.pi)
        
        # Normalize and map to color
        normalized = (total + 200) / 400  # Normalize to 0-1
        normalized = max(0, min(1, normalized))
        
        # Color based on interference pattern and phase
        hue = (phase_sum / (2 * math.pi * len(waves))) % 1.0
        
        # Saturation varies with amplitude
        saturation = 0.3 + 0.7 * abs(normalized - 0.5) * 2
        
        # Value creates the interference pattern
        value = normalized
        
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))

# Add subtle radial gradient overlay
draw = ImageDraw.Draw(img)
for i in range(100):
    radius = WIDTH * (1 - i/100)
    alpha = int(255 * (i/100) * 0.3)
    # Create darker edges
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.ellipse(
        [WIDTH/2 - radius, HEIGHT/2 - radius, 
         WIDTH/2 + radius, HEIGHT/2 + radius],
        fill=(10, 10, 20, alpha)
    )
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

img.save('resonance_01.png')
print("Resonance piece created: resonance_01.png")