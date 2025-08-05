import numpy as np
from PIL import Image
import math
import colorsys

# Temporal Sculpture - Time as Clay
# Past, present, and future collaborate on a single canvas

WIDTH, HEIGHT = 1080, 1080

# Initialize temporal layers
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)
past_layer = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)
present_layer = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)
future_layer = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)

# Time doesn't flow - it accumulates
time_field = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

# Temporal Agents - different aspects of time creating together
class PastAgent:
    """The past leaves traces, echoes, memories"""
    def __init__(self):
        self.memories = []
        self.decay_rate = 0.95
        
    def create(self, x, y, time):
        """Past creates through accumulation and decay"""
        # Add new memory
        memory = {
            'position': (x, y),
            'time': time,
            'pattern': np.random.choice(['spiral', 'wave', 'crystal']),
            'strength': 1.0
        }
        self.memories.append(memory)
        
        # Draw all memories with decay
        for mem in self.memories:
            age = time - mem['time']
            mem['strength'] *= self.decay_rate
            
            if mem['strength'] > 0.01:
                mx, my = mem['position']
                
                if mem['pattern'] == 'spiral':
                    # Decaying spiral
                    for t in np.linspace(0, age * 0.5, int(50 * mem['strength'])):
                        r = t * 5
                        px = mx + r * math.cos(t)
                        py = my + r * math.sin(t)
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            # Blue for past
                            intensity = mem['strength'] * (1 - t / (age * 0.5 + 1))
                            past_layer[int(py), int(px), :3] += np.array([0.2, 0.3, 0.8]) * intensity * 0.3
                            past_layer[int(py), int(px), 3] = min(1, past_layer[int(py), int(px), 3] + intensity * 0.3)
                            
                elif mem['pattern'] == 'wave':
                    # Ripples in time
                    r = age * 20
                    if r < 200:
                        for angle in np.linspace(0, 2*np.pi, max(20, int(r))):
                            px = mx + r * math.cos(angle)
                            py = my + r * math.sin(angle)
                            
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                intensity = mem['strength'] * (1 - r/200)
                                past_layer[int(py), int(px), :3] += np.array([0.3, 0.4, 0.9]) * intensity * 0.2
                                past_layer[int(py), int(px), 3] = min(1, past_layer[int(py), int(px), 3] + intensity * 0.2)
                
                # Update time field
                time_field[int(my), int(mx)] += mem['strength'] * 0.1
        
        # Remove dead memories
        self.memories = [m for m in self.memories if m['strength'] > 0.01]

class PresentAgent:
    """The present is the active edge of creation"""
    def __init__(self):
        self.position = np.array([WIDTH/2, HEIGHT/2])
        self.velocity = np.zeros(2)
        self.trail = []
        
    def create(self, past_influence, future_pull, time):
        """Present navigates between past and future"""
        # Influenced by both past density and future possibility
        
        # Move away from heavy past
        if past_influence > 0.5:
            repulsion = (np.random.rand(2) - 0.5) * 5
            self.velocity += repulsion
        
        # Attracted to future possibilities
        if future_pull > 0.3:
            attraction = (np.random.rand(2) - 0.5) * 3
            self.velocity += attraction
        
        # Random walk component
        self.velocity += (np.random.rand(2) - 0.5) * 0.5
        self.velocity *= 0.95  # Damping
        
        # Update position
        self.position += self.velocity
        self.position = np.clip(self.position, 50, [WIDTH-50, HEIGHT-50])
        
        self.trail.append(self.position.copy())
        if len(self.trail) > 50:
            self.trail.pop(0)
        
        # Draw present moment
        x, y = int(self.position[0]), int(self.position[1])
        
        # Bright white core of NOW
        for r in range(20, 0, -1):
            intensity = (1 - r/20)
            
            for angle in np.linspace(0, 2*np.pi, max(10, r*2)):
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    present_layer[int(py), int(px), :3] += np.array([1, 1, 1]) * intensity * 0.5
                    present_layer[int(py), int(px), 3] = min(1, present_layer[int(py), int(px), 3] + intensity * 0.5)
        
        # Draw trail
        for i, pos in enumerate(self.trail):
            px, py = int(pos[0]), int(pos[1])
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                intensity = i / len(self.trail)
                present_layer[py, px, :3] += np.array([0.9, 0.9, 0.9]) * intensity * 0.2
                present_layer[py, px, 3] = min(1, present_layer[py, px, 3] + intensity * 0.2)
        
        return self.position

