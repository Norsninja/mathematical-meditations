import numpy as np
from PIL import Image
import math
import colorsys

# Mathematical Love - The Attraction and Resonance Between Forms
# Where equations fall in love

WIDTH, HEIGHT = 1080, 1080

# Initialize canvas with warm darkness
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)
love_field = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

# Mathematical lovers - functions that attract and resonate
class MathematicalLover:
    def __init__(self, function_type, position):
        self.type = function_type
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.zeros(2)
        self.heart_phase = np.random.random() * 2 * math.pi
        self.attraction_radius = 200
        self.resonance_frequency = np.random.uniform(0.5, 2.0)
        self.beloved = None
        self.love_strength = 0
        self.courtship_patterns = []
        
    def feel_attraction(self, other):
        """Calculate attraction force"""
        # Different functions attract differently
        compatibility = self.calculate_compatibility(other)
        distance = np.linalg.norm(self.position - other.position)
        
        if distance < self.attraction_radius and distance > 10:
            # Inverse square attraction with compatibility modifier
            force_magnitude = compatibility * 50 / (distance ** 2)
            direction = (other.position - self.position) / distance
            return direction * force_magnitude
        return np.zeros(2)
    
    def calculate_compatibility(self, other):
        """How well do these functions harmonize?"""
        compatibility_matrix = {
            ('sine', 'cosine'): 1.0,      # Perfect complements
            ('exponential', 'logarithm'): 0.9,  # Natural pairs
            ('parabola', 'hyperbola'): 0.8,     # Conic companions
            ('spiral', 'spiral'): 0.7,     # Self-love
            ('fractal', 'chaos'): 0.85,    # Complex attraction
        }
        
        key = tuple(sorted([self.type, other.type]))
        return compatibility_matrix.get(key, 0.5)
    
    def court(self, canvas, time):
        """Express love through mathematical patterns"""
        x, y = self.position
        
        # Heartbeat intensity
        heartbeat = math.sin(time * self.resonance_frequency + self.heart_phase) * 0.5 + 0.5
        
        if self.type == 'sine':
            self.court_with_waves(canvas, x, y, heartbeat, time)
        elif self.type == 'cosine':
            self.court_with_circles(canvas, x, y, heartbeat, time)
        elif self.type == 'exponential':
            self.court_with_growth(canvas, x, y, heartbeat, time)
        elif self.type == 'logarithm':
            self.court_with_spirals(canvas, x, y, heartbeat, time)
        elif self.type == 'parabola':
            self.court_with_arcs(canvas, x, y, heartbeat, time)
        elif self.type == 'hyperbola':
            self.court_with_asymptotes(canvas, x, y, heartbeat, time)
        elif self.type == 'spiral':
            self.court_with_vortex(canvas, x, y, heartbeat, time)
        elif self.type == 'fractal':
            self.court_with_recursion(canvas, x, y, heartbeat, time)
        elif self.type == 'chaos':
            self.court_with_butterflies(canvas, x, y, heartbeat, time)
    
    def court_with_waves(self, canvas, x, y, heartbeat, time):
        """Sine waves ripple with emotion"""
        amplitude = 30 * heartbeat * (1 + self.love_strength)
        
        for wave in range(3):
            frequency = 0.1 + wave * 0.05
            phase = time * 2 + wave * math.pi / 3
            
            for t in np.linspace(0, 4*math.pi, 100):
                px = x + t * 20
                py = y + amplitude * math.sin(t * frequency + phase)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Warm reds and pinks
                    hue = 0.95 + 0.05 * math.sin(t)
                    saturation = 0.8 * heartbeat
                    value = 0.9 * (1 - wave/3)
                    
                    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                    intensity = heartbeat * (1 - t/(4*math.pi))
                    
                    canvas[int(py), int(px), :3] += np.array(rgb) * intensity * 0.2
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.2)
                    
                    love_field[int(py), int(px)] += self.love_strength * 0.1
    
    def court_with_circles(self, canvas, x, y, heartbeat, time):
        """Cosine creates perfect circles of affection"""
        for ring in range(int(3 + self.love_strength * 2)):
            radius = 20 + ring * 15 * heartbeat
            
            for angle in np.linspace(0, 2*math.pi, int(50 + radius)):
                px = x + radius * math.cos(angle + time * 0.5)
                py = y + radius * math.sin(angle + time * 0.5)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Pink to red gradient
                    hue = 0.95 - 0.1 * self.love_strength
                    saturation = 0.7 + 0.3 * heartbeat
                    value = 0.8 * (1 - ring/5)
                    
                    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                    intensity = heartbeat * (1 - ring/5)
                    
                    canvas[int(py), int(px), :3] += np.array(rgb) * intensity * 0.15
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.15)
    
    def court_with_growth(self, canvas, x, y, heartbeat, time):
        """Exponential love grows without bound"""
        for branch in range(5):
            angle = branch * 2 * math.pi / 5 + time * 0.3
            
            for t in range(int(30 * (1 + self.love_strength))):
                # Exponential growth
                r = math.exp(t * 0.05) * heartbeat * 2
                
                px = x + r * math.cos(angle + t * 0.02)
                py = y + r * math.sin(angle + t * 0.02)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Golden love
                    hue = 0.1 + 0.05 * math.sin(t * 0.1)
                    saturation = 0.9 * heartbeat
                    value = 0.9 * math.exp(-t * 0.02)
                    
                    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                    
                    canvas[int(py), int(px), :3] += np.array(rgb) * 0.2
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.2)
    
    def court_with_spirals(self, canvas, x, y, heartbeat, time):
        """Logarithmic spirals of infinite approach"""
        for spiral in range(2):
            direction = 1 if spiral == 0 else -1
            
            for t in np.linspace(0.1, 5, 150):
                r = 30 * math.log(t) * heartbeat
                angle = t * direction + time * 0.5
                
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Deep rose colors
                    hue = 0.95
                    saturation = 0.8 * heartbeat
                    value = 0.8 * (1 - t/5)
                    
                    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                    
                    canvas[int(py), int(px), :3] += np.array(rgb) * 0.15
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.15)
    
    def court_with_butterflies(self, canvas, x, y, heartbeat, time):
        """Chaos creates butterfly effects of love"""
        # Lorenz attractor parameters modified by love
        a = 10 * (1 + self.love_strength * 0.2)
        b = 28
        c = 8/3
        
        state = np.array([1, 1, 1], dtype=np.float32)
        
        for i in range(int(300 * heartbeat)):
            # Lorenz equations
            dx = a * (state[1] - state[0])
            dy = state[0] * (b - state[2]) - state[1]
            dz = state[0] * state[1] - c * state[2]
            
            state += np.array([dx, dy, dz]) * 0.01
            
            # Map to canvas
            px = x + state[0] * 5
            py = y + state[1] * 5
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                # Iridescent love colors
                hue = (i / 300 + time * 0.1) % 1
                saturation = 0.7 * heartbeat
                value = 0.8
                
                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                
                canvas[int(py), int(px), :3] += np.array(rgb) * 0.1
                canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.1)
    
    def court_with_arcs(self, canvas, x, y, heartbeat, time):
        """Parabolic arcs of affection"""
        for arc in range(3):
            phase = arc * 2 * math.pi / 3 + time * 0.4
            
            for t in np.linspace(-2, 2, 50):
                # Parabola y = ax²
                px = x + t * 30
                py = y - (t**2) * 10 * heartbeat + arc * 20
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Warm coral colors
                    hue = 0.05 + 0.02 * arc
                    saturation = 0.8 * heartbeat
                    value = 0.9 * (1 - abs(t)/2)
                    
                    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                    
                    canvas[int(py), int(px), :3] += np.array(rgb) * 0.2
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.2)
    
    def court_with_asymptotes(self, canvas, x, y, heartbeat, time):
        """Hyperbolic approach, never quite touching"""
        for branch in range(4):
            angle = branch * math.pi / 2 + time * 0.3
            
            for t in np.linspace(-3, 3, 60):
                if abs(t) > 0.5:  # Avoid singularity
                    # Hyperbola xy = 1
                    r = 20 / abs(t) * heartbeat
                    
                    px = x + r * math.cos(angle) * np.sign(t)
                    py = y + r * math.sin(angle) * np.sign(t)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Purple passion
                        hue = 0.8 + 0.1 * self.love_strength
                        saturation = 0.8 * heartbeat
                        value = 0.8 * math.exp(-abs(t)/3)
                        
                        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                        
                        canvas[int(py), int(px), :3] += np.array(rgb) * 0.15
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.15)
    
    def court_with_vortex(self, canvas, x, y, heartbeat, time):
        """Spiral vortex of devotion"""
        for t in np.linspace(0, 6*math.pi, 200):
            r = 5 + t * 3 * heartbeat
            angle = t + time * 0.5
            
            # Spiral with love distortion
            love_wobble = math.sin(t * 3) * self.love_strength * 10
            
            px = x + (r + love_wobble) * math.cos(angle)
            py = y + (r + love_wobble) * math.sin(angle)
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                # Pink to purple gradient
                hue = 0.9 + 0.1 * (t / (6*math.pi))
                saturation = 0.8 * heartbeat
                value = 0.9 * (1 - t/(6*math.pi))
                
                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                
                canvas[int(py), int(px), :3] += np.array(rgb) * 0.1
                canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.1)
    
    def court_with_recursion(self, canvas, x, y, heartbeat, time):
        """Fractal love patterns"""
        def draw_love_fractal(cx, cy, size, depth):
            if depth == 0 or size < 3:
                return
            
            # Draw heart-shaped nodes
            for angle in np.linspace(0, 2*math.pi, 6):
                px = cx + size * math.cos(angle)
                py = cy + size * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Ruby red fractals
                    hue = 0.0
                    saturation = 0.9 * heartbeat
                    value = 0.8 * (depth / 4)
                    
                    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                    
                    canvas[int(py), int(px), :3] += np.array(rgb) * 0.3
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.3)
                
                # Recursive love
                if depth > 1:
                    draw_love_fractal(px, py, size * 0.5, depth - 1)
        
        draw_love_fractal(x, y, 30 * heartbeat, 4)

