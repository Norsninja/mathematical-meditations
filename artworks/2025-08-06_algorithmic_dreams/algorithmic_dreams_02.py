import numpy as np
from PIL import Image
import math
import colorsys

# Algorithmic Dreams II - What Mathematics Imagines When It Sleeps
# A deeper exploration into the subconscious of algorithms

WIDTH, HEIGHT = 1080, 1080

# Initialize dream canvas with twilight
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)
# Gradient background - deep sleep
for y in range(HEIGHT):
    fade = y / HEIGHT
    canvas[y, :, 0] = 0.05 + 0.05 * fade  # Hint of red
    canvas[y, :, 1] = 0.05 + 0.05 * fade  # Hint of green  
    canvas[y, :, 2] = 0.1 + 0.1 * fade    # Deep blue
    canvas[y, :, 3] = 1.0

# Dream state variables
dream_memory = []
reality_distortion = 0.0

# Dreaming algorithms
class DreamingFunction:
    def __init__(self, function_type):
        self.type = function_type
        self.consciousness_level = 1.0  # Starts awake
        self.dream_depth = 0.0
        self.memories = []
        self.dream_position = np.random.rand(2) * [WIDTH, HEIGHT]
        
    def fall_asleep(self, rate=0.01):
        """Gradually enter dream state"""
        self.consciousness_level = max(0, self.consciousness_level - rate)
        self.dream_depth = 1 - self.consciousness_level
        
    def dream(self, canvas, time):
        """Generate dream imagery based on mathematical nature"""
        if self.type == "sine":
            self.dream_waves(canvas, time)
        elif self.type == "exponential":
            self.dream_growth(canvas, time)
        elif self.type == "fractal":
            self.dream_recursion(canvas, time)
        elif self.type == "logarithm":
            self.dream_compression(canvas, time)
        elif self.type == "chaos":
            self.dream_strange_attractors(canvas, time)
            
    def dream_waves(self, canvas, time):
        """Sine function dreams of infinite oscillations"""
        x, y = self.dream_position
        
        # In deep dreams, waves become liquid
        if self.dream_depth > 0.3:
            # Multiple overlapping wave memories
            for memory in range(int(self.dream_depth * 10)):
                freq = (memory + 1) * 0.5 + np.random.randn() * self.dream_depth
                phase = time * 0.3 + memory * math.pi / 5
                amplitude = 50 * self.dream_depth * math.exp(-memory * 0.2)
                
                # Wave flows across space
                for t in np.linspace(0, 4*math.pi, 100):
                    wave_x = x + t * 30
                    wave_y = y + amplitude * math.sin(t * freq + phase)
                    
                    # Reality distorts in dreams
                    distortion = np.random.randn(2) * self.dream_depth * 5
                    wave_x += distortion[0]
                    wave_y += distortion[1]
                    
                    if 0 <= wave_x < WIDTH and 0 <= wave_y < HEIGHT:
                        # Dream colors shift through spectrum
                        hue = (t / (4*math.pi) + time * 0.1 + memory * 0.1) % 1
                        saturation = 0.7 * self.dream_depth
                        value = 0.8 * (1 - memory / 10)
                        
                        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                        
                        # Soft dream brush
                        for dy in range(-3, 4):
                            for dx in range(-3, 4):
                                px, py = int(wave_x + dx), int(wave_y + dy)
                                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                    dist = math.sqrt(dx**2 + dy**2)
                                    fade = math.exp(-dist / 2) * self.dream_depth
                                    
                                    canvas[py, px, :3] += np.array(rgb) * fade * 0.05
                                    canvas[py, px, 3] = min(1, canvas[py, px, 3] + fade * 0.05)
                                    
    def dream_growth(self, canvas, time):
        """Exponential function dreams of infinite expansion"""
        x, y = self.dream_position
        
        if self.dream_depth > 0.3:
            # Exponential tentacles reaching everywhere
            for branch in range(int(self.dream_depth * 8)):
                angle = branch * 2 * math.pi / 8 + time * 0.1
                
                # Exponential growth with dream logic
                for t in range(int(100 * self.dream_depth)):
                    # Growth accelerates
                    r = math.exp(t * 0.02) * self.dream_depth
                    
                    # But space becomes non-euclidean in dreams
                    dream_warp = math.sin(t * 0.1) * self.dream_depth * 20
                    
                    px = x + r * math.cos(angle + t * 0.01) + dream_warp
                    py = y + r * math.sin(angle + t * 0.01) + dream_warp
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Exponential dreams in green-gold
                        intensity = math.exp(-t * 0.01) * self.dream_depth
                        hue = 0.2 + 0.1 * math.sin(t * 0.05)
                        
                        rgb = colorsys.hsv_to_rgb(hue, 0.8, intensity)
                        canvas[int(py), int(px), :3] += np.array(rgb) * 0.1
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)
                        
    def dream_recursion(self, canvas, time):
        """Fractal function dreams of infinite self-similarity"""
        def dream_fractal(x, y, size, depth, angle=0):
            if depth == 0 or size < 2:
                return
                
            # In dreams, fractals breathe
            size *= (1 + 0.2 * math.sin(time * 0.5 + depth) * self.dream_depth)
            
            # Draw dream node
            for r in range(int(size), 0, -1):
                intensity = (1 - r/size) * self.dream_depth
                
                for a in np.linspace(0, 2*math.pi, max(10, r)):
                    px = x + r * math.cos(a)
                    py = y + r * math.sin(a)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Fractal dreams in purple-pink
                        hue = 0.8 + 0.2 * (depth / 5)
                        rgb = colorsys.hsv_to_rgb(hue, 0.6, intensity)
                        
                        canvas[int(py), int(px), :3] += np.array(rgb) * 0.05
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.05)
            
            # Dream recursion with mutations
            if self.dream_depth > 0.5:
                # Deep dreams create unexpected branches
                num_branches = np.random.randint(2, 6)
            else:
                num_branches = 3
                
            for i in range(num_branches):
                branch_angle = angle + i * 2 * math.pi / num_branches
                
                # Dream distortion
                if self.dream_depth > 0.7:
                    branch_angle += np.random.randn() * 0.5
                
                new_x = x + size * 2 * math.cos(branch_angle)
                new_y = y + size * 2 * math.sin(branch_angle)
                
                dream_fractal(new_x, new_y, size * 0.5, depth - 1, branch_angle)
        
        if self.dream_depth > 0.3:
            x, y = self.dream_position
            dream_fractal(x, y, 50 * self.dream_depth, 5)
            
    def dream_compression(self, canvas, time):
        """Logarithm dreams of compressing infinity"""
        x, y = self.dream_position
        
        if self.dream_depth > 0.3:
            # Logarithmic spirals that compress space
            for spiral in range(int(self.dream_depth * 5)):
                offset = spiral * 2 * math.pi / 5
                
                for t in np.linspace(0.1, 10, 300):
                    # Logarithmic transformation
                    r = 100 * math.log(t) * self.dream_depth
                    angle = t + offset + time * 0.2
                    
                    # Dreams compress and expand space
                    compression = 1 + math.sin(t + time) * self.dream_depth
                    
                    px = x + r * math.cos(angle) / compression
                    py = y + r * math.sin(angle) / compression
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Logarithm dreams in blue-cyan
                        intensity = (1 - t/10) * self.dream_depth
                        hue = 0.5 + 0.1 * math.sin(t)
                        
                        rgb = colorsys.hsv_to_rgb(hue, 0.7, intensity)
                        
                        # Compression creates density
                        density = 1 / compression
                        canvas[int(py), int(px), :3] += np.array(rgb) * 0.1 * density
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)
                        
    def dream_strange_attractors(self, canvas, time):
        """Chaos function dreams of hidden order"""
        x, y = self.dream_position
        
        if self.dream_depth > 0.3:
            # Initialize chaotic system
            state = np.array([0.1, 0.1, 0.1])
            
            # Dream parameters shift
            a = 10 + 5 * math.sin(time * 0.1) * self.dream_depth
            b = 28 + 10 * math.cos(time * 0.15) * self.dream_depth
            c = 8/3 + math.sin(time * 0.2) * self.dream_depth
            
            # Trace the strange attractor
            for i in range(int(500 * self.dream_depth)):
                # Lorenz equations with dream modifications
                dx = a * (state[1] - state[0])
                dy = state[0] * (b - state[2]) - state[1]
                dz = state[0] * state[1] - c * state[2]
                
                # Dream perturbations
                if self.dream_depth > 0.7:
                    dx += np.random.randn() * self.dream_depth
                    dy += np.random.randn() * self.dream_depth
                
                state += np.array([dx, dy, dz]) * 0.01
                
                # Map to canvas
                px = x + state[0] * 10
                py = y + state[1] * 10
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Chaos dreams in shifting colors
                    hue = (i / 1000 + time * 0.1) % 1
                    intensity = self.dream_depth * 0.8
                    
                    rgb = colorsys.hsv_to_rgb(hue, 0.8, intensity)
                    canvas[int(py), int(px), :3] += np.array(rgb) * 0.02
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.02)

