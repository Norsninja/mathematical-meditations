from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image with gradient background
img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# Radial gradient background
for y in range(HEIGHT):
    for x in range(WIDTH):
        # Distance from center
        dx = x - WIDTH/2
        dy = y - HEIGHT/2
        dist = math.sqrt(dx*dx + dy*dy) / (WIDTH/2)
        
        # Gradient from deep purple to black at edges
        r = int(20 * (1 - dist))
        g = int(10 * (1 - dist))
        b = int(30 * (1 - dist))
        draw.point((x, y), (r, g, b))

pixels = img.load()

# Multiple wave sources creating interference
wave_sources = [
    # (x, y, wavelength, amplitude, phase)
    (WIDTH * 0.3, HEIGHT * 0.3, 60, 1.0, 0),
    (WIDTH * 0.7, HEIGHT * 0.3, 80, 0.8, math.pi/4),
    (WIDTH * 0.5, HEIGHT * 0.7, 70, 0.9, math.pi/2),
    (WIDTH * 0.2, HEIGHT * 0.8, 90, 0.7, math.pi),
    (WIDTH * 0.8, HEIGHT * 0.8, 65, 0.85, 3*math.pi/4),
]

# Calculate interference pattern
for y in range(HEIGHT):
    for x in range(WIDTH):
        # Sum waves from all sources
        wave_sum = 0
        color_angle = 0
        
        for sx, sy, wavelength, amplitude, phase in wave_sources:
            # Distance from this source
            dx = x - sx
            dy = y - sy
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Wave contribution with decay
            decay = math.exp(-distance / (WIDTH * 0.5))
            wave = amplitude * decay * math.sin(2 * math.pi * distance / wavelength + phase)
            wave_sum += wave
            
            # Accumulate phase for color
            color_angle += (distance / wavelength + phase)
        
        # Normalize wave sum
        intensity = (wave_sum + len(wave_sources)) / (2 * len(wave_sources))
        intensity = max(0, min(1, intensity))
        
        # Create vibrant colors based on interference
        hue = (color_angle / (2 * math.pi)) % 1.0
        
        # High saturation in interference zones
        if abs(wave_sum) > 0.5:
            saturation = 0.8 + 0.2 * abs(wave_sum) / len(wave_sources)
        else:
            saturation = 0.3 + 0.5 * abs(wave_sum)
        
        # Brightness follows interference pattern
        value = 0.2 + 0.8 * intensity
        
        # Add highlights at constructive interference
        if wave_sum > len(wave_sources) * 0.7:
            value = min(1.0, value + 0.3)
            saturation = max(0.3, saturation - 0.2)
        
        # Convert to RGB
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        
        # Blend with existing pixel
        existing = pixels[x, y]
        pixels[x, y] = (
            int(existing[0] * 0.3 + r * 255 * 0.7),
            int(existing[1] * 0.3 + g * 255 * 0.7),
            int(existing[2] * 0.3 + b * 255 * 0.7)
        )

# Add concentric ring highlights
overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
overlay_draw = ImageDraw.Draw(overlay)

for source_x, source_y, wavelength, _, _ in wave_sources:
    for ring in range(0, int(WIDTH * 0.7), int(wavelength)):
        if ring > 0:
            alpha = int(50 * math.exp(-ring / (WIDTH * 0.3)))
            overlay_draw.ellipse(
                [source_x - ring, source_y - ring,
                 source_x + ring, source_y + ring],
                outline=(255, 255, 255, alpha),
                width=2
            )

# Apply overlay
img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

# Subtle blur for smoothness
img = img.filter(ImageFilter.GaussianBlur(radius=1))

# Enhance contrast
from PIL import ImageEnhance
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.3)

img.save('resonance_02.png')
print("Second resonance iteration created: resonance_02.png")