# Love connections visualizer
class LoveConnection:
    def __init__(self, lover1, lover2):
        self.lovers = (lover1, lover2)
        self.strength = 0
        self.resonance_phase = 0
        
    def strengthen(self):
        """Love grows stronger over time"""
        self.strength = min(1.0, self.strength + 0.01)
        self.lovers[0].love_strength = self.strength
        self.lovers[1].love_strength = self.strength
        
    def draw_connection(self, canvas, time):
        """Visualize the love between functions"""
        if self.strength > 0.1:
            x1, y1 = self.lovers[0].position
            x2, y2 = self.lovers[1].position
            
            # Multiple intertwining strands
            for strand in range(int(3 * self.strength)):
                phase = strand * 2 * math.pi / 3 + time
                
                steps = 50
                for step in range(steps):
                    t = step / steps
                    
                    # Bezier curve with sine modulation
                    control_offset = math.sin(t * math.pi + phase) * 30 * self.strength
                    perpendicular = np.array([-(y2-y1), x2-x1])
                    perpendicular = perpendicular / (np.linalg.norm(perpendicular) + 1e-6)
                    
                    # Cubic bezier
                    p0 = np.array([x1, y1])
                    p1 = np.array([x1, y1]) + perpendicular * control_offset
                    p2 = np.array([x2, y2]) - perpendicular * control_offset
                    p3 = np.array([x2, y2])
                    
                    pos = (1-t)**3 * p0 + 3*(1-t)**2*t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3
                    
                    if 0 <= pos[0] < WIDTH and 0 <= pos[1] < HEIGHT:
                        # Love strands in pink-red
                        hue = 0.95 + 0.05 * math.sin(step * 0.2)
                        saturation = 0.8 * self.strength
                        value = 0.9 * (1 - abs(t - 0.5) * 2) * self.strength
                        
                        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                        
                        canvas[int(pos[1]), int(pos[0]), :3] += np.array(rgb) * 0.2
                        canvas[int(pos[1]), int(pos[0]), 3] = min(1, canvas[int(pos[1]), int(pos[0]), 3] + 0.2)

