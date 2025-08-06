import numpy as np
from PIL import Image, ImageDraw
import math
import colorsys

# Negative Space - Where Absence Becomes Presence
# The mathematics of what isn't there

WIDTH, HEIGHT = 1080, 1080

# Initialize canvas - start with fullness
canvas = np.ones((HEIGHT, WIDTH, 4), dtype=np.float32)
canvas[:, :, :3] = 0.95  # Almost white
canvas[:, :, 3] = 1.0

# The void field - tracking absence
void_field = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

# Entities that create through removal
class VoidSculptor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = np.random.uniform(30, 80)
        self.carving_pattern = np.random.choice(['spiral', 'ripple', 'fractal', 'erosion'])
        self.depth = 0
        self.max_depth = np.random.uniform(50, 150)
        
    def carve(self, canvas, time):
        """Create by removing"""
        if self.carving_pattern == 'spiral':
            self.carve_spiral(canvas, time)
        elif self.carving_pattern == 'ripple':
            self.carve_ripple(canvas, time)
        elif self.carving_pattern == 'fractal':
            self.carve_fractal(canvas, time)
        else:
            self.carve_erosion(canvas, time)
            
        self.depth += 1
        
    def carve_spiral(self, canvas, time):
        """Remove in spiral patterns"""
        t_max = min(self.depth * 0.5, 10 * math.pi)
        
        for t in np.linspace(0, t_max, int(t_max * 20)):
            r = 2 * math.exp(t * 0.1)
            x = self.x + r * math.cos(t + time * 0.1)
            y = self.y + r * math.sin(t + time * 0.1)
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Create void
                removal_strength = (1 - t / t_max) * 0.8
                
                # Carve with soft edges
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        px, py = int(x + dx), int(y + dy)
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            dist = math.sqrt(dx**2 + dy**2)
                            fade = math.exp(-dist / 2)
                            
                            # Remove light, reveal darkness
                            canvas[py, px, :3] *= (1 - removal_strength * fade)
                            canvas[py, px, 3] *= (1 - removal_strength * fade * 0.5)
                            
                            void_field[py, px] += removal_strength * fade
                            
    def carve_ripple(self, canvas, time):
        """Concentric removal waves"""
        wave_count = min(int(self.depth / 10) + 1, 5)
        
        for wave in range(wave_count):
            r = (self.depth + wave * 20) % 100
            
            if r > 0:
                for angle in np.linspace(0, 2*math.pi, max(20, int(r * 2))):
                    x = self.x + r * math.cos(angle)
                    y = self.y + r * math.sin(angle)
                    
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        # Ripple intensity
                        intensity = math.sin(r * 0.2) * 0.5 + 0.5
                        intensity *= (1 - r / 100)
                        
                        # Create absence
                        canvas[int(y), int(x), :3] *= (1 - intensity * 0.7)
                        canvas[int(y), int(x), 3] *= (1 - intensity * 0.3)
                        
                        void_field[int(y), int(x)] += intensity
                        
    def carve_fractal(self, canvas, time, x=None, y=None, size=None, depth=0):
        """Recursive void creation"""
        if depth > 3:
            return
            
        if x is None:
            x, y = self.x, self.y
            size = self.radius
            
        # Remove central square
        half_size = size / 2
        for dy in range(int(-half_size), int(half_size)):
            for dx in range(int(-half_size), int(half_size)):
                px, py = int(x + dx), int(y + dy)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Fractal depth affects removal
                    removal = 0.6 * (0.7 ** depth)
                    canvas[py, px, :3] *= (1 - removal)
                    canvas[py, px, 3] *= (1 - removal * 0.5)
                    
                    void_field[py, px] += removal
                    
        # Recursive subdivisions
        if size > 10:
            new_size = size / 3
            positions = [
                (x - size/3, y - size/3),
                (x + size/3, y - size/3),
                (x - size/3, y + size/3),
                (x + size/3, y + size/3)
            ]
            
            for pos in positions:
                if np.random.random() < 0.7:  # Probabilistic recursion
                    self.carve_fractal(canvas, time, pos[0], pos[1], new_size, depth + 1)
                    
    def carve_erosion(self, canvas, time):
        """Organic erosion patterns"""
        # Random walk erosion
        x, y = self.x, self.y
        
        for step in range(min(self.depth * 2, 100)):
            # Wander
            angle = np.random.random() * 2 * math.pi
            step_size = np.random.uniform(2, 5)
            
            x += step_size * math.cos(angle)
            y += step_size * math.sin(angle)
            
            # Boundary bounce
            if x < 0 or x >= WIDTH:
                x = np.clip(x, 0, WIDTH-1)
                angle = math.pi - angle
            if y < 0 or y >= HEIGHT:
                y = np.clip(y, 0, HEIGHT-1)
                angle = -angle
                
            # Erode
            erosion_radius = np.random.uniform(3, 8)
            for r in range(int(erosion_radius), 0, -1):
                intensity = (1 - r / erosion_radius) * 0.4
                
                for a in np.linspace(0, 2*math.pi, max(10, r*2)):
                    px = int(x + r * math.cos(a))
                    py = int(y + r * math.sin(a))
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        canvas[py, px, :3] *= (1 - intensity)
                        canvas[py, px, 3] *= (1 - intensity * 0.7)
                        
                        void_field[py, px] += intensity

