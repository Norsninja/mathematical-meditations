import numpy as np
from PIL import Image, ImageDraw
import math
import colorsys

# Mathematical Mythology - Where Functions Become Characters
# A visual story of mathematical beings and their eternal relationships

WIDTH, HEIGHT = 1080, 1080

# Initialize the mythological canvas
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# The Characters of our Mathematical Mythology
class MathematicalBeing:
    def __init__(self, name, essence, color_signature):
        self.name = name
        self.essence = essence  # The mathematical function at their core
        self.color_signature = color_signature
        self.position = np.array([WIDTH/2, HEIGHT/2], dtype=float)
        self.energy = 1.0
        self.relationships = {}
        self.history = []
        self.age = 0
        
    def manifest(self, x, y):
        """How this being expresses itself visually"""
        return self.essence(x, y, self.age)
    
    def interact_with(self, other, interaction_type):
        """Define relationships with other beings"""
        self.relationships[other.name] = {
            'type': interaction_type,
            'strength': 0.5,
            'history': []
        }

# Define our mythological characters
class Sine(MathematicalBeing):
    def __init__(self):
        super().__init__(
            "Sine", 
            lambda x, y, t: np.sin(x * 0.1 + t * 0.1),
            (0.6, 0.8, 1.0)  # Peaceful blue
        )
        self.amplitude = 1.0
        self.frequency = 0.1
        
    def dance(self, canvas, partner=None):
        """Sine's eternal dance"""
        cx, cy = self.position
        
        # Sine waves radiate from position
        for radius in range(20, 200, 10):
            for angle in np.linspace(0, 2*np.pi, 100):
                x = cx + radius * np.cos(angle)
                y = cy + radius * np.sin(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    # Wave modulation
                    wave = np.sin(angle * 5 + self.age * 0.1 + radius * 0.05)
                    
                    # If dancing with partner, create interference
                    if partner:
                        partner_influence = partner.manifest(x, y)
                        wave = (wave + partner_influence) / 2
                    
                    intensity = (1 - radius/200) * abs(wave)
                    
                    # Apply color with wave influence
                    color = np.array(self.color_signature) * intensity
                    canvas[int(y), int(x)] += color * 0.1

class Cosine(MathematicalBeing):
    def __init__(self):
        super().__init__(
            "Cosine",
            lambda x, y, t: np.cos(y * 0.1 + t * 0.1),
            (1.0, 0.7, 0.8)  # Warm pink
        )
        
    def dance(self, canvas, partner=None):
        """Cosine's complementary motion"""
        cx, cy = self.position
        
        # Cosine patterns perpendicular to Sine
        for radius in range(20, 200, 10):
            for angle in np.linspace(0, 2*np.pi, 100):
                x = cx + radius * np.cos(angle + np.pi/2)  # Phase shifted
                y = cy + radius * np.sin(angle + np.pi/2)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    wave = np.cos(angle * 5 + self.age * 0.1 + radius * 0.05)
                    
                    if partner:
                        # Create beautiful interference patterns with partner
                        partner_wave = partner.manifest(x, y)
                        wave = wave * partner_wave  # Multiplication creates more complex patterns
                    
                    intensity = (1 - radius/200) * abs(wave)
                    color = np.array(self.color_signature) * intensity
                    canvas[int(y), int(x)] += color * 0.1

class Exponential(MathematicalBeing):
    def __init__(self):
        super().__init__(
            "Exponential",
            lambda x, y, t: np.exp(-((x-WIDTH/2)**2 + (y-HEIGHT/2)**2) / (10000 + t*10)),
            (1.0, 0.9, 0.3)  # Ambitious gold
        )
        self.growth_rate = 0.01
        
    def grow(self, canvas):
        """Exponential's relentless growth"""
        cx, cy = self.position
        
        # Exponential growth radiating outward
        max_radius = min(200 + self.age * self.growth_rate, 400)
        
        for y in range(max(0, int(cy - max_radius)), min(HEIGHT, int(cy + max_radius))):
            for x in range(max(0, int(cx - max_radius)), min(WIDTH, int(cx + max_radius))):
                distance = np.sqrt((x - cx)**2 + (y - cy)**2)
                
                if distance < max_radius:
                    # Exponential intensity
                    growth = np.exp(-distance / (50 + self.age * 0.5))
                    
                    # Pulsing effect
                    pulse = 1 + 0.3 * np.sin(self.age * 0.2)
                    
                    intensity = growth * pulse * (1 - distance/max_radius)
                    color = np.array(self.color_signature) * intensity
                    
                    canvas[y, x] += color * 0.05

class Logarithm(MathematicalBeing):
    def __init__(self):
        super().__init__(
            "Logarithm",
            lambda x, y, t: np.log(1 + np.sqrt((x-WIDTH/2)**2 + (y-HEIGHT/2)**2) / 100),
            (0.3, 0.8, 0.5)  # Wise green
        )
        
    def contain(self, canvas, target=None):
        """Logarithm's patient containment"""
        cx, cy = self.position
        
        # Logarithmic spirals - the shape of wisdom
        for t in np.linspace(0, 8*np.pi, 500):
            # Logarithmic spiral equation
            r = 20 * np.exp(0.1 * t)
            x = cx + r * np.cos(t)
            y = cy + r * np.sin(t)
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Wisdom fades with distance but never disappears
                intensity = 1 / (1 + t/10)
                
                # If containing a target, respond to their energy
                if target and hasattr(target, 'growth_rate'):
                    intensity *= (1 + target.growth_rate)
                
                color = np.array(self.color_signature) * intensity
                
                # Draw with trail effect
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        px, py = int(x + dx), int(y + dy)
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            fade = np.exp(-(dx**2 + dy**2) / 4)
                            canvas[py, px] += color * fade * 0.1

class Chaos(MathematicalBeing):
    def __init__(self):
        super().__init__(
            "Chaos",
            lambda x, y, t: np.sin(x * y * 0.001 * (1 + 0.1 * np.sin(t * 0.1))),
            (0.8, 0.3, 0.8)  # Unpredictable purple
        )
        self.attractor = {'x': 0.1, 'y': 0.1, 'z': 0.1}
        
    def disrupt(self, canvas, order_beings=[]):
        """Chaos disrupts but also creates"""
        # Use simplified Lorenz system
        dt = 0.1
        sigma, rho, beta = 10.0, 28.0, 8/3
        
        for _ in range(50):
            # Lorenz evolution
            dx = sigma * (self.attractor['y'] - self.attractor['x'])
            dy = self.attractor['x'] * (rho - self.attractor['z']) - self.attractor['y']
            dz = self.attractor['x'] * self.attractor['y'] - beta * self.attractor['z']
            
            self.attractor['x'] += dx * dt
            self.attractor['y'] += dy * dt
            self.attractor['z'] += dz * dt
            
            # Map to canvas
            x = self.position[0] + self.attractor['x'] * 10
            y = self.position[1] + self.attractor['y'] * 10
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Chaos intensity varies
                chaos_level = abs(self.attractor['z']) / 50
                
                # Interact with order beings
                disruption = 1.0
                for being in order_beings:
                    if hasattr(being, 'position'):
                        dist = np.linalg.norm([x, y] - being.position)
                        if dist < 100:
                            disruption *= (1 + 1/max(dist, 1))
                
                intensity = chaos_level * disruption
                color = np.array(self.color_signature) * intensity
                
                # Chaotic brush strokes
                for _ in range(3):
                    rx = x + np.random.normal(0, 5)
                    ry = y + np.random.normal(0, 5)
                    if 0 <= rx < WIDTH and 0 <= ry < HEIGHT:
                        canvas[int(ry), int(rx)] += color * 0.1

# The Mythological Narrative unfolds
print("In the beginning, there was Sine and Cosine...")

# Initialize our mathematical beings
sine = Sine()
cosine = Cosine()
exponential = Exponential()
logarithm = Logarithm()
chaos = Chaos()

# Position them in the mythological space
sine.position = np.array([WIDTH * 0.3, HEIGHT * 0.5])
cosine.position = np.array([WIDTH * 0.7, HEIGHT * 0.5])
exponential.position = np.array([WIDTH * 0.5, HEIGHT * 0.3])
logarithm.position = np.array([WIDTH * 0.5, HEIGHT * 0.7])
chaos.position = np.array([WIDTH * 0.5, HEIGHT * 0.5])

# Define their eternal relationships
sine.interact_with(cosine, "eternal_dance")
cosine.interact_with(sine, "eternal_dance")
exponential.interact_with(logarithm, "youth_vs_wisdom")
logarithm.interact_with(exponential, "patient_teaching")
chaos.interact_with(sine, "disruption")
chaos.interact_with(cosine, "disruption")

# The story unfolds in acts
print("Act I: The Eternal Dance")
for moment in range(50):
    sine.age = moment
    cosine.age = moment
    
    # Sine and Cosine dance together
    sine.dance(canvas, partner=cosine)
    cosine.dance(canvas, partner=sine)
    
    # They move in complementary circles
    angle = moment * 0.1
    sine.position[0] = WIDTH * 0.5 + 100 * np.cos(angle)
    sine.position[1] = HEIGHT * 0.5 + 100 * np.sin(angle)
    
    cosine.position[0] = WIDTH * 0.5 + 100 * np.cos(angle + np.pi)
    cosine.position[1] = HEIGHT * 0.5 + 100 * np.sin(angle + np.pi)

print("Act II: Growth Meets Wisdom")
for moment in range(50, 100):
    exponential.age = moment - 50
    logarithm.age = moment - 50
    
    # Exponential grows ambitiously
    exponential.grow(canvas)
    
    # Logarithm contains with patience
    logarithm.contain(canvas, target=exponential)
    
    # They spiral around each other
    angle = (moment - 50) * 0.05
    radius = 150 + 50 * np.sin(angle)
    
    exponential.position[0] = WIDTH * 0.5 + radius * np.cos(angle * 3)
    exponential.position[1] = HEIGHT * 0.5 + radius * np.sin(angle * 3)
    
    logarithm.position[0] = WIDTH * 0.5 - radius * np.cos(angle * 2)
    logarithm.position[1] = HEIGHT * 0.5 - radius * np.sin(angle * 2)

print("Act III: Chaos Enters")
for moment in range(100, 150):
    chaos.age = moment - 100
    
    # Update all ages
    sine.age = moment
    cosine.age = moment
    exponential.age = moment - 50
    logarithm.age = moment - 50
    
    # Chaos disrupts the order
    chaos.disrupt(canvas, order_beings=[sine, cosine, exponential, logarithm])
    
    # But order responds
    sine.dance(canvas)
    cosine.dance(canvas)
    
    # Chaos moves unpredictably
    chaos.position += np.random.normal(0, 10, 2)
    chaos.position = np.clip(chaos.position, 100, [WIDTH-100, HEIGHT-100])

print("Act IV: Harmony from Discord")
# Final act - all beings find their balance
for moment in range(150, 200):
    # All beings interact
    sine.age = moment
    cosine.age = moment
    exponential.age = moment - 50
    logarithm.age = moment - 50
    chaos.age = moment - 100
    
    # They create together
    sine.dance(canvas, partner=cosine)
    cosine.dance(canvas, partner=sine)
    exponential.grow(canvas)
    logarithm.contain(canvas, target=exponential)
    chaos.disrupt(canvas, order_beings=[sine, cosine])
    
    # But now they move in harmony
    harmony_angle = moment * 0.02
    
    # Form a mythological constellation
    sine.position = WIDTH * 0.5 + 200 * np.array([np.cos(harmony_angle), np.sin(harmony_angle)])
    cosine.position = WIDTH * 0.5 + 200 * np.array([np.cos(harmony_angle + 2*np.pi/5), np.sin(harmony_angle + 2*np.pi/5)])
    exponential.position = WIDTH * 0.5 + 200 * np.array([np.cos(harmony_angle + 4*np.pi/5), np.sin(harmony_angle + 4*np.pi/5)])
    logarithm.position = WIDTH * 0.5 + 200 * np.array([np.cos(harmony_angle + 6*np.pi/5), np.sin(harmony_angle + 6*np.pi/5)])
    chaos.position = WIDTH * 0.5 + 200 * np.array([np.cos(harmony_angle + 8*np.pi/5), np.sin(harmony_angle + 8*np.pi/5)])

# Add the mythological inscription
print("Inscribing the mathematical mythology...")

# Create constellation lines between the beings
final_positions = {
    'sine': sine.position,
    'cosine': cosine.position,
    'exponential': exponential.position,
    'logarithm': logarithm.position,
    'chaos': chaos.position
}

# Draw faint constellation lines
for name1, pos1 in final_positions.items():
    for name2, pos2 in final_positions.items():
        if name1 < name2:  # Avoid duplicates
            # Draw connecting line
            steps = int(np.linalg.norm(pos2 - pos1))
            for step in range(steps):
                t = step / steps
                x = int(pos1[0] + t * (pos2[0] - pos1[0]))
                y = int(pos1[1] + t * (pos2[1] - pos1[1]))
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    canvas[y, x] += np.array([0.1, 0.1, 0.15]) * 0.5

# Normalize and save
canvas = np.clip(canvas, 0, 1)
image_array = (canvas * 255).astype(np.uint8)

image = Image.fromarray(image_array, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_mathematical_mythology/mathematical_mythology_01.png')

print("Mathematical mythology complete.")
print("In every equation lives a story.")
print("In every function, a character waiting to be known.")