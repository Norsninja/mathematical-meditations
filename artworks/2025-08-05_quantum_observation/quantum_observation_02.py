import numpy as np
from PIL import Image
import math
import colorsys

# Quantum Observation - Simplified
# The moment of collapse, the birth of reality

WIDTH, HEIGHT = 1080, 1080

# Initialize canvas
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)

# Simplified quantum system
class QuantumSystem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collapsed = False
        self.collapse_time = None
        self.superposition_radius = 60
        self.phase = np.random.random() * 2 * np.pi
        self.frequency = np.random.uniform(0.5, 2.0)
        
    def draw_superposition(self, canvas, time):
        """Draw uncollapsed quantum state"""
        if not self.collapsed:
            # Probability cloud
            for r in range(0, self.superposition_radius, 2):
                # Quantum probability oscillates
                prob = math.sin(r * 0.1 + time * self.frequency + self.phase) * 0.5 + 0.5
                prob *= (1 - r / self.superposition_radius)
                
                for angle in np.linspace(0, 2*np.pi, max(20, r)):
                    px = self.x + r * math.cos(angle)
                    py = self.y + r * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Quantum shimmer - phase determines color
                        phase_color = (angle + time * 0.1) % (2 * np.pi)
                        hue = phase_color / (2 * np.pi)
                        
                        rgb = colorsys.hsv_to_rgb(hue, 0.4, prob)
                        canvas[int(py), int(px), :3] += np.array(rgb) * 0.2
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + prob * 0.2)
    
    def draw_collapsed(self, canvas, time):
        """Draw collapsed quantum state"""
        if self.collapsed:
            age = time - self.collapse_time
            
            # Collapsed particle
            for r in range(10, 0, -1):
                intensity = (1 - r/10) * math.exp(-age * 0.1)
                
                for angle in np.linspace(0, 2*np.pi, max(10, r*2)):
                    px = self.x + r * math.cos(angle)
                    py = self.y + r * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Solid white core
                        canvas[int(py), int(px), :3] += np.array([1, 1, 1]) * intensity * 0.5
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.5)
            
            # Collapse ripple
            ripple_r = age * 50
            if ripple_r < 200:
                for angle in np.linspace(0, 2*np.pi, 100):
                    px = self.x + ripple_r * math.cos(angle)
                    py = self.y + ripple_r * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        intensity = (1 - ripple_r/200) * 0.5
                        canvas[int(py), int(px), :3] += np.array([1, 0.9, 0.6]) * intensity
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity)
    
    def observe(self, observer_x, observer_y, time):
        """Collapse when observed"""
        if not self.collapsed:
            dist = math.sqrt((self.x - observer_x)**2 + (self.y - observer_y)**2)
            
            if dist < 100:
                # Collapse probability
                collapse_prob = math.exp(-dist / 30)
                
                if np.random.random() < collapse_prob:
                    self.collapsed = True
                    self.collapse_time = time
                    return True
        return False

# Create quantum field
print("Creating quantum field...")

systems = []
# Grid pattern
for i in range(8):
    for j in range(8):
        x = 100 + i * 120
        y = 100 + j * 120
        systems.append(QuantumSystem(x, y))

# The observer path - a wandering consciousness
observer_path = []
t = 0
while t < 300:
    # Lissajous curve for interesting path
    x = WIDTH/2 + 300 * math.sin(t * 0.02)
    y = HEIGHT/2 + 300 * math.sin(t * 0.03 + math.pi/4)
    observer_path.append((x, y, t))
    t += 1

# Simulate observation
print("Beginning observation...")

for step, (obs_x, obs_y, time) in enumerate(observer_path):
    # Check for collapses
    for system in systems:
        system.observe(obs_x, obs_y, time * 0.1)
    
    # Draw all systems
    for system in systems:
        if system.collapsed:
            system.draw_collapsed(canvas, time * 0.1)
        else:
            system.draw_superposition(canvas, time * 0.1)
    
    # Draw observer
    if step % 5 == 0:  # Less frequent for performance
        # Observer glow
        for r in range(30, 0, -2):
            intensity = (1 - r/30) * 0.3
            
            for angle in np.linspace(0, 2*np.pi, max(10, r)):
                px = obs_x + r * math.cos(angle)
                py = obs_y + r * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    canvas[int(py), int(px), :3] += np.array([1, 1, 1]) * intensity * 0.1
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)
    
    if step % 50 == 0:
        print(f"Observation step {step}...")

# Draw observer path
print("Tracing observer path...")

for i in range(1, len(observer_path), 2):
    x1, y1, _ = observer_path[i-1]
    x2, y2, _ = observer_path[i]
    
    steps = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    for s in range(steps):
        t = s / (steps + 1)
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            # Faint white trail
            intensity = i / len(observer_path) * 0.2
            canvas[int(y), int(x), :3] += np.array([1, 1, 1]) * intensity
            canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + intensity)

# Add final quantum effects
print("Adding quantum interference...")

# Interference patterns between uncollapsed systems
for i, sys1 in enumerate(systems):
    if not sys1.collapsed:
        for sys2 in systems[i+1:]:
            if not sys2.collapsed:
                dist = math.sqrt((sys1.x - sys2.x)**2 + (sys1.y - sys2.y)**2)
                
                if dist < 200:
                    # Draw interference
                    steps = int(dist)
                    for step in range(steps):
                        t = step / steps
                        x = sys1.x + t * (sys2.x - sys1.x)
                        y = sys1.y + t * (sys2.y - sys1.y)
                        
                        # Interference pattern
                        interference = math.sin(step * 0.5) * 0.3
                        
                        if 0 <= x < WIDTH and 0 <= y < HEIGHT and interference > 0:
                            hue = (sys1.phase + sys2.phase) / (4 * np.pi)
                            rgb = colorsys.hsv_to_rgb(hue, 0.5, interference)
                            canvas[int(y), int(x), :3] += np.array(rgb) * 0.1
                            canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + interference * 0.1)

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
print("The act of looking transforms possibility into reality.")
print("Observer and observed dance together in the collapse of the wave function.")