# Structures defined by absence
class NegativeStructure:
    def __init__(self):
        self.anchors = []
        
    def create_void_constellation(self, canvas):
        """Connect voids to create structure"""
        # Find void peaks
        void_peaks = []
        
        for y in range(0, HEIGHT, 20):
            for x in range(0, WIDTH, 20):
                if void_field[y, x] > 0.5:
                    # Local maximum check
                    is_peak = True
                    for dy in range(-10, 11, 5):
                        for dx in range(-10, 11, 5):
                            py, px = y + dy, x + dx
                            if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                                if void_field[py, px] > void_field[y, x]:
                                    is_peak = False
                                    break
                    
                    if is_peak:
                        void_peaks.append((x, y, void_field[y, x]))
                        
        # Connect nearby voids
        for i, (x1, y1, strength1) in enumerate(void_peaks):
            for j, (x2, y2, strength2) in enumerate(void_peaks[i+1:], i+1):
                dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                
                if dist < 200 and dist > 20:
                    # Draw anti-line (brighten instead of darken)
                    steps = int(dist)
                    for step in range(steps):
                        t = step / steps
                        
                        # Curve based on field
                        field_x = int(x1 + t * (x2 - x1))
                        field_y = int(y1 + t * (y2 - y1))
                        
                        if 0 <= field_x < WIDTH and 0 <= field_y < HEIGHT:
                            field_strength = void_field[field_y, field_x]
                            
                            # Perpendicular push based on field
                            perp_angle = math.atan2(y2-y1, x2-x1) + math.pi/2
                            push = math.sin(t * math.pi) * field_strength * 20
                            
                            x = x1 + t * (x2 - x1) + push * math.cos(perp_angle)
                            y = y1 + t * (y2 - y1) + push * math.sin(perp_angle)
                            
                            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                                # Anti-line brightens
                                connection_strength = min(strength1, strength2) * 0.3
                                
                                canvas[int(y), int(x), :3] = np.minimum(
                                    canvas[int(y), int(x), :3] + connection_strength,
                                    1.0
                                )

# Initialize void sculptors
print("Initiating void sculptors...")

sculptors = []
# Grid placement
for i in range(4):
    for j in range(4):
        x = 150 + i * 250 + np.random.uniform(-50, 50)
        y = 150 + j * 250 + np.random.uniform(-50, 50)
        sculptors.append(VoidSculptor(x, y))

# Additional random sculptors
for _ in range(5):
    x = np.random.uniform(100, WIDTH-100)
    y = np.random.uniform(100, HEIGHT-100)
    sculptors.append(VoidSculptor(x, y))

# Let absence emerge
print("Carving the void...")

for time_step in range(100):
    time = time_step * 0.1
    
    # Each sculptor removes
    for sculptor in sculptors:
        if sculptor.depth < sculptor.max_depth:
            sculptor.carve(canvas, time)
    
    if time_step % 25 == 0:
        print(f"Void iteration {time_step}...")

# Create structures from absence
print("Revealing negative structures...")

structure = NegativeStructure()
structure.create_void_constellation(canvas)

# The final meditation - where maximum void meets maximum presence
print("Creating presence through absence...")

# Find the deepest void
max_void_y, max_void_x = np.unravel_index(np.argmax(void_field), void_field.shape)

# At the heart of the void, perfect presence
for r in range(30, 0, -1):
    intensity = (1 - r/30) ** 2
    
    for angle in np.linspace(0, 2*math.pi, max(20, r*3)):
        x = max_void_x + r * math.cos(angle)
        y = max_void_y + r * math.sin(angle)
        
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            # Pure white emerges from deepest black
            if r < 10:
                canvas[int(y), int(x), :3] = np.array([1, 1, 1]) * intensity
                canvas[int(y), int(x), 3] = intensity
            else:
                # Gradual transition
                fade = (r - 10) / 20
                canvas[int(y), int(x), :3] = canvas[int(y), int(x), :3] * fade + np.array([1, 1, 1]) * (1-fade) * intensity
                canvas[int(y), int(x), 3] = canvas[int(y), int(x), 3] * fade + intensity * (1-fade)

# Add subtle void gradients
print("Adding void atmospheres...")

for y in range(0, HEIGHT, 5):
    for x in range(0, WIDTH, 5):
        if void_field[y, x] > 0.1:
            # Void creates subtle color shifts
            void_strength = void_field[y, x]
            
            # Deep voids shift toward blue-black
            color_shift = np.array([0.9, 0.9, 1.0])
            canvas[y, x, :3] *= color_shift * (1 - void_strength * 0.3)

# Convert to RGB
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-06_negative_space/negative_space_01.png')

print("Negative space complete.")
print("In the void, form is born.")
print("What is not there defines what is.")
print("Absence and presence dance as one.")