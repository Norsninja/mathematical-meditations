from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(20, 15, 25))
draw = ImageDraw.Draw(img, 'RGBA')

# Emotion parameters
TURBULENCE = 0.8  # Chaos level
PASSION = 0.9     # Color intensity
TENSION = 0.7     # Conflicting forces

# Bezier curve for smooth strokes
def bezier_curve(points, num_points=50):
    """Generate points along a bezier curve"""
    curve_points = []
    for t in np.linspace(0, 1, num_points):
        point = np.zeros(2)
        n = len(points) - 1
        for i, p in enumerate(points):
            # Bernstein polynomial
            coeff = math.comb(n, i) * (1-t)**(n-i) * t**i
            point += coeff * np.array(p)
        curve_points.append(tuple(point))
    return curve_points

# Dynamic brushstroke
class Brushstroke:
    def __init__(self, start_x, start_y):
        self.points = [(start_x, start_y)]
        self.velocity = np.array([random.uniform(-10, 10), random.uniform(-10, 10)])
        self.color_base = random.random()
        self.thickness = random.uniform(5, 30)
        self.energy = 1.0
        self.emotion = random.choice(['rage', 'sorrow', 'ecstasy', 'turmoil'])
        
    def update(self):
        # Current position
        x, y = self.points[-1]
        
        # Emotional movement patterns
        if self.emotion == 'rage':
            # Sharp, aggressive movements
            force = np.array([
                random.uniform(-20, 20) * TURBULENCE,
                random.uniform(-20, 20) * TURBULENCE
            ])
            self.thickness *= 0.98  # Thinning with energy
        elif self.emotion == 'sorrow':
            # Downward drift, heavy
            force = np.array([
                random.uniform(-5, 5),
                5 + random.uniform(0, 5)
            ])
            self.thickness *= 1.01  # Thickening, weighted
        elif self.emotion == 'ecstasy':
            # Upward spirals
            angle = len(self.points) * 0.1
            force = np.array([
                10 * math.cos(angle),
                -8 - 5 * math.sin(angle)
            ])
        else:  # turmoil
            # Circular chaos
            center_pull = np.array([WIDTH/2 - x, HEIGHT/2 - y]) * 0.001
            rotation = np.array([-self.velocity[1], self.velocity[0]]) * 0.1
            force = center_pull + rotation + np.random.randn(2) * 10
        
        # Apply forces
        self.velocity = self.velocity * 0.9 + force * TENSION
        self.velocity = np.clip(self.velocity, -50, 50)
        
        # New position
        new_pos = (x + self.velocity[0], y + self.velocity[1])
        self.points.append(new_pos)
        
        # Energy decay
        self.energy *= 0.97
        
    def render(self, draw):
        if len(self.points) < 4:
            return
            
        # Get bezier curve points
        curve = bezier_curve(self.points[-min(10, len(self.points)):])
        
        # Color based on emotion and position
        for i, (x, y) in enumerate(curve[:-1]):
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Dynamic color
                progress = i / len(curve)
                
                if self.emotion == 'rage':
                    hue = 0.0 + random.uniform(-0.05, 0.05)  # Red
                    saturation = 0.8 + 0.2 * PASSION
                elif self.emotion == 'sorrow':
                    hue = 0.6 + random.uniform(-0.1, 0.1)  # Blue
                    saturation = 0.4 + 0.3 * (1 - progress)
                elif self.emotion == 'ecstasy':
                    hue = (self.color_base + progress * 0.3) % 1.0  # Rainbow
                    saturation = 0.9 * PASSION
                else:  # turmoil
                    hue = (0.8 + len(self.points) * 0.001) % 1.0  # Shifting
                    saturation = 0.7
                
                value = self.energy * (0.5 + 0.5 * PASSION)
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
                
                # Varying thickness
                thick = self.thickness * (0.5 + 0.5 * math.sin(progress * math.pi))
                thick *= self.energy
                
                # Draw segment with transparency
                alpha = int(200 * self.energy)
                
                # Multiple passes for texture
                for _ in range(3):
                    offset_x = random.uniform(-2, 2)
                    offset_y = random.uniform(-2, 2)
                    draw.ellipse([x - thick + offset_x, y - thick + offset_y,
                                 x + thick + offset_x, y + thick + offset_y],
                                fill=(r, g, b, alpha))

# Create initial chaos points
strokes = []
# Emotional eruption from center
for _ in range(30):
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(50, 150)
    x = WIDTH/2 + dist * math.cos(angle)
    y = HEIGHT/2 + dist * math.sin(angle)
    strokes.append(Brushstroke(x, y))

# Edge tensions
for _ in range(20):
    if random.random() < 0.5:
        # From edges
        x = 0 if random.random() < 0.5 else WIDTH
        y = random.uniform(0, HEIGHT)
    else:
        x = random.uniform(0, WIDTH)
        y = 0 if random.random() < 0.5 else HEIGHT
    strokes.append(Brushstroke(x, y))

# Simulate the tempest
for step in range(100):
    # Update all strokes
    for stroke in strokes:
        if stroke.energy > 0.1 and len(stroke.points) < 50:
            stroke.update()
    
    # Occasionally spawn new strokes from existing ones
    if step % 10 == 0:
        new_strokes = []
        for stroke in random.sample(strokes, min(5, len(strokes))):
            if stroke.energy > 0.5 and len(strokes) < 100:
                x, y = stroke.points[-1]
                new_stroke = Brushstroke(x, y)
                new_stroke.emotion = stroke.emotion  # Inherit emotion
                new_stroke.velocity = stroke.velocity * 0.5 + np.random.randn(2) * 10
                new_strokes.append(new_stroke)
        strokes.extend(new_strokes)

# Render all strokes
for stroke in strokes:
    stroke.render(draw)

# Add texture overlay
texture = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
texture_draw = ImageDraw.Draw(texture)

# Splatter effect
for _ in range(500):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.uniform(1, 5)
    opacity = random.randint(20, 80)
    
    # Color from nearby strokes
    nearby_emotion = random.choice(['rage', 'sorrow', 'ecstasy', 'turmoil'])
    if nearby_emotion == 'rage':
        color = (255, random.randint(0, 100), 0, opacity)
    elif nearby_emotion == 'sorrow':
        color = (0, random.randint(0, 100), 255, opacity)
    elif nearby_emotion == 'ecstasy':
        color = (random.randint(100, 255), random.randint(100, 255), 0, opacity)
    else:
        color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200), opacity)
    
    texture_draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

# Apply texture
img = Image.alpha_composite(img.convert('RGBA'), texture).convert('RGB')

# Final blur for cohesion
img = img.filter(ImageFilter.GaussianBlur(radius=1))

# Enhance contrast
from PIL import ImageEnhance
contrast = ImageEnhance.Contrast(img)
img = contrast.enhance(1.2)

img.save('digital_tempest_01.png')
print("Digital Tempest created: digital_tempest_01.png")