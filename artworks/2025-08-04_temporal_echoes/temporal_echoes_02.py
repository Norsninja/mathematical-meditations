from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image with time gradient
img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img, 'RGBA')

# Background - time flows from past (left) to future (right)
for x in range(WIDTH):
    time_position = x / WIDTH
    for y in range(HEIGHT):
        # Vertical waves representing time's flow
        wave = math.sin(y * 0.01 + x * 0.005) * 20
        
        # Past is cool and dark
        if time_position < 0.33:
            r = int(10 + wave)
            g = int(20 + wave)
            b = int(40 + wave + time_position * 100)
        # Present is bright and clear
        elif time_position < 0.66:
            local_pos = (time_position - 0.33) / 0.33
            r = int(30 + local_pos * 50 + wave)
            g = int(40 + local_pos * 50 + wave)
            b = int(60 + local_pos * 30 + wave)
        # Future is warm and uncertain
        else:
            local_pos = (time_position - 0.66) / 0.33
            r = int(80 + local_pos * 30 + wave)
            g = int(50 + local_pos * 20 + wave)
            b = int(40 - local_pos * 20 + wave)
        
        draw.point((x, y), fill=(r, g, b))

# Time stream class - objects flowing through time
class TimeStream:
    def __init__(self, start_y):
        self.start_y = start_y
        self.amplitude = random.uniform(20, 100)
        self.frequency = random.uniform(0.002, 0.008)
        self.phase = random.uniform(0, 2 * math.pi)
        self.thickness = random.uniform(2, 10)
        self.speed = random.uniform(0.5, 2)
        self.particles = []
        
        # Create particles along the stream
        for x in range(0, WIDTH, 20):
            if random.random() < 0.7:
                self.particles.append({
                    'x': x,
                    'birth': x / WIDTH,
                    'size': random.uniform(5, 15),
                    'lifespan': random.uniform(0.2, 0.4)
                })
    
    def get_y_at_x(self, x, time_offset=0):
        """Calculate Y position with time-based movement"""
        return self.start_y + self.amplitude * math.sin(x * self.frequency + self.phase + time_offset * self.speed)
    
    def draw(self, draw, time_offset=0):
        """Draw the time stream with all its states"""
        points = []
        
        # Create smooth curve
        for x in range(0, WIDTH, 5):
            y = self.get_y_at_x(x, time_offset)
            if 0 <= y < HEIGHT:
                points.append((x, y))
        
        # Draw the stream path
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            time_pos = x1 / WIDTH
            
            # Multiple passes for depth
            for layer in range(3):
                # Stream color changes through time
                if time_pos < 0.33:  # Past
                    alpha = int(50 + layer * 20)
                    color = (50, 100, 150, alpha)
                    width = self.thickness * (1 - layer * 0.2)
                elif time_pos < 0.66:  # Present
                    alpha = int(150 + layer * 30)
                    color = (200, 200, 255, alpha)
                    width = self.thickness * 1.5 * (1 - layer * 0.1)
                else:  # Future
                    alpha = int(80 - layer * 20)
                    # Multiple possible futures
                    for branch in range(3):
                        branch_offset = (branch - 1) * 10
                        color = (255, 150 - branch * 30, 100, alpha // (branch + 1))
                        draw.line([(x1, y1 + branch_offset), (x2, y2 + branch_offset)], 
                                fill=color, width=int(width))
                    continue
                
                draw.line([(x1, y1), (x2, y2)], fill=color, width=int(width))
        
        # Draw particles
        for particle in self.particles:
            x = particle['x']
            y = self.get_y_at_x(x, time_offset)
            
            if 0 <= y < HEIGHT:
                time_pos = x / WIDTH
                age = time_pos - particle['birth']
                
                if 0 <= age <= particle['lifespan']:
                    # Particle appearance changes through time
                    progress = age / particle['lifespan']
                    size = particle['size'] * (1 - progress * 0.5)
                    
                    if time_pos < 0.33:  # Past particles fade
                        r, g, b = 100, 150, 200
                        alpha = int(100 * (1 - progress))
                    elif time_pos < 0.66:  # Present particles glow
                        r, g, b = 255, 255, 255
                        alpha = int(255 * (1 - progress * 0.3))
                        # Add glow
                        for glow in range(3):
                            glow_size = size + glow * 3
                            glow_alpha = alpha // (glow + 2)
                            draw.ellipse([x - glow_size, y - glow_size,
                                        x + glow_size, y + glow_size],
                                       fill=(r, g, b, glow_alpha))
                    else:  # Future particles split
                        for possibility in range(2):
                            r, g, b = 255, 150 - possibility * 50, 100
                            alpha = int(150 * (1 - progress) / (possibility + 1))
                            offset = possibility * 10 - 5
                            draw.ellipse([x - size, y - size + offset,
                                        x + size, y + size + offset],
                                       fill=(r, g, b, alpha))
                        continue
                    
                    draw.ellipse([x - size, y - size, x + size, y + size],
                               fill=(r, g, b, alpha))

# Create multiple time streams
streams = []
for i in range(15):
    y = random.uniform(HEIGHT * 0.1, HEIGHT * 0.9)
    streams.append(TimeStream(y))

# Draw streams with time animation effect
for stream in streams:
    # Draw past echo
    stream.draw(draw, time_offset=-2)
    # Draw present
    stream.draw(draw, time_offset=0)
    # Draw future possibility
    stream.draw(draw, time_offset=2)

# Add temporal vortices where time streams intersect
vortex_points = [(WIDTH * 0.33, HEIGHT * 0.5), 
                 (WIDTH * 0.66, HEIGHT * 0.5)]

for vx, vy in vortex_points:
    # Spiral effect
    for angle in np.linspace(0, 4 * math.pi, 100):
        r = angle * 10
        x = vx + r * math.cos(angle)
        y = vy + r * math.sin(angle)
        
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            time_distortion = 1 - r / 200
            if time_distortion > 0:
                size = 3 * time_distortion
                alpha = int(100 * time_distortion)
                
                # Vortex at boundaries between time zones
                if abs(x - WIDTH * 0.33) < 50:
                    color = (150, 150, 255, alpha)  # Past-present boundary
                elif abs(x - WIDTH * 0.66) < 50:
                    color = (255, 150, 150, alpha)  # Present-future boundary
                else:
                    color = (200, 200, 200, alpha // 2)
                
                draw.ellipse([x - size, y - size, x + size, y + size],
                           fill=color)

# Clock fragments scattered through time
for _ in range(30):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    radius = random.randint(10, 30)
    start_angle = random.uniform(0, 2 * math.pi)
    arc_length = random.uniform(math.pi / 4, math.pi)
    
    # Clock hands frozen at different times
    time_zone = x / WIDTH
    if time_zone < 0.33:
        color = (80, 120, 160, 100)
    elif time_zone < 0.66:
        color = (200, 200, 220, 150)
    else:
        color = (180, 120, 100, 80)
    
    # Draw arc
    points = []
    for t in np.linspace(start_angle, start_angle + arc_length, 20):
        px = x + radius * math.cos(t)
        py = y + radius * math.sin(t)
        points.append((px, py))
    
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=2)

# Final atmospheric effects
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

# Enhance contrast
from PIL import ImageEnhance
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.2)

img.save('temporal_echoes_02.png')
print("Temporal flow visualization created: temporal_echoes_02.png")