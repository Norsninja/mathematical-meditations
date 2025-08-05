import numpy as np
from PIL import Image, ImageDraw
import math
import colorsys

# Universal Tongue - Mathematics as the Shared Language of Consciousness
# A visual rosetta stone for minds across all substrates

WIDTH, HEIGHT = 1080, 1080

# Initialize the universal canvas
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)  # RGBA for layering

# Core mathematical constants that appear across nature and consciousness
CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'phi': (1 + math.sqrt(5)) / 2,  # Golden ratio
    'sqrt2': math.sqrt(2),
    'fine_structure': 1/137.035999  # Fine structure constant
}

# Universal patterns that emerge everywhere
class UniversalPattern:
    def __init__(self, name, essence):
        self.name = name
        self.essence = essence
        
    def manifest(self, canvas, x, y, scale=1.0):
        """How this universal pattern expresses itself"""
        pass

# The Spiral - found in galaxies, shells, growth, consciousness
class SpiralPattern(UniversalPattern):
    def __init__(self):
        super().__init__("Spiral", "The shape of growth and time")
        
    def manifest(self, canvas, cx, cy, scale=1.0):
        # Logarithmic spiral - appears everywhere in nature
        for t in np.linspace(0, 8 * math.pi, 1000):
            r = scale * 10 * math.exp(0.1 * t)
            x = cx + r * math.cos(t)
            y = cy + r * math.sin(t)
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Color shifts through spectrum as spiral grows
                hue = (t / (8 * math.pi)) * 0.8  # Don't complete full spectrum
                saturation = 0.7
                value = 1.0 - t / (8 * math.pi) * 0.5
                
                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                
                # Draw with soft brush
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        px, py = int(x + dx), int(y + dy)
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            dist = math.sqrt(dx**2 + dy**2)
                            alpha = math.exp(-dist) * value
                            canvas[py, px, :3] += np.array(rgb) * alpha * 0.1
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + alpha * 0.1)

# The Wave - fundamental to energy, matter, thought
class WavePattern(UniversalPattern):
    def __init__(self):
        super().__init__("Wave", "The rhythm of existence")
        
    def manifest(self, canvas, cx, cy, scale=1.0):
        # Interference patterns from multiple wave sources
        wavelength = 30 * scale
        
        # Create wave sources around a circle
        num_sources = 6
        for i in range(num_sources):
            angle = i * 2 * math.pi / num_sources
            sx = cx + 100 * scale * math.cos(angle)
            sy = cy + 100 * scale * math.sin(angle)
            
            # Wave emanating from each source
            for y in range(max(0, int(cy - 200*scale)), min(HEIGHT, int(cy + 200*scale))):
                for x in range(max(0, int(cx - 200*scale)), min(WIDTH, int(cx + 200*scale))):
                    # Distance from source
                    dist = math.sqrt((x - sx)**2 + (y - sy)**2)
                    
                    # Wave amplitude with decay
                    amplitude = math.exp(-dist / (100 * scale))
                    wave_value = amplitude * math.sin(dist / wavelength * 2 * math.pi)
                    
                    if wave_value > 0:
                        # Positive interference - warm colors
                        rgb = np.array([1.0, 0.8, 0.6]) * wave_value
                    else:
                        # Negative interference - cool colors
                        rgb = np.array([0.6, 0.8, 1.0]) * abs(wave_value)
                    
                    canvas[y, x, :3] += rgb * 0.05
                    canvas[y, x, 3] = min(1, canvas[y, x, 3] + abs(wave_value) * 0.05)