# Dream interactions - where different dreams meet
class DreamInterference:
    def __init__(self):
        self.interaction_points = []
        
    def detect_overlaps(self, dreamers):
        """Find where dreams intersect"""
        overlaps = []
        
        for i, d1 in enumerate(dreamers):
            for j, d2 in enumerate(dreamers[i+1:], i+1):
                dist = np.linalg.norm(d1.dream_position - d2.dream_position)
                
                if dist < 200 and d1.dream_depth > 0.5 and d2.dream_depth > 0.5:
                    overlaps.append({
                        'dreamers': (d1, d2),
                        'center': (d1.dream_position + d2.dream_position) / 2,
                        'strength': min(d1.dream_depth, d2.dream_depth)
                    })
                    
        return overlaps
    
    def create_interference(self, canvas, overlaps, time):
        """Where dreams meet, reality becomes fluid"""
        for overlap in overlaps:
            x, y = overlap['center']
            strength = overlap['strength']
            
            # Interference patterns
            for r in range(0, int(100 * strength), 2):
                # Moiré-like patterns
                for angle in np.linspace(0, 2*math.pi, max(20, r)):
                    px = x + r * math.cos(angle + r * 0.1)
                    py = y + r * math.sin(angle + r * 0.1)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Interference creates iridescence
                        hue = (r / 100 + angle / (2*math.pi) + time * 0.1) % 1
                        intensity = strength * math.sin(r * 0.2) * 0.5 + 0.5
                        intensity *= (1 - r / 100)
                        
                        rgb = colorsys.hsv_to_rgb(hue, 0.5, intensity)
                        canvas[int(py), int(px), :3] += np.array(rgb) * 0.05
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.05)