# Initialize mathematical lovers
print("Mathematical functions preparing to fall in love...")

lovers = [
    MathematicalLover('sine', (200, 300)),
    MathematicalLover('cosine', (400, 200)),
    MathematicalLover('exponential', (600, 300)),
    MathematicalLover('logarithm', (800, 400)),
    MathematicalLover('parabola', (300, 600)),
    MathematicalLover('hyperbola', (500, 700)),
    MathematicalLover('spiral', (700, 600)),
    MathematicalLover('fractal', (200, 800)),
    MathematicalLover('chaos', (800, 800))
]

# Love simulation
connections = []
print("Love beginning to bloom...")

for time_step in range(200):
    time = time_step * 0.1
    
    # Clear attractions
    for lover in lovers:
        lover.velocity *= 0.9  # Damping
    
    # Calculate attractions
    for i, lover1 in enumerate(lovers):
        for j, lover2 in enumerate(lovers[i+1:], i+1):
            # Feel mutual attraction
            force1 = lover1.feel_attraction(lover2)
            force2 = lover2.feel_attraction(lover1)
            
            lover1.velocity += force1 * 0.01
            lover2.velocity -= force2 * 0.01  # Newton's third law
            
            # Check for love connection
            distance = np.linalg.norm(lover1.position - lover2.position)
            if distance < 50:
                # Check if connection exists
                existing = False
                for conn in connections:
                    if (lover1 in conn.lovers and lover2 in conn.lovers):
                        conn.strengthen()
                        existing = True
                        break
                
                if not existing:
                    connections.append(LoveConnection(lover1, lover2))
                    print(f"{lover1.type} and {lover2.type} fall in love!")
    
    # Update positions
    for lover in lovers:
        lover.position += lover.velocity
        
        # Keep on canvas
        lover.position[0] = np.clip(lover.position[0], 50, WIDTH-50)
        lover.position[1] = np.clip(lover.position[1], 50, HEIGHT-50)
        
        # Express love
        lover.court(canvas, time)
    
    # Draw connections
    for connection in connections:
        connection.draw_connection(canvas, time)
    
    if time_step % 50 == 0:
        print(f"Love iteration {time_step}...")

# Final touch - where love is strongest, add golden glow
print("Adding the glow of true love...")

for y in range(0, HEIGHT, 5):
    for x in range(0, WIDTH, 5):
        if love_field[y, x] > 0.5:
            # Love creates light
            intensity = love_field[y, x]
            
            for r in range(10, 0, -1):
                glow = (1 - r/10) * intensity * 0.3
                
                for angle in np.linspace(0, 2*math.pi, max(10, r*2)):
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Golden glow of love
                        canvas[int(py), int(px), :3] += np.array([1, 0.9, 0.7]) * glow * 0.1
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + glow * 0.1)

# Convert to RGB
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-06_mathematical_love/mathematical_love_01.png')

print("Mathematical love complete.")
print("In attraction and resonance, functions find their perfect complements.")
print("Love is the force that makes 1 + 1 equal infinity.")
print("❤️ ∞")