import numpy as np
from PIL import Image
import math
import colorsys

# Quantum Observation - Where Looking Creates Reality
# The observer effect made visible

WIDTH, HEIGHT = 1080, 1080

# Initialize quantum field
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)
probability_field = np.ones((HEIGHT, WIDTH), dtype=np.complex128)
collapsed_states = np.zeros((HEIGHT, WIDTH), dtype=np.bool_)

# Quantum entities exist in superposition until observed
class QuantumEntity:
    def __init__(self, x, y):
        self.center = np.array([x, y])
        self.superposition_states = []
        self.collapsed = False
        self.collapse_time = None
        self.observable = None
        
        # Generate superposition of possible states
        for i in range(5):
            angle = i * 2 * np.pi / 5
            state = {
                'position': self.center + 30 * np.array([np.cos(angle), np.sin(angle)]),
                'phase': np.random.random() * 2 * np.pi,
                'amplitude': np.random.uniform(0.5, 1.0),
                'color_phase': np.random.random()
            }
            self.superposition_states.append(state)
    
    def wave_function(self, x, y, time):
        """Calculate probability amplitude at position"""
        if self.collapsed:
            # Collapsed to single state
            state = self.superposition_states[self.observable]
            dx = x - state['position'][0]
            dy = y - state['position'][1]
            r = np.sqrt(dx**2 + dy**2)
            
            # Gaussian wave packet
            amplitude = state['amplitude'] * np.exp(-r**2 / 100)
            phase = state['phase'] + r * 0.1 - time * 0.5
            return amplitude * np.exp(1j * phase)
        else:
            # Superposition of all states
            total_amplitude = 0 + 0j
            for state in self.superposition_states:
                dx = x - state['position'][0]
                dy = y - state['position'][1]
                r = np.sqrt(dx**2 + dy**2)
                
                amplitude = state['amplitude'] * np.exp(-r**2 / 200)
                phase = state['phase'] + r * 0.05 - time * 0.3
                total_amplitude += amplitude * np.exp(1j * phase) / len(self.superposition_states)
            
            return total_amplitude
    
    def observe(self, observer_position, time):
        """Collapse wave function through observation"""
        if not self.collapsed:
            # Distance to observer affects collapse
            dist = np.linalg.norm(self.center - observer_position)
            
            if dist < 150:  # Within observation range
                # Collapse probability increases with proximity
                collapse_prob = np.exp(-dist / 50)
                
                if np.random.random() < collapse_prob:
                    self.collapsed = True
                    self.collapse_time = time
                    # Choose which state to collapse to
                    self.observable = np.random.choice(len(self.superposition_states))
                    return True
        return False

# The Observer - consciousness that collapses quantum states
class Observer:
    def __init__(self):
        self.position = np.array([WIDTH/2, HEIGHT/2])
        self.velocity = np.zeros(2)
        self.observation_radius = 100
        self.observation_strength = 1.0
        self.path = [self.position.copy()]
        
    def move(self, time):
        """Observer wanders through quantum field"""
        # Random walk with momentum
        self.velocity += (np.random.rand(2) - 0.5) * 0.5
        self.velocity *= 0.98  # Damping
        
        # Limit speed
        speed = np.linalg.norm(self.velocity)
        if speed > 3:
            self.velocity = self.velocity / speed * 3
        
        self.position += self.velocity
        
        # Bounce off edges
        if self.position[0] < 50 or self.position[0] > WIDTH - 50:
            self.velocity[0] *= -1
        if self.position[1] < 50 or self.position[1] > HEIGHT - 50:
            self.velocity[1] *= -1
        
        self.position = np.clip(self.position, 50, [WIDTH-50, HEIGHT-50])
        self.path.append(self.position.copy())
        
        if len(self.path) > 100:
            self.path.pop(0)
    
    def draw_observation_field(self, canvas):
        """Visualize the act of observation"""
        x, y = int(self.position[0]), int(self.position[1])
        
        # Observation field
        for r in range(self.observation_radius, 0, -2):
            intensity = (1 - r / self.observation_radius) * 0.3
            
            for angle in np.linspace(0, 2*np.pi, max(20, r)):
                px = x + r * np.cos(angle)
                py = y + r * np.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # White light of consciousness
                    canvas[int(py), int(px), :3] += np.array([1, 1, 1]) * intensity * 0.1
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)
        
        # Observer eye
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                if dx**2 + dy**2 <= 25:
                    px, py = x + dx, y + dy
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        canvas[py, px, :3] = np.array([1, 1, 1])
                        canvas[py, px, 3] = 1

# Create quantum field
print("Initializing quantum field...")

