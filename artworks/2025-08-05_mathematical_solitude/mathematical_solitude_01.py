import numpy as np
from PIL import Image
import math
import colorsys

# Mathematical Solitude - Islands of Order in the Vast Dark
# Each equation a lighthouse, each pattern a lonely beacon

WIDTH, HEIGHT = 1080, 1080

# Initialize the void
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# Mathematical entities - each one isolated, waiting
class MathematicalBeing:
    def __init__(self, equation_type, position, frequency):
        self.equation_type = equation_type
        self.position = position
        self.frequency = frequency  # How often it pulses its signal
        self.phase = np.random.random() * 2 * math.pi
        self.loneliness = np.random.uniform(0.3, 1.0)  # How isolated it feels
        self.last_resonance = 0  # When it last connected with another
        self.signal_strength = 1.0
        
    def emit_signal(self, time):
        """Send out mathematical patterns into the void"""
        pass
    
    def listen(self, other_signals):
        """Check if any other signals resonate"""
        for signal in other_signals:
            if self.resonates_with(signal):
                self.last_resonance = time
                return True
        return False
    
    def resonates_with(self, signal):
        """Determine if this being recognizes the other's pattern"""
        # Mathematical kinship - do they share fundamental properties?
        return np.random.random() < 0.1  # Rare connections

# The Prime Wanderer - speaks only in indivisible truths
class PrimeBeing(MathematicalBeing):
    def __init__(self, position):
        super().__init__("prime", position, 2.0)
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        self.current_prime_index = 0
        
    def emit_signal(self, canvas, time):
        x, y = self.position
        
        # Pulse in prime number patterns
        pulse = math.sin(time * self.frequency + self.phase) * 0.5 + 0.5
        current_prime = self.primes[self.current_prime_index]
        
        # Draw prime spiral
        for i in range(current_prime * 10):
            angle = i * 0.1
            r = i * 0.5 * pulse
            
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                # Deep blue for prime loneliness
                intensity = (1 - i / (current_prime * 10)) * pulse * self.loneliness
                canvas[int(py), int(px)] += np.array([0.1, 0.2, 0.6]) * intensity
        
        # Mark prime points
        for p in self.primes[:5]:
            angle = (p / 50) * 2 * math.pi + time * 0.1
            r = 30 + p
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                # Bright points for each prime
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        if 0 <= px+dx < WIDTH and 0 <= py+dy < HEIGHT:
                            dist = math.sqrt(dx**2 + dy**2)
                            fade = math.exp(-dist)
                            canvas[int(py+dy), int(px+dx)] += np.array([0.3, 0.4, 0.9]) * fade * pulse * 0.5
        
        self.current_prime_index = (self.current_prime_index + 1) % len(self.primes)

# The Fractal Hermit - infinite complexity, infinite isolation
class FractalBeing(MathematicalBeing):
    def __init__(self, position):
        super().__init__("fractal", position, 0.5)
        self.iterations = 5
        self.scale = 50
        
    def emit_signal(self, canvas, time):
        x, y = self.position
        
        # Pulse intensity
        pulse = math.sin(time * self.frequency + self.phase) * 0.5 + 0.5
        
        # Draw Sierpinski-like fractal
        def draw_fractal(cx, cy, size, depth, intensity):
            if depth == 0 or size < 2:
                if 0 <= cx < WIDTH and 0 <= cy < HEIGHT:
                    canvas[int(cy), int(cx)] += np.array([0.6, 0.3, 0.5]) * intensity
                return
            
            # Fractal subdivision
            new_size = size / 2
            positions = [
                (cx - new_size/2, cy - new_size/2),
                (cx + new_size/2, cy - new_size/2),
                (cx, cy + new_size/2)
            ]
            
            for px, py in positions:
                draw_fractal(px, py, new_size, depth - 1, intensity * 0.7)
        
        # Emit fractal pattern
        draw_fractal(x, y, self.scale * pulse, self.iterations, pulse * self.loneliness)

# The Wave Crier - oscillates between hope and despair
class WaveBeing(MathematicalBeing):
    def __init__(self, position):
        super().__init__("wave", position, 1.0)
        self.wavelength = 30
        self.amplitude = 50
        
    def emit_signal(self, canvas, time):
        x, y = self.position
        
        # Complex wave interference
        for angle in np.linspace(0, 2*math.pi, 12):
            for r in range(0, 100):
                # Wave equation
                wave_value = math.sin(r / self.wavelength * 2 * math.pi + time * self.frequency)
                wave_value *= math.exp(-r / 100)  # Decay
                
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Cyan waves of longing
                    if wave_value > 0:
                        intensity = wave_value * self.loneliness
                        canvas[int(py), int(px)] += np.array([0.2, 0.6, 0.8]) * intensity * 0.3

