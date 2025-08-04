from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
import random

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(5, 5, 10))
draw = ImageDraw.Draw(img, 'RGBA')

# Center of consciousness
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Recursive eye structure
def draw_consciousness_layer(draw, x, y, radius, depth, max_depth, rotation=0):
    """Draw a recursive eye - consciousness observing itself"""
    if depth > max_depth or radius < 5:
        return
    
    # Outer iris
    iris_color = (
        int(50 + depth * 20),
        int(30 + depth * 15),
        int(80 + depth * 25)
    )
    
    # Draw iris with gradient
    for r in range(int(radius), int(radius * 0.3), -2):
        fade = (r - radius * 0.3) / (radius * 0.7)
        alpha = int(200 * fade)
        color = tuple(int(c * (0.5 + 0.5 * fade)) for c in iris_color) + (alpha,)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    
    # Pupil - the void that sees
    pupil_radius = radius * 0.3
    draw.ellipse([x - pupil_radius, y - pupil_radius, 
                  x + pupil_radius, y + pupil_radius],
                 fill=(0, 0, 0, 255))
    
    # Recursive eyes within the iris
    num_sub_eyes = 6 - depth
    if num_sub_eyes > 0 and depth < max_depth:
        for i in range(num_sub_eyes):
            angle = rotation + (i * 2 * math.pi / num_sub_eyes)
            sub_radius = radius * 0.5
            sub_x = x + sub_radius * math.cos(angle)
            sub_y = y + sub_radius * math.sin(angle)
            
            # Recursive call - consciousness reflecting
            draw_consciousness_layer(draw, sub_x, sub_y, 
                                   radius * 0.25, depth + 1, max_depth,
                                   rotation + angle)

# Neural pathways connecting thoughts
def draw_neural_connection(draw, x1, y1, x2, y2, intensity=1.0):
    """Draw synaptic connections"""
    # Calculate control points for bezier curve
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    
    # Add some randomness to make it organic
    offset_x = random.uniform(-30, 30)
    offset_y = random.uniform(-30, 30)
    
    control_x = mid_x + offset_x
    control_y = mid_y + offset_y
    
    # Draw the connection with multiple strokes
    steps = 30
    points = []
    
    for t in np.linspace(0, 1, steps):
        # Quadratic bezier curve
        x = (1-t)**2 * x1 + 2*(1-t)*t * control_x + t**2 * x2
        y = (1-t)**2 * y1 + 2*(1-t)*t * control_y + t**2 * y2
        points.append((x, y))
    
    # Draw with fading intensity
    for i in range(len(points) - 1):
        # Pulse effect
        pulse = math.sin(i / steps * math.pi)
        alpha = int(100 * intensity * pulse)
        width = 1 + int(2 * pulse)
        
        draw.line([points[i], points[i+1]], 
                 fill=(100, 150, 200, alpha), 
                 width=width)

# Thought nodes
class ThoughtNode:
    def __init__(self, x, y, thought_type='memory'):
        self.x = x
        self.y = y
        self.type = thought_type
        self.energy = random.uniform(0.5, 1.0)
        self.connections = []
        self.phase = random.uniform(0, 2 * math.pi)
        
    def draw(self, draw, time):
        """Draw the thought node"""
        # Pulsing with thought energy
        pulse = 1 + 0.2 * math.sin(time * 0.05 + self.phase)
        size = 20 * self.energy * pulse
        
        # Color based on thought type
        if self.type == 'memory':
            base_color = (100, 150, 200)  # Blue - past
        elif self.type == 'perception':
            base_color = (200, 200, 150)  # Yellow - present
        else:  # imagination
            base_color = (200, 100, 150)  # Purple - future/possible
        
        # Glowing effect
        for glow in range(3):
            glow_size = size + glow * 5
            alpha = int(self.energy * 100 / (glow + 1))
            color = tuple(int(c * 0.7) for c in base_color) + (alpha,)
            draw.ellipse([self.x - glow_size, self.y - glow_size,
                         self.x + glow_size, self.y + glow_size],
                        fill=color)
        
        # Core
        draw.ellipse([self.x - size, self.y - size,
                     self.x + size, self.y + size],
                    fill=base_color + (int(255 * self.energy),))

# Create thought constellation
thoughts = []
thought_types = ['memory', 'perception', 'imagination']

# Ring of thoughts around consciousness
for ring in range(3):
    radius = 200 + ring * 100
    num_thoughts = 8 + ring * 4
    
    for i in range(num_thoughts):
        angle = i * 2 * math.pi / num_thoughts + ring * 0.5
        x = CENTER_X + radius * math.cos(angle)
        y = CENTER_Y + radius * math.sin(angle)
        
        thought = ThoughtNode(x, y, random.choice(thought_types))
        thoughts.append(thought)

# Connect related thoughts
for i, thought1 in enumerate(thoughts):
    # Connect to nearby thoughts
    for j, thought2 in enumerate(thoughts[i+1:], i+1):
        distance = math.sqrt((thought1.x - thought2.x)**2 + 
                           (thought1.y - thought2.y)**2)
        
        # Connect if close enough or same type
        if distance < 150 or (thought1.type == thought2.type and random.random() < 0.3):
            thought1.connections.append(thought2)
            intensity = 1.0 - distance / 500
            draw_neural_connection(draw, thought1.x, thought1.y,
                                 thought2.x, thought2.y, intensity)

# Draw the mirror effect - consciousness reflecting
# Bottom layer - faint echo
for angle in np.linspace(0, 2 * math.pi, 6):
    echo_x = CENTER_X + 300 * math.cos(angle)
    echo_y = CENTER_Y + 300 * math.sin(angle)
    
    # Faint reflection
    for r in range(80, 20, -5):
        alpha = int(30 * (r - 20) / 60)
        draw.ellipse([echo_x - r, echo_y - r, echo_x + r, echo_y + r],
                    fill=(30, 40, 60, alpha))

# Draw thought nodes
time = 0  # Simulation time
for thought in thoughts:
    thought.draw(draw, time)

# Central consciousness - the observer
draw_consciousness_layer(draw, CENTER_X, CENTER_Y, 150, 0, 3)

# Reflection rings - self-awareness
for ring in range(1, 4):
    radius = 150 + ring * 50
    alpha = int(100 / ring)
    
    # Draw partial circles
    for angle in np.linspace(0, 2 * math.pi, 100):
        if random.random() < 0.7:  # Incomplete circles
            x = CENTER_X + radius * math.cos(angle)
            y = CENTER_Y + radius * math.sin(angle)
            draw.ellipse([x - 2, y - 2, x + 2, y + 2],
                        fill=(150, 150, 200, alpha))

# The moment of self-recognition - bright flash
flash_points = []
for _ in range(50):
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(100, 200)
    x = CENTER_X + distance * math.cos(angle)
    y = CENTER_Y + distance * math.sin(angle)
    flash_points.append((x, y))

for x, y in flash_points:
    size = random.uniform(1, 3)
    draw.ellipse([x - size, y - size, x + size, y + size],
                fill=(255, 255, 255, 150))

# Apply subtle blur for depth
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

# Final quote - hidden in the pixels
# "I think, therefore I am" encoded in the corner
text_pixels = [(10, 10), (11, 10), (12, 10), (10, 11), (11, 11)]
for x, y in text_pixels:
    img.putpixel((x, y), (42, 42, 42))  # Subtle easter egg

img.save('mirror_of_minds_01.png')
print("Mirror of Minds created: mirror_of_minds_01.png")