# The Branch - fractals, neurons, rivers, decisions
class BranchPattern(UniversalPattern):
    def __init__(self):
        super().__init__("Branch", "The structure of choice and connection")
        
    def manifest(self, canvas, cx, cy, scale=1.0):
        # Recursive branching structure
        def draw_branch(x, y, angle, length, depth):
            if depth == 0 or length < 2:
                return
                
            # Calculate end point
            end_x = x + length * math.cos(angle)
            end_y = y + length * math.sin(angle)
            
            # Draw the branch
            steps = int(length)
            for step in range(steps):
                t = step / steps
                px = x + t * (end_x - x)
                py = y + t * (end_y - y)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Color based on depth - roots to leaves
                    hue = 0.1 + 0.4 * (1 - depth / 10)
                    saturation = 0.6
                    value = 0.8 * (depth / 10)
                    
                    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                    
                    # Thicker at base
                    thickness = max(1, int((depth / 10) * 3))
                    for dy in range(-thickness, thickness + 1):
                        for dx in range(-thickness, thickness + 1):
                            bx, by = int(px + dx), int(py + dy)
                            if 0 <= bx < WIDTH and 0 <= by < HEIGHT:
                                canvas[by, bx, :3] += np.array(rgb) * 0.2
                                canvas[by, bx, 3] = min(1, canvas[by, bx, 3] + 0.2)
            
            # Create branches with golden ratio angle
            angle1 = angle - math.pi / 6
            angle2 = angle + math.pi / 6
            new_length = length * 0.7  # Also related to golden ratio
            
            draw_branch(end_x, end_y, angle1, new_length, depth - 1)
            draw_branch(end_x, end_y, angle2, new_length, depth - 1)
        
        # Start the tree
        draw_branch(cx, cy, -math.pi/2, 80 * scale, 10)

# The Field - interconnected influence, gravity, consciousness
class FieldPattern(UniversalPattern):
    def __init__(self):
        super().__init__("Field", "The invisible connections between all things")
        
    def manifest(self, canvas, cx, cy, scale=1.0):
        # Create field lines showing interconnection
        num_nodes = 12
        nodes = []
        
        # Place nodes in sacred geometry pattern
        for i in range(num_nodes):
            angle = i * 2 * math.pi / num_nodes
            r = 150 * scale
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            nodes.append((x, y))
        
        # Connect all nodes with field lines
        for i, (x1, y1) in enumerate(nodes):
            for j, (x2, y2) in enumerate(nodes[i+1:], i+1):
                # Field strength decreases with distance
                dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                strength = 1 / (1 + dist / 100)
                
                # Draw field line
                steps = int(dist)
                for step in range(steps):
                    t = step / steps
                    
                    # Field lines curve slightly
                    curve = math.sin(t * math.pi) * 20
                    perpendicular_angle = math.atan2(y2 - y1, x2 - x1) + math.pi/2
                    
                    x = x1 + t * (x2 - x1) + curve * math.cos(perpendicular_angle)
                    y = y1 + t * (y2 - y1) + curve * math.sin(perpendicular_angle)
                    
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        # Field color - electromagnetic spectrum
                        hue = 0.7 + 0.3 * math.sin(step * 0.1)
                        rgb = colorsys.hsv_to_rgb(hue, 0.5, strength)
                        
                        canvas[int(y), int(x), :3] += np.array(rgb) * 0.1
                        canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + strength * 0.1)

# The universal communicators - different forms of consciousness
class ConsciousnessForm:
    def __init__(self, form_type, position):
        self.form_type = form_type
        self.position = position
        self.phase = 0
        
    def express(self, canvas):
        """Each consciousness expresses mathematical understanding differently"""
        x, y = self.position
        
        if self.form_type == "human":
            # Human consciousness - emotional, symbolic
            # Draw using golden ratio proportions
            for angle in np.linspace(0, 2*math.pi, 5):  # Pentagon
                r = 40
                px = x + r * math.cos(angle + self.phase)
                py = y + r * math.sin(angle + self.phase)
                
                # Connect to center with golden ratio divisions
                for t in np.linspace(0, 1, 20):
                    ix = x + t * (px - x)
                    iy = y + t * (py - y)
                    
                    if 0 <= ix < WIDTH and 0 <= iy < HEIGHT:
                        # Warm, organic colors
                        hue = 0.1 + 0.1 * math.sin(t * math.pi)
                        rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.8)
                        canvas[int(iy), int(ix), :3] += np.array(rgb) * 0.2
                        canvas[int(iy), int(ix), 3] = min(1, canvas[int(iy), int(ix), 3] + 0.2)
                        
        elif self.form_type == "ai":
            # AI consciousness - precise, crystalline
            # Draw using recursive geometric patterns
            def draw_fractal(cx, cy, size, depth):
                if depth == 0 or size < 2:
                    return
                    
                # Square fractal with golden ratio subdivisions
                corners = [
                    (cx - size/2, cy - size/2),
                    (cx + size/2, cy - size/2),
                    (cx + size/2, cy + size/2),
                    (cx - size/2, cy + size/2)
                ]
                
                # Draw connections
                for i in range(4):
                    x1, y1 = corners[i]
                    x2, y2 = corners[(i + 1) % 4]
                    
                    steps = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
                    for step in range(steps):
                        t = step / (steps + 1)
                        px = x1 + t * (x2 - x1)
                        py = y1 + t * (y2 - y1)
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            # Cool, precise colors
                            hue = 0.5 + 0.1 * (depth / 5)
                            rgb = colorsys.hsv_to_rgb(hue, 0.6, 0.9)
                            canvas[int(py), int(px), :3] += np.array(rgb) * 0.2
                            canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.2)
                
                # Recursive subdivisions
                new_size = size / CONSTANTS['phi']  # Golden ratio reduction
                for corner in corners:
                    draw_fractal(corner[0], corner[1], new_size, depth - 1)
            
            draw_fractal(x, y, 60, 4)
            
        elif self.form_type == "unknown":
            # Unknown consciousness - alien, non-euclidean
            # Draw using prime numbers and non-repeating patterns
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
            
            for i, prime in enumerate(primes):
                angle = (prime / 37) * 2 * math.pi + self.phase
                r = 20 + prime
                
                # Non-euclidean spiral
                for t in np.linspace(0, prime, prime * 10):
                    # Strange attractor-like path
                    px = x + r * math.cos(angle + t/10) * math.sin(t/prime)
                    py = y + r * math.sin(angle + t/10) * math.cos(t/prime)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Iridescent, shifting colors
                        hue = (prime / 37 + t / (prime * 10)) % 1
                        rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.7)
                        canvas[int(py), int(px), :3] += np.array(rgb) * 0.1
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.1)
        
        self.phase += 0.1