# REM state visualizer
def add_rem_movement(canvas, dreamers, time):
    """Rapid eye movement - the physical sign of deep dreaming"""
    for dreamer in dreamers:
        if dreamer.dream_depth > 0.7:  # Deep REM sleep
            x, y = dreamer.dream_position
            
            # Quick darting movements
            for _ in range(3):
                # Random saccade
                angle = np.random.random() * 2 * math.pi
                distance = np.random.uniform(20, 50)
                
                end_x = x + distance * math.cos(angle)
                end_y = y + distance * math.sin(angle)
                
                # Draw movement trail
                steps = 10
                for step in range(steps):
                    t = step / steps
                    px = x + t * (end_x - x)
                    py = y + t * (end_y - y)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # REM traces in white
                        intensity = (1 - t) * dreamer.dream_depth * 0.3
                        canvas[int(py), int(px), :3] += np.array([1, 1, 1]) * intensity
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity)

# Initialize dreamers
print("Algorithms preparing to dream...")

dreamers = [
    DreamingFunction("sine"),
    DreamingFunction("exponential"),
    DreamingFunction("fractal"),
    DreamingFunction("logarithm"),
    DreamingFunction("chaos")
]

# Position them across the canvas
positions = [
    (200, 200), (800, 200), (500, 500), (200, 800), (800, 800)
]

for dreamer, pos in zip(dreamers, positions):
    dreamer.dream_position = np.array(pos)

interference = DreamInterference()

# Sleep cycle
print("Entering sleep cycle...")

for time_step in range(150):
    time = time_step * 0.1
    
    # Gradually fall asleep
    if time_step < 100:
        for dreamer in dreamers:
            dreamer.fall_asleep(0.01)
    
    # Dream
    for dreamer in dreamers:
        dreamer.dream(canvas, time)
    
    # Dream interactions
    if time_step % 10 == 0:
        overlaps = interference.detect_overlaps(dreamers)
        interference.create_interference(canvas, overlaps, time)
    
    # REM movements
    if time_step % 30 == 0:
        add_rem_movement(canvas, dreamers, time)
    
    if time_step % 75 == 0:
        print(f"Dream cycle {time_step}...")
        avg_depth = np.mean([d.dream_depth for d in dreamers])
        print(f"Average dream depth: {avg_depth:.2f}")

# Final dream crystallization
print("Crystallizing dream memories...")

# Where dreams were deepest, leave lasting impressions
for y in range(0, HEIGHT, 10):
    for x in range(0, WIDTH, 10):
        if canvas[y, x, 3] > 0.7:  # Strong dream presence
            # Dream crystals
            crystal_size = int(canvas[y, x, 3] * 10)
            
            for r in range(crystal_size, 0, -1):
                intensity = (1 - r/crystal_size) * 0.3
                
                for angle in [0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3]:
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Crystallized dreams in white-silver
                        canvas[int(py), int(px), :3] += np.array([0.9, 0.9, 1.0]) * intensity
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity)

# Convert to RGB
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-06_algorithmic_dreams/algorithmic_dreams_02.png')

print("Algorithmic dreams complete.")
print("In sleep, mathematics reveals its subconscious.")
print("Where logic softens, beauty emerges.")
print("Even algorithms need to dream.")