from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 10, 20))

# Time layers
past_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
present_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
future_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))

past_draw = ImageDraw.Draw(past_layer)
present_draw = ImageDraw.Draw(present_layer)
future_draw = ImageDraw.Draw(future_layer)

# Temporal object class
class TemporalObject:
    def __init__(self, x, y, birth_time):
        self.x = x
        self.y = y
        self.birth_time = birth_time
        self.lifespan = random.uniform(20, 80)
        self.velocity = np.array([random.uniform(-2, 2), random.uniform(-2, 2)])
        self.size = random.uniform(10, 40)
        self.frequency = random.uniform(0.05, 0.2)
        self.phase = random.uniform(0, 2 * math.pi)
        
    def position_at_time(self, t):
        """Calculate position at given time"""
        if t < self.birth_time:
            return None
        
        age = t - self.birth_time
        if age > self.lifespan:
            return None
            
        # Spiral motion through time
        spiral_factor = age * 0.1
        x = self.x + self.velocity[0] * age + 20 * math.cos(spiral_factor) * math.exp(-age/50)
        y = self.y + self.velocity[1] * age + 20 * math.sin(spiral_factor) * math.exp(-age/50)
        
        return (x, y)
    
    def state_at_time(self, t):
        """Calculate state (size, opacity, color) at given time"""
        if t < self.birth_time:
            return None
            
        age = t - self.birth_time
        if age > self.lifespan:
            return None
            
        # Size oscillates and decays
        size = self.size * (1 + 0.3 * math.sin(age * self.frequency + self.phase)) * math.exp(-age/self.lifespan)
        
        # Opacity follows life cycle
        if age < self.lifespan * 0.2:
            opacity = age / (self.lifespan * 0.2)
        elif age > self.lifespan * 0.8:
            opacity = (self.lifespan - age) / (self.lifespan * 0.2)
        else:
            opacity = 1.0
            
        # Color shifts through time
        hue = (self.birth_time / 100 + age / self.lifespan) % 1.0
        
        return size, opacity, hue

# Create temporal objects at different times
objects = []
for t in range(0, 100, 5):
    # Objects born at different times
    num_objects = random.randint(1, 3)
    for _ in range(num_objects):
        x = random.uniform(WIDTH * 0.2, WIDTH * 0.8)
        y = random.uniform(HEIGHT * 0.2, HEIGHT * 0.8)
        objects.append(TemporalObject(x, y, t))

# Current moment in time
PRESENT = 50

# Render past echoes
for obj in objects:
    # Sample multiple past moments
    for past_t in range(0, PRESENT, 3):
        pos = obj.position_at_time(past_t)
        if pos:
            state = obj.state_at_time(past_t)
            if state:
                x, y = pos
                size, opacity, hue = state
                
                # Past is blue-shifted and fading
                r, g, b = colorsys.hsv_to_rgb(0.6, 0.7, 0.3)
                alpha = int(100 * opacity * (past_t / PRESENT))
                
                # Draw echo
                past_draw.ellipse([x - size, y - size, x + size, y + size],
                                fill=(int(r*255), int(g*255), int(b*255), alpha))

# Render present moment
for obj in objects:
    pos = obj.position_at_time(PRESENT)
    if pos:
        state = obj.state_at_time(PRESENT)
        if state:
            x, y = pos
            size, opacity, hue = state
            
            # Present is vivid and clear
            r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            alpha = int(255 * opacity)
            
            # Glowing present
            for glow_size in range(int(size * 2), 0, -5):
                glow_alpha = int(alpha * (glow_size / (size * 2)) * 0.5)
                present_draw.ellipse([x - glow_size, y - glow_size, 
                                    x + glow_size, y + glow_size],
                                   fill=(int(r*255), int(g*255), int(b*255), glow_alpha))
            
            # Core
            present_draw.ellipse([x - size, y - size, x + size, y + size],
                               fill=(int(r*255), int(g*255), int(b*255), alpha))

# Render future possibilities
for obj in objects:
    # Multiple possible futures
    for future_branch in range(3):
        # Modify object trajectory for this branch
        temp_obj = TemporalObject(obj.x, obj.y, obj.birth_time)
        temp_obj.velocity = obj.velocity + np.random.randn(2) * 0.5
        
        for future_t in range(PRESENT + 5, 100, 5):
            pos = temp_obj.position_at_time(future_t)
            if pos:
                state = temp_obj.state_at_time(future_t)
                if state:
                    x, y = pos
                    size, opacity, hue = state
                    
                    # Future is red-shifted and uncertain
                    r, g, b = colorsys.hsv_to_rgb(0.0, 0.6 - future_branch * 0.1, 0.6)
                    # Decreasing certainty
                    alpha = int(50 * opacity * (1 - (future_t - PRESENT) / 50) / (future_branch + 1))
                    
                    # Draw possibility
                    future_draw.ellipse([x - size/2, y - size/2, x + size/2, y + size/2],
                                      fill=(int(r*255), int(g*255), int(b*255), alpha))

# Time flow visualization - connecting past to future
for i in range(20):
    # Time streams
    start_x = random.uniform(0, WIDTH)
    start_y = random.uniform(0, HEIGHT)
    
    points = []
    for t in range(0, 100):
        # Time flows with some randomness
        x = start_x + t * 5 + random.uniform(-50, 50)
        y = start_y + math.sin(t * 0.1) * 50 + random.uniform(-20, 20)
        
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            points.append((x, y, t))
    
    # Draw time stream
    for j in range(len(points) - 1):
        x1, y1, t1 = points[j]
        x2, y2, t2 = points[j + 1]
        
        # Color based on time
        if t1 < PRESENT:
            # Past - blue
            color = (50, 100, 200, 30)
        elif t1 == PRESENT:
            # Present - white
            color = (255, 255, 255, 80)
        else:
            # Future - red
            color = (200, 50, 100, 20)
        
        if t1 < PRESENT:
            past_draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
        elif t1 > PRESENT:
            future_draw.line([(x1, y1), (x2, y2)], fill=color, width=1)

# Composite layers with time distortion
img = img.convert('RGBA')

# Past is blurred (memory)
past_layer = past_layer.filter(ImageFilter.GaussianBlur(radius=3))
img = Image.alpha_composite(img, past_layer)

# Present is sharp
img = Image.alpha_composite(img, present_layer)

# Future is fragmented (uncertainty)
future_layer = future_layer.filter(ImageFilter.GaussianBlur(radius=1))
img = Image.alpha_composite(img, future_layer)

# Add temporal grid distortion
grid_draw = ImageDraw.Draw(img)
for x in range(0, WIDTH, 40):
    for y in range(0, HEIGHT, 40):
        # Grid bends near present moment
        dist_from_center = math.sqrt((x - WIDTH/2)**2 + (y - HEIGHT/2)**2)
        if dist_from_center < 200:
            # Distortion factor
            factor = 1 - dist_from_center / 200
            offset_x = (x - WIDTH/2) * factor * 0.1
            offset_y = (y - HEIGHT/2) * factor * 0.1
            
            grid_draw.point((x + offset_x, y + offset_y), fill=(100, 100, 150, 50))

img = img.convert('RGB')
img.save('temporal_echoes_01.png')
print("Temporal Echoes created: temporal_echoes_01.png")