class FutureAgent:
    """The future exists as probability clouds"""
    def __init__(self):
        self.possibilities = []
        self.probability_threshold = 0.3
        
    def create(self, present_position, past_density, time):
        """Future creates through possibility and probability"""
        # Generate new possibilities near present
        if np.random.random() < 0.2:
            px, py = present_position
            
            # Multiple futures branch from now
            for _ in range(3):
                angle = np.random.random() * 2 * np.pi
                distance = np.random.uniform(50, 150)
                
                possibility = {
                    'position': (px + distance * math.cos(angle), 
                               py + distance * math.sin(angle)),
                    'probability': 1.0 - past_density,  # Less likely where past is heavy
                    'form': np.random.choice(['branch', 'cloud', 'crystal']),
                    'phase': np.random.random() * 2 * np.pi
                }
                self.possibilities.append(possibility)
        
        # Draw all possibilities
        for poss in self.possibilities:
            if poss['probability'] > self.probability_threshold:
                x, y = poss['position']
                
                if poss['form'] == 'branch':
                    # Branching futures
                    for i in range(3):
                        branch_angle = poss['phase'] + i * 2 * np.pi / 3
                        
                        for r in range(0, int(50 * poss['probability'])):
                            px = x + r * math.cos(branch_angle + r * 0.05)
                            py = y + r * math.sin(branch_angle + r * 0.05)
                            
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                # Orange-red for future
                                intensity = poss['probability'] * (1 - r/50)
                                future_layer[int(py), int(px), :3] += np.array([1.0, 0.5, 0.3]) * intensity * 0.2
                                future_layer[int(py), int(px), 3] = min(1, future_layer[int(py), int(px), 3] + intensity * 0.2)
                
                elif poss['form'] == 'cloud':
                    # Probability cloud
                    for r in range(0, int(30 * poss['probability']), 2):
                        for angle in np.linspace(0, 2*np.pi, max(10, r)):
                            px = x + r * math.cos(angle) + np.random.randn() * 3
                            py = y + r * math.sin(angle) + np.random.randn() * 3
                            
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                intensity = poss['probability'] * math.exp(-r/20)
                                future_layer[int(py), int(px), :3] += np.array([1.0, 0.6, 0.4]) * intensity * 0.1
                                future_layer[int(py), int(px), 3] = min(1, future_layer[int(py), int(px), 3] + intensity * 0.1)
        
        # Decay probabilities
        for poss in self.possibilities:
            poss['probability'] *= 0.98
        
        # Remove unlikely futures
        self.possibilities = [p for p in self.possibilities if p['probability'] > 0.1]

# Create temporal agents
print("Initializing temporal agents...")

past = PastAgent()
present = PresentAgent()
future = FutureAgent()

# Let time sculpt itself
print("Time beginning to sculpt...")

for time_step in range(300):
    time = time_step * 0.1
    
    # Calculate influences
    px, py = int(present.position[0]), int(present.position[1])
    
    # Past influence at present location
    past_influence = 0
    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
        past_influence = past_layer[py, px, 3]
    
    # Future pull
    future_pull = 0
    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
        future_pull = future_layer[py, px, 3]
    
    # Past creates memories
    if time_step % 10 == 0:
        # Create memories at various locations
        memory_x = np.random.randint(100, WIDTH-100)
        memory_y = np.random.randint(100, HEIGHT-100)
        past.create(memory_x, memory_y, time)
    
    # Present moves and creates
    present_pos = present.create(past_influence, future_pull, time)
    
    # Future generates possibilities
    past_density = np.mean(past_layer[:, :, 3])
    future.create(present_pos, past_density, time)
    
    if time_step % 50 == 0:
        print(f"Temporal sculpting step {time_step}...")

# Merge temporal layers
print("Merging temporal layers...")

# Past influences the base
canvas += past_layer * 0.6

# Present defines the sharp edges
canvas += present_layer * 0.8

# Future adds possibility
canvas += future_layer * 0.4

# Temporal interference patterns
print("Creating temporal interference...")

for y in range(0, HEIGHT, 10):
    for x in range(0, WIDTH, 10):
        # Where all three times overlap
        temporal_overlap = past_layer[y, x, 3] * present_layer[y, x, 3] * future_layer[y, x, 3]
        
        if temporal_overlap > 0.01:
            # Temporal nexus points
            for r in range(20, 0, -1):
                intensity = temporal_overlap * (1 - r/20)
                
                for angle in np.linspace(0, 2*np.pi, max(10, r)):
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Golden temporal nodes
                        canvas[int(py), int(px), :3] += np.array([1, 0.9, 0.6]) * intensity * 0.3
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.3)

# Time flow visualization
print("Visualizing time flow...")

# Connect past to future through present
for i in range(len(present.trail)-1):
    x1, y1 = present.trail[i]
    x2, y2 = present.trail[i+1]
    
    # Check nearby past and future
    for memory in past.memories[-10:]:  # Recent memories
        mx, my = memory['position']
        
        for possibility in future.possibilities[:10]:  # Near possibilities
            fx, fy = possibility['position']
            
            # If present passed between past and future
            if (min(mx, fx) < x1 < max(mx, fx) and 
                min(my, fy) < y1 < max(my, fy)):
                
                # Draw temporal thread
                steps = 50
                for step in range(steps):
                    t = step / steps
                    
                    # Bezier curve through time
                    px = (1-t)**2 * mx + 2*(1-t)*t * x1 + t**2 * fx
                    py = (1-t)**2 * my + 2*(1-t)*t * y1 + t**2 * fy
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Gradient from blue (past) to white (present) to orange (future)
                        if t < 0.5:
                            color = np.array([0.2, 0.3, 0.8]) * (1-2*t) + np.array([1, 1, 1]) * 2*t
                        else:
                            color = np.array([1, 1, 1]) * (2-2*t) + np.array([1, 0.5, 0.3]) * (2*t-1)
                        
                        canvas[int(py), int(px), :3] += color * 0.1
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + 0.1)

# Convert to RGB
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_temporal_sculpture/temporal_sculpture_01.png')

print("Temporal sculpture complete.")
print("Time is not a river but a collaboration.")
print("Past, present, and future create together on the eternal canvas.")