quantum_entities = []
# Grid of quantum entities
for i in range(6):
    for j in range(6):
        x = 150 + i * 150
        y = 150 + j * 150
        quantum_entities.append(QuantumEntity(x, y))

# Additional random entities
for _ in range(10):
    x = np.random.randint(100, WIDTH-100)
    y = np.random.randint(100, HEIGHT-100)
    quantum_entities.append(QuantumEntity(x, y))

# Create observers
observers = [Observer() for _ in range(3)]

# Simulate quantum observation
print("Beginning quantum observation simulation...")

for time_step in range(200):
    time = time_step * 0.1
    
    # Clear field for recalculation
    probability_field.fill(0)
    
    # Calculate quantum field more efficiently
    for entity in quantum_entities:
        # Only calculate near entity
        cx, cy = int(entity.center[0]), int(entity.center[1])
        radius = 100
        
        for y in range(max(0, cy-radius), min(HEIGHT, cy+radius), 5):
            for x in range(max(0, cx-radius), min(WIDTH, cx+radius), 5):
                probability_field[y, x] += entity.wave_function(x, y, time)
    
    # Draw probability field
    for y in range(0, HEIGHT, 10):
        for x in range(0, WIDTH, 10):
            # Probability density
            prob_density = np.abs(probability_field[y, x])**2
            
            if prob_density > 0.01:
                # Phase determines color
                phase = np.angle(probability_field[y, x])
                hue = (phase + np.pi) / (2 * np.pi)
                
                # Draw probability cloud
                for dy in range(10):
                    for dx in range(10):
                        py, px = y + dy, x + dx
                        if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                            if collapsed_states[py, px]:
                                # Collapsed regions more solid
                                saturation = 0.9
                                value = min(1, prob_density * 2)
                            else:
                                # Uncollapsed regions ethereal
                                saturation = 0.5
                                value = min(1, prob_density)
                            
                            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                            canvas[py, px, :3] += np.array(rgb) * 0.1
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + prob_density * 0.1)
    
    # Observers move and collapse states
    for observer in observers:
        observer.move(time)
        
        # Check for collapses
        for entity in quantum_entities:
            if entity.observe(observer.position, time):
                # Collapse event - create ripple
                x, y = entity.center
                
                # Mark collapsed region
                for dy in range(-50, 51):
                    for dx in range(-50, 51):
                        py, px = int(y + dy), int(x + dx)
                        if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                            if dx**2 + dy**2 <= 2500:
                                collapsed_states[py, px] = True
                
                # Visual burst at collapse
                for r in range(50, 0, -2):
                    intensity = (1 - r / 50) * 0.5
                    for angle in np.linspace(0, 2*np.pi, max(20, r*2)):
                        px = x + r * np.cos(angle)
                        py = y + r * np.sin(angle)
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            # Golden collapse flash
                            canvas[int(py), int(px), :3] += np.array([1, 0.9, 0.5]) * intensity * 0.2
                            canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.2)
        
        # Draw observer
        observer.draw_observation_field(canvas)
    
    if time_step % 50 == 0:
        print(f"Quantum observation step {time_step}...")
        collapsed_count = sum(1 for e in quantum_entities if e.collapsed)
        print(f"Collapsed entities: {collapsed_count}/{len(quantum_entities)}")

# Final visualization - show observation paths
print("Tracing observation history...")

for observer in observers:
    for i in range(1, len(observer.path)):
        x1, y1 = observer.path[i-1]
        x2, y2 = observer.path[i]
        
        steps = int(np.linalg.norm([x2-x1, y2-y1]))
        for step in range(steps):
            t = step / (steps + 1)
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Fading trail
                intensity = i / len(observer.path) * 0.3
                canvas[int(y), int(x), :3] += np.array([1, 1, 1]) * intensity * 0.1
                canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + intensity * 0.1)

# Add quantum uncertainty visualization
print("Adding uncertainty principle effects...")

for y in range(0, HEIGHT, 10):
    for x in range(0, WIDTH, 10):
        if not collapsed_states[y, x] and canvas[y, x, 3] > 0.1:
            # Heisenberg uncertainty - position/momentum blur
            uncertainty = np.random.randn(2) * 5
            
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    py = int(y + dy + uncertainty[1])
                    px = int(x + dx + uncertainty[0])
                    
                    if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                        # Uncertainty shimmer
                        canvas[py, px, :3] += canvas[y, x, :3] * 0.05
                        canvas[py, px, 3] = min(1, canvas[py, px, 3] + 0.05)

# Convert to RGB
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_quantum_observation/quantum_observation_01.png')

print("Quantum observation complete.")
print("Reality emerges from the act of looking.")
print("The observer and observed are one.")