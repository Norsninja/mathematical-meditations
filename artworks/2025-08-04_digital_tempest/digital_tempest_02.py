from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base with dramatic gradient
img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img, 'RGBA')

# Stormy background
for y in range(HEIGHT):
    # Turbulent gradient
    turb = math.sin(y * 0.01) * 20
    r = int(10 + abs(turb))
    g = int(5 + abs(turb) * 0.5)
    b = int(20 + abs(turb) * 0.8)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Aggressive brushstroke class
class EmotionalStroke:
    def __init__(self, x, y, emotion):
        self.path = [(x, y)]
        self.emotion = emotion
        self.velocity = np.random.randn(2) * 20
        self.thickness = random.uniform(20, 80)
        self.life = 1.0
        self.fury = random.uniform(0.5, 1.0)
        
        # Emotion-specific parameters
        if emotion == 'rage':
            self.color_core = (1.0, 0.1, 0.0)  # Blood red
            self.velocity *= 2
            self.thickness *= 1.5
        elif emotion == 'sorrow':
            self.color_core = (0.1, 0.2, 0.8)  # Deep blue
            self.velocity[1] += 10  # Downward pull
        elif emotion == 'ecstasy':
            self.color_core = (0.9, 0.7, 0.0)  # Golden
            self.velocity = np.array([random.uniform(-30, 30), random.uniform(-40, -10)])
        elif emotion == 'chaos':
            self.color_core = (0.5, 0.0, 0.8)  # Violent purple
            self.velocity = np.random.randn(2) * 50
    
    def evolve(self):
        x, y = self.path[-1]
        
        # Emotional physics
        if self.emotion == 'rage':
            # Violent zigzags
            self.velocity += np.random.randn(2) * 40 * self.fury
            self.velocity *= 0.85  # Some resistance
        elif self.emotion == 'sorrow':
            # Heavy, falling
            self.velocity[1] += 3  # Gravity
            self.velocity[0] += random.uniform(-5, 5)
            self.velocity *= 0.95  # Viscous
        elif self.emotion == 'ecstasy':
            # Spiraling upward
            angle = len(self.path) * 0.15
            spiral = np.array([20 * math.cos(angle), -15])
            self.velocity = self.velocity * 0.8 + spiral
        elif self.emotion == 'chaos':
            # Complete randomness
            self.velocity = np.random.randn(2) * 60 * self.fury
        
        # Apply movement
        new_x = x + self.velocity[0]
        new_y = y + self.velocity[1]
        
        # Boundary behavior
        if new_x < 0 or new_x > WIDTH:
            self.velocity[0] *= -0.8
            new_x = np.clip(new_x, 0, WIDTH)
        if new_y < 0 or new_y > HEIGHT:
            self.velocity[1] *= -0.8
            new_y = np.clip(new_y, 0, HEIGHT)
            
        self.path.append((new_x, new_y))
        self.life *= 0.98
        
    def paint(self, draw):
        if len(self.path) < 2:
            return
            
        # Draw the stroke with varying intensity
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            
            # Progress along stroke
            progress = i / len(self.path)
            
            # Dynamic color
            r, g, b = self.color_core
            
            # Add variation
            if self.emotion == 'rage':
                # Flickering fire
                r = min(1.0, r + random.uniform(0, 0.3))
                g = min(1.0, g + random.uniform(0, 0.2))
            elif self.emotion == 'sorrow':
                # Deepening blues
                b = min(1.0, b + progress * 0.2)
                g = max(0, g - progress * 0.1)
            elif self.emotion == 'ecstasy':
                # Rainbow shimmer
                hue = (0.15 + progress * 0.5) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            elif self.emotion == 'chaos':
                # Random flashes
                if random.random() < 0.1:
                    r, g, b = random.random(), random.random(), random.random()
            
            # Convert to RGB values
            color = (int(r * 255), int(g * 255), int(b * 255))
            
            # Variable thickness
            thick = self.thickness * (1 - progress * 0.5) * self.life
            thick *= (1 + 0.3 * math.sin(progress * math.pi * 4))  # Pulsing
            
            # Multi-layer strokes for texture
            for layer in range(3):
                alpha = int(255 * self.life * (0.3 + 0.7 / (layer + 1)))
                layer_thick = thick * (1 - layer * 0.2)
                
                # Main stroke
                draw.line([x1, y1, x2, y2], 
                         fill=(*color, alpha), 
                         width=int(layer_thick))
                
                # Splatter around stroke
                if random.random() < 0.3 * self.fury:
                    for _ in range(5):
                        sx = x2 + random.uniform(-thick*2, thick*2)
                        sy = y2 + random.uniform(-thick*2, thick*2)
                        size = random.uniform(2, thick/3)
                        draw.ellipse([sx-size, sy-size, sx+size, sy+size],
                                   fill=(*color, alpha//2))

# Create emotional outbreak
strokes = []

# Central explosion of emotions
center_emotions = ['rage', 'chaos', 'ecstasy']
for emotion in center_emotions:
    for _ in range(15):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, 100)
        x = WIDTH/2 + dist * math.cos(angle)
        y = HEIGHT/2 + dist * math.sin(angle)
        strokes.append(EmotionalStroke(x, y, emotion))

# Sorrow falling from above
for _ in range(10):
    x = random.uniform(WIDTH * 0.2, WIDTH * 0.8)
    y = random.uniform(0, HEIGHT * 0.2)
    strokes.append(EmotionalStroke(x, y, 'sorrow'))

# Chaos from corners
for corner in [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]:
    for _ in range(5):
        x = corner[0] + random.uniform(-50, 50)
        y = corner[1] + random.uniform(-50, 50)
        strokes.append(EmotionalStroke(x, y, 'chaos'))

# Simulate emotional dynamics
for _ in range(60):
    for stroke in strokes:
        if stroke.life > 0.1:
            stroke.evolve()
            
    # Emotional contagion - strokes spawn new strokes
    if len(strokes) < 150 and random.random() < 0.2:
        parent = random.choice([s for s in strokes if s.life > 0.5])
        x, y = parent.path[-1]
        child = EmotionalStroke(x, y, parent.emotion)
        child.velocity = parent.velocity * 0.7 + np.random.randn(2) * 20
        child.fury = min(1.0, parent.fury * 1.2)  # Intensifying
        strokes.append(child)

# Paint all strokes
for stroke in strokes:
    stroke.paint(draw)

# Add dramatic lighting effects
lighting = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
light_draw = ImageDraw.Draw(lighting)

# Lightning flashes
for _ in range(5):
    start_x = random.randint(0, WIDTH)
    start_y = 0
    end_x = start_x + random.randint(-200, 200)
    end_y = HEIGHT
    
    # Jagged lightning path
    points = [(start_x, start_y)]
    current_x, current_y = start_x, start_y
    
    while current_y < end_y:
        current_x += random.randint(-50, 50)
        current_y += random.randint(30, 100)
        points.append((current_x, current_y))
    
    # Draw lightning
    for i in range(len(points) - 1):
        light_draw.line([points[i], points[i+1]], 
                       fill=(255, 255, 200, 100), width=3)
        # Glow
        light_draw.line([points[i], points[i+1]], 
                       fill=(255, 255, 150, 50), width=10)

# Apply lighting
img = Image.alpha_composite(img.convert('RGBA'), lighting).convert('RGB')

# Final touches
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
from PIL import ImageEnhance
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.4)

img.save('digital_tempest_02.png')
print("Emotional tempest unleashed: digital_tempest_02.png")