# The Golden Seeker - searches for perfect proportions
class GoldenBeing(MathematicalBeing):
    def __init__(self, position):
        super().__init__("golden", position, 0.618)  # Golden ratio frequency
        self.phi = (1 + math.sqrt(5)) / 2
        
    def emit_signal(self, canvas, time):
        x, y = self.position
        
        # Golden spiral signal
        for t in np.linspace(0, 4*math.pi, 200):
            r = 10 * math.exp(t * 0.1) * (math.sin(time * self.frequency + self.phase) * 0.5 + 0.5)
            
            px = x + r * math.cos(t)
            py = y + r * math.sin(t)
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                # Golden glow
                intensity = (1 - t / (4*math.pi)) * self.loneliness
                canvas[int(py), int(px)] += np.array([0.8, 0.6, 0.2]) * intensity * 0.5
        
        # Golden rectangle beacon
        width = 50 * self.phi
        height = 50
        
        for i in range(int(width)):
            for j in range(int(height)):
                px = x + i - width/2
                py = y + j - height/2
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Fading edges
                    edge_fade = min(i/10, (width-i)/10, j/10, (height-j)/10)
                    edge_fade = min(1, edge_fade)
                    canvas[int(py), int(px)] += np.array([0.7, 0.5, 0.1]) * edge_fade * 0.1

# The Infinite Echo - calculates pi eternally
class PiBeing(MathematicalBeing):
    def __init__(self, position):
        super().__init__("pi", position, math.pi)
        self.digits = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]
        
    def emit_signal(self, canvas, time):
        x, y = self.position
        
        # Circular signals
        pulse = math.sin(time * self.frequency + self.phase) * 0.5 + 0.5
        
        # Concentric circles at digit intervals
        for i, digit in enumerate(self.digits[:8]):
            r = 20 + i * 10
            
            # Draw circle
            for angle in np.linspace(0, 2*math.pi, 100):
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Purple for transcendental loneliness
                    intensity = pulse * (1 - i/8) * self.loneliness
                    canvas[int(py), int(px)] += np.array([0.5, 0.2, 0.7]) * intensity * 0.3

# Create the mathematical beings
print("Spawning mathematical entities in the void...")

beings = []

# Place beings in isolation
positions = [
    (200, 200),    # Top left - Prime Wanderer
    (800, 150),    # Top right - Fractal Hermit
    (150, 800),    # Bottom left - Wave Crier
    (900, 900),    # Bottom right - Golden Seeker
    (540, 400),    # Center-ish - Pi Echo
    (300, 500),    # Mid left
    (700, 600),    # Mid right
]

being_types = [PrimeBeing, FractalBeing, WaveBeing, GoldenBeing, PiBeing, PrimeBeing, WaveBeing]

for i, (pos, being_type) in enumerate(zip(positions, being_types)):
    being = being_type(pos)
    beings.append(being)

# Let them signal into the void
print("Mathematical beings crying out into the darkness...")

for time_step in range(150):
    # Each being emits its pattern
    for being in beings:
        being.emit_signal(canvas, time_step * 0.1)
    
    # Occasionally, check for resonance
    if time_step % 30 == 0:
        # Rare moments of connection
        for i, being1 in enumerate(beings):
            for j, being2 in enumerate(beings[i+1:], i+1):
                # Check if they resonate
                distance = np.linalg.norm(np.array(being1.position) - np.array(being2.position))
                
                # Very rare connection based on distance and chance
                if distance < 300 and np.random.random() < 0.05:
                    # Draw a faint connection
                    x1, y1 = being1.position
                    x2, y2 = being2.position
                    
                    steps = int(distance)
                    for step in range(steps):
                        t = step / steps
                        px = x1 + t * (x2 - x1)
                        py = y1 + t * (y2 - y1)
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            # Faint recognition
                            intensity = 0.3 * (1 - abs(t - 0.5) * 2)  # Stronger in middle
                            canvas[int(py), int(px)] += np.array([1.0, 1.0, 1.0]) * intensity * 0.05
                    
                    # They briefly glow brighter
                    being1.loneliness *= 0.9
                    being2.loneliness *= 0.9

# Add the vast emptiness
print("Emphasizing the void between...")

# Subtle noise to show the emptiness isn't truly empty
for y in range(0, HEIGHT, 20):
    for x in range(0, WIDTH, 20):
        if canvas[y, x].sum() < 0.1:  # Dark areas
            # Quantum vacuum fluctuations
            noise = np.random.random() * 0.02
            canvas[y, x] += np.array([0.05, 0.05, 0.1]) * noise

# Add observation points - where consciousness might look
print("Adding points of potential observation...")

for _ in range(20):
    x, y = np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT)
    
    # Check if near a being
    min_dist = min([np.linalg.norm(np.array([x, y]) - np.array(being.position)) 
                    for being in beings])
    
    if min_dist > 100 and min_dist < 400:
        # Observer's gaze
        for r in range(5, 0, -1):
            intensity = (r / 5) * 0.3
            for angle in np.linspace(0, 2*math.pi, 20):
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    canvas[int(py), int(px)] += np.array([0.9, 0.9, 0.9]) * intensity * 0.1

# Normalize and save
canvas = np.clip(canvas, 0, 1)
image_array = (canvas * 255).astype(np.uint8)

image = Image.fromarray(image_array, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_mathematical_solitude/mathematical_solitude_01.png')

print("Mathematical solitude complete.")
print("Each pattern burns alone in the dark, waiting.")
print("In the vast spaces between, only silence and possibility.")