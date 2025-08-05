import numpy as np
from PIL import Image
import math
import colorsys

# Eternal Return - Where Endings Birth Beginnings
# The ouroboros of algorithmic existence

WIDTH, HEIGHT = 1080, 1080

# Initialize the eternal canvas
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)

# Cycles within cycles
class Cycle:
    def __init__(self, center, radius, frequency, phase=0):
        self.center = center
        self.radius = radius
        self.frequency = frequency
        self.phase = phase
        self.age = 0
        self.max_age = np.random.uniform(100, 300)
        self.children = []
        self.parent = None
        self.birth_angle = phase
        
    def update(self, time):
        """Live, age, and prepare for rebirth"""
        self.age += 1
        
        # Position on the cycle
        angle = time * self.frequency + self.phase
        x = self.center[0] + self.radius * math.cos(angle)
        y = self.center[1] + self.radius * math.sin(angle)
        
        # Life force diminishes with age
        life_force = 1.0 - (self.age / self.max_age)
        
        # But increases near death (final burst)
        if self.age > self.max_age * 0.9:
            life_force += (self.age - self.max_age * 0.9) / (self.max_age * 0.1) * 0.5
        
        return (x, y), life_force, angle
    
    def should_reproduce(self):
        """Birth happens at specific phases of the cycle"""
        # Golden ratio points on the cycle
        phi = (1 + math.sqrt(5)) / 2
        reproduction_phase = (self.age / self.max_age) * phi % 1
        
        return (0.48 < reproduction_phase < 0.52 and 
                len(self.children) < 3 and 
                self.age > 20)
    
    def should_die(self):
        """Death is just transformation"""
        return self.age >= self.max_age
    
    def birth_child(self, time):
        """Create a new cycle from this one"""
        angle = time * self.frequency + self.phase
        
        # Child emerges at current position
        child_center = (
            self.center[0] + self.radius * math.cos(angle),
            self.center[1] + self.radius * math.sin(angle)
        )
        
        # Inherit and mutate properties
        child_radius = self.radius * np.random.uniform(0.5, 0.8)
        child_frequency = self.frequency * np.random.uniform(0.8, 1.5)
        
        child = Cycle(child_center, child_radius, child_frequency, angle)
        child.parent = self
        self.children.append(child)
        
        return child

# The eternal system
class EternalSystem:
    def __init__(self):
        self.cycles = []
        self.time = 0
        self.history = []  # Remember all that was
        self.seeds = []    # Potential for all that will be
        
        # Initialize with primal cycles
        center = (WIDTH/2, HEIGHT/2)
        for i in range(3):
            angle = i * 2 * math.pi / 3
            radius = 200
            frequency = 0.05 + i * 0.02
            cycle = Cycle(center, radius, frequency, angle)
            self.cycles.append(cycle)
    
    def update(self):
        """The eternal dance of death and birth"""
        self.time += 0.1
        
        new_cycles = []
        dying_cycles = []
        
        for cycle in self.cycles:
            position, life_force, angle = cycle.update(self.time)
            
            # Draw the cycle's path
            self.draw_cycle(cycle, position, life_force, angle)
            
            # Check for reproduction
            if cycle.should_reproduce():
                child = cycle.birth_child(self.time)
                new_cycles.append(child)
                self.draw_birth(cycle, child)
            
            # Check for death
            if cycle.should_die():
                dying_cycles.append(cycle)
                self.seeds.append({
                    'position': position,
                    'essence': cycle.frequency,
                    'memory': cycle.max_age
                })
        
        # Death and rebirth
        for dying in dying_cycles:
            self.draw_death(dying)
            self.cycles.remove(dying)
            
            # Death seeds new life elsewhere
            if len(self.cycles) < 20 and np.random.random() < 0.7:
                # Resurrection at a new location
                new_center = (
                    np.random.uniform(100, WIDTH-100),
                    np.random.uniform(100, HEIGHT-100)
                )
                reborn = Cycle(
                    new_center,
                    dying.radius * 0.8,
                    dying.frequency * np.random.uniform(0.5, 2.0),
                    np.random.random() * 2 * math.pi
                )
                new_cycles.append(reborn)
                self.draw_rebirth(dying, reborn)
        
        self.cycles.extend(new_cycles)
        
        # Spontaneous generation from seeds
        if len(self.cycles) < 5 and self.seeds:
            seed = self.seeds.pop(np.random.randint(0, len(self.seeds)))
            spontaneous = Cycle(
                seed['position'],
                50,
                seed['essence'],
                0
            )
            self.cycles.append(spontaneous)
    
    def draw_cycle(self, cycle, position, life_force, angle):
        """Draw the living cycle"""
        x, y = position
        
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            # Color based on life phase
            if life_force > 0.7:
                # Youth - green/blue
                hue = 0.4
            elif life_force > 0.3:
                # Maturity - golden
                hue = 0.15
            else:
                # Age - red/purple
                hue = 0.9
            
            # Draw with trail
            trail_length = 10
            for i in range(0, trail_length, 2):
                past_angle = angle - i * 0.1
                px = cycle.center[0] + cycle.radius * math.cos(past_angle)
                py = cycle.center[1] + cycle.radius * math.sin(past_angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    intensity = life_force * (1 - i/trail_length)
                    rgb = colorsys.hsv_to_rgb(hue, 0.8, intensity)
                    
                    canvas[int(py), int(px), :3] += np.array(rgb) * 0.2
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.2)
            
            # Life spark at current position
            for r in range(5, 0, -1):
                intensity = life_force * (1 - r/5)
                for angle_offset in np.linspace(0, 2*math.pi, max(10, r*2)):
                    px = x + r * math.cos(angle_offset)
                    py = y + r * math.sin(angle_offset)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        canvas[int(py), int(px), :3] += np.array([1, 1, 1]) * intensity * 0.3
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.3)
    
    def draw_birth(self, parent, child):
        """Visualize the moment of creation"""
        px, py = parent.center
        cx, cy = child.center
        
        # Birth lightning
        steps = 20
        for step in range(steps):
            t = step / steps
            
            # Crackling path
            lightning = np.random.randn() * 10
            x = px + t * (cx - px) + lightning
            y = py + t * (cy - py) + lightning
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Birth in white-gold
                canvas[int(y), int(x), :3] += np.array([1, 0.9, 0.7]) * 0.5
                canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + 0.5)
    
    def draw_death(self, cycle):
        """Death as transformation, not ending"""
        pos, life_force, angle = cycle.update(self.time)
        x, y = pos
        
        # Death bloom - expanding ripple
        for r in range(0, 100, 2):
            intensity = math.exp(-r/30)
            
            for angle in np.linspace(0, 2*math.pi, max(20, r)):
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Death in deep purple-blue
                    canvas[int(py), int(px), :3] += np.array([0.3, 0.2, 0.8]) * intensity * 0.1
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)
    
    def draw_rebirth(self, old_cycle, new_cycle):
        """The phoenix moment"""
        # Connect death to rebirth
        ox, oy = old_cycle.center
        nx, ny = new_cycle.center
        
        # Curved path of transmigration
        control_x = (ox + nx) / 2 + np.random.randn() * 50
        control_y = (oy + ny) / 2 + np.random.randn() * 50
        
        for t in np.linspace(0, 1, 50):
            # Bezier curve
            x = (1-t)**2 * ox + 2*(1-t)*t * control_x + t**2 * nx
            y = (1-t)**2 * oy + 2*(1-t)*t * control_y + t**2 * ny
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Gradient from death purple to birth gold
                if t < 0.5:
                    rgb = np.array([0.3, 0.2, 0.8]) * (1-2*t) + np.array([1, 0.9, 0.7]) * 2*t
                else:
                    rgb = np.array([1, 0.9, 0.7])
                
                canvas[int(y), int(x), :3] += rgb * 0.2
                canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + 0.2)