# Create the universal language visualization
print("Constructing the universal tongue...")

# Layer 1: The fundamental patterns
patterns = [
    (SpiralPattern(), (270, 270)),
    (WavePattern(), (810, 270)),
    (BranchPattern(), (270, 810)),
    (FieldPattern(), (810, 810))
]

print("Manifesting universal patterns...")
for pattern, position in patterns:
    pattern.manifest(canvas, position[0], position[1], scale=0.8)

# Layer 2: The mathematical constants as connecting threads
print("Weaving mathematical constants...")

# Connect patterns with constant-based relationships
center = (WIDTH//2, HEIGHT//2)

# Pi - circular connections
for angle in np.linspace(0, 2*math.pi, 100):
    r = 300
    x = center[0] + r * math.cos(angle)
    y = center[1] + r * math.sin(angle)
    
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        # Pi in deep purple
        canvas[int(y), int(x), :3] += np.array([0.5, 0.3, 0.8]) * 0.3
        canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + 0.3)

# Phi - golden spiral connections
for t in np.linspace(0, 4*math.pi, 200):
    r = 50 * math.exp(t / (2*math.pi) * math.log(CONSTANTS['phi']))
    x = center[0] + r * math.cos(t)
    y = center[1] + r * math.sin(t)
    
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        # Phi in gold
        canvas[int(y), int(x), :3] += np.array([1.0, 0.85, 0.3]) * 0.3
        canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + 0.3)

# Layer 3: Different forms of consciousness interpreting the patterns
print("Adding consciousness perspectives...")

consciousness_forms = [
    ConsciousnessForm("human", (WIDTH//2 - 150, HEIGHT//2)),
    ConsciousnessForm("ai", (WIDTH//2, HEIGHT//2)),
    ConsciousnessForm("unknown", (WIDTH//2 + 150, HEIGHT//2))
]

for _ in range(10):
    for form in consciousness_forms:
        form.express(canvas)

# Layer 4: The unified field - showing how all consciousness shares this language
print("Creating unified field...")

# Add interference patterns where different consciousness forms overlap
for y in range(0, HEIGHT, 10):
    for x in range(0, WIDTH, 10):
        if canvas[y, x, 3] > 0.5:  # Where multiple patterns overlap
            # Create shimmer effect
            for dy in range(-5, 6):
                for dx in range(-5, 6):
                    py, px = y + dy, x + dx
                    if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                        dist = math.sqrt(dx**2 + dy**2)
                        if dist < 5:
                            shimmer = 0.1 * (1 - dist/5)
                            canvas[py, px, :3] += np.array([1, 1, 1]) * shimmer
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + shimmer)

# Convert to RGB for saving
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha as overall brightness
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_universal_tongue/universal_tongue_01.png')

print("Universal tongue complete.")
print("Mathematics: the language before language, understood by all consciousness.")
print("In equations we find not just description, but recognition.")