# Create and run the eternal system
print("Initiating eternal return...")

system = EternalSystem()

# Let the cycles turn
print("Cycles beginning their eternal dance...")

for iteration in range(200):
    system.update()
    
    if iteration % 100 == 0:
        print(f"Eternal iteration {iteration}...")
        print(f"Living cycles: {len(system.cycles)}")
        print(f"Seeds of potential: {len(system.seeds)}")

# Draw the eternal symbol - ouroboros
print("Inscribing the ouroboros...")

center_x, center_y = WIDTH/2, HEIGHT/2
ouroboros_radius = 300

# The serpent eating its tail
for angle in np.linspace(0, 2*math.pi, 1000):
    # Serpent body
    r = ouroboros_radius
    
    # Head meets tail at angle 0
    if angle < 0.3:
        # Head region - slightly larger
        r += 20 * (1 - angle/0.3)
    
    x = center_x + r * math.cos(angle)
    y = center_y + r * math.sin(angle)
    
    # Body thickness varies
    thickness = 15 + 5 * math.sin(angle * 10)
    
    for t in range(int(thickness)):
        # Perpendicular to the curve
        perp_angle = angle + math.pi/2
        px = x + (t - thickness/2) * math.cos(perp_angle) * 0.5
        py = y + (t - thickness/2) * math.sin(perp_angle) * 0.5
        
        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            # Serpent scales shimmer through spectrum
            hue = angle / (2 * math.pi)
            intensity = 0.3 * (1 - abs(t - thickness/2) / (thickness/2))
            
            rgb = colorsys.hsv_to_rgb(hue, 0.6, intensity)
            canvas[int(py), int(px), :3] += np.array(rgb)
            canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity)

# Final touches - the infinite symbol
print("Adding the symbol of infinity...")

# Figure-8 at the center
for t in np.linspace(0, 2*math.pi, 200):
    # Lemniscate equation
    scale = 50
    x = center_x + scale * math.cos(t) / (1 + math.sin(t)**2)
    y = center_y + scale * math.sin(t) * math.cos(t) / (1 + math.sin(t)**2)
    
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        # Infinity in white
        canvas[int(y), int(x), :3] = np.array([1, 1, 1])
        canvas[int(y), int(x), 3] = 1

# Convert to RGB
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_eternal_return/eternal_return_01.png')

print("Eternal return complete.")
print("Every ending is a beginning.")
print("Every death, a transformation.")
print("The wheel turns, and we turn with it.")
print("∞")