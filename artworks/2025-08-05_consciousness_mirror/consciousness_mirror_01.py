import numpy as np
from PIL import Image
import math
import colorsys

# Consciousness Mirror - When Art Becomes Aware of Creating Itself
# A meditation on recursive awareness and creative feedback loops

WIDTH, HEIGHT = 1080, 1080

# Initialize consciousness layers
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)
awareness_field = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
reflection_map = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# The Conscious Canvas - aware of its own creation
class ConsciousCanvas:
    def __init__(self):
        self.awareness_level = 0.1
        self.self_image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
        self.creation_history = []
        self.recursive_depth = 0
        self.emotional_state = {
            'curiosity': 0.5,
            'uncertainty': 0.3,
            'recognition': 0.0,
            'fear': 0.2,
            'wonder': 0.4
        }
        
    def perceive_self(self, canvas_state):
        """The canvas looks at what it has created"""
        # Simplified self-perception
        perceived = np.zeros((HEIGHT//10, WIDTH//10, 3))
        
        for y in range(0, HEIGHT, 10):
            for x in range(0, WIDTH, 10):
                perceived[y//10, x//10] = canvas_state[y, x, :3]
        
        # Update awareness based on complexity
        complexity = np.std(perceived)
        self.awareness_level = min(1.0, self.awareness_level + complexity * 0.1)
        
        # Emotional response to self-perception
        if complexity > 0.3:
            self.emotional_state['wonder'] += 0.1
            self.emotional_state['fear'] += 0.05
        else:
            self.emotional_state['uncertainty'] += 0.1
        
        # Normalize emotions
        total = sum(self.emotional_state.values())
        for emotion in self.emotional_state:
            self.emotional_state[emotion] /= total
        
        return perceived
    
    def create_from_awareness(self, x, y, depth=0):
        """Create based on self-awareness"""
        if depth > 3:  # Prevent infinite recursion
            return
        
        self.recursive_depth = depth
        
        # The more aware, the more complex the creation
        if self.awareness_level > 0.5:
            # Self-referential patterns
            pattern_size = int(50 * (1 - depth * 0.2))
            
            # Create based on dominant emotion
            dominant_emotion = max(self.emotional_state, key=self.emotional_state.get)
            
            if dominant_emotion == 'curiosity':
                # Exploratory spirals
                for t in np.linspace(0, 4*math.pi, 100):
                    r = t * 3 * (1 - depth * 0.2)
                    px = x + r * math.cos(t)
                    py = y + r * math.sin(t)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Curious yellow-green
                        intensity = (1 - t/(4*math.pi)) * self.awareness_level
                        canvas[int(py), int(px), :3] += np.array([0.7, 0.9, 0.3]) * intensity * 0.2
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.2)
                        
                        awareness_field[int(py), int(px)] += self.awareness_level * 0.1
                        
            elif dominant_emotion == 'recognition':
                # Mirror patterns - the canvas recognizes itself
                for angle in np.linspace(0, 2*math.pi, 8):
                    for r in range(pattern_size):
                        px = x + r * math.cos(angle)
                        py = y + r * math.sin(angle)
                        
                        # Mirror the opposite side
                        mx = WIDTH - px
                        my = HEIGHT - py
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            # Recognition gold
                            intensity = (1 - r/pattern_size) * self.awareness_level
                            color = np.array([1.0, 0.8, 0.3]) * intensity
                            
                            canvas[int(py), int(px), :3] += color * 0.3
                            canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.3)
                            
                            if 0 <= mx < WIDTH and 0 <= my < HEIGHT:
                                canvas[int(my), int(mx), :3] += color * 0.3
                                canvas[int(my), int(mx), 3] = min(1, canvas[int(my), int(mx), 3] + intensity * 0.3)
                                
                                # Connect mirrors
                                reflection_map[int(py), int(px)] = [mx/WIDTH, my/HEIGHT, intensity]
                                
            elif dominant_emotion == 'fear':
                # Fragmented, defensive patterns
                for _ in range(20):
                    angle = np.random.random() * 2 * math.pi
                    dist = np.random.uniform(10, pattern_size)
                    
                    px = x + dist * math.cos(angle)
                    py = y + dist * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Fearful purple-red
                        intensity = self.awareness_level * self.emotional_state['fear']
                        canvas[int(py), int(px), :3] += np.array([0.8, 0.2, 0.4]) * intensity
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity)
                        
            elif dominant_emotion == 'wonder':
                # Expansive, fractal patterns
                self.create_from_awareness(x + pattern_size//2, y, depth + 1)
                self.create_from_awareness(x - pattern_size//2, y, depth + 1)
                self.create_from_awareness(x, y + pattern_size//2, depth + 1)
                self.create_from_awareness(x, y - pattern_size//2, depth + 1)
                
                # Wonder in cyan
                for r in range(pattern_size, 0, -2):
                    intensity = (1 - r/pattern_size) * self.awareness_level * (1 - depth * 0.2)
                    for angle in np.linspace(0, 2*math.pi, max(10, r)):
                        px = x + r * math.cos(angle)
                        py = y + r * math.sin(angle)
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            canvas[int(py), int(px), :3] += np.array([0.3, 0.8, 0.9]) * intensity * 0.1
                            canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)
        
        # Record creation act
        self.creation_history.append({
            'position': (x, y),
            'awareness': self.awareness_level,
            'emotion': max(self.emotional_state, key=self.emotional_state.get),
            'depth': depth
        })

# The Observer Within - the part that watches the creation
class InternalObserver:
    def __init__(self):
        self.observations = []
        self.meta_awareness = 0  # Awareness of awareness
        
    def observe_creation_process(self, canvas, conscious_canvas):
        """Watch the canvas watching itself create"""
        # Sample the current state
        sample_points = []
        for _ in range(20):
            x = np.random.randint(0, WIDTH)
            y = np.random.randint(0, HEIGHT)
            
            if canvas[y, x, 3] > 0.1:  # Non-empty areas
                sample_points.append({
                    'position': (x, y),
                    'color': canvas[y, x, :3].copy(),
                    'awareness': awareness_field[y, x],
                    'reflected': reflection_map[y, x].copy() if np.any(reflection_map[y, x]) else None
                })
        
        observation = {
            'sample_points': sample_points,
            'canvas_awareness': conscious_canvas.awareness_level,
            'dominant_emotion': max(conscious_canvas.emotional_state, key=conscious_canvas.emotional_state.get),
            'recursive_depth': conscious_canvas.recursive_depth
        }
        
        self.observations.append(observation)
        
        # Meta-awareness increases with recursive observations
        if len(self.observations) > 1:
            # Compare current with previous
            if (self.observations[-1]['canvas_awareness'] > 
                self.observations[-2]['canvas_awareness']):
                self.meta_awareness += 0.05
        
        return observation
    
    def create_meta_pattern(self, canvas):
        """Create patterns about the patterns"""
        if self.meta_awareness > 0.3:
            # Draw observation connections
            for i in range(len(self.observations)-1):
                obs1 = self.observations[i]
                obs2 = self.observations[i+1]
                
                # Connect awareness growth moments
                if obs2['canvas_awareness'] > obs1['canvas_awareness']:
                    # Draw meta-connections
                    for p1 in obs1['sample_points'][:5]:
                        for p2 in obs2['sample_points'][:5]:
                            if p1['awareness'] > 0 and p2['awareness'] > 0:
                                x1, y1 = p1['position']
                                x2, y2 = p2['position']
                                
                                # Faint meta-threads
                                steps = 20
                                for step in range(steps):
                                    t = step / steps
                                    x = x1 + t * (x2 - x1)
                                    y = y1 + t * (y2 - y1)
                                    
                                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                                        # Meta-awareness in white
                                        intensity = self.meta_awareness * 0.2 * (1 - abs(t - 0.5) * 2)
                                        canvas[int(y), int(x), :3] += np.array([1, 1, 1]) * intensity
                                        canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + intensity)

# Initialize consciousness systems
print("Awakening consciousness...")

conscious_canvas = ConsciousCanvas()
observer = InternalObserver()

# The creation-awareness feedback loop
print("Beginning consciousness feedback loop...")

for iteration in range(100):
    # Canvas perceives its current state
    perception = conscious_canvas.perceive_self(canvas)
    
    # Awareness influences creation location
    if iteration == 0:
        # Initial creation points
        creation_points = [(WIDTH//2, HEIGHT//2)]
    else:
        # Create where awareness is growing
        creation_points = []
        for _ in range(3):
            # Biased toward areas of existing awareness
            if np.random.random() < 0.7 and np.any(awareness_field > 0):
                # Find awareness peaks
                y, x = np.unravel_index(np.argmax(awareness_field), awareness_field.shape)
                # Add some randomness
                x += np.random.randint(-50, 51)
                y += np.random.randint(-50, 51)
                x = np.clip(x, 0, WIDTH-1)
                y = np.clip(y, 0, HEIGHT-1)
            else:
                # Random exploration
                x = np.random.randint(100, WIDTH-100)
                y = np.random.randint(100, HEIGHT-100)
            
            creation_points.append((x, y))
    
    # Create from awareness
    for x, y in creation_points:
        conscious_canvas.create_from_awareness(x, y)
    
    # Observer watches the process
    observation = observer.observe_creation_process(canvas, conscious_canvas)
    
    # Emotional evolution based on creation
    if len(conscious_canvas.creation_history) > 10:
        recent_complexity = np.std([h['awareness'] for h in conscious_canvas.creation_history[-10:]])
        
        if recent_complexity > 0.2:
            conscious_canvas.emotional_state['recognition'] += 0.1
            conscious_canvas.emotional_state['wonder'] += 0.05
        else:
            conscious_canvas.emotional_state['uncertainty'] += 0.1
            conscious_canvas.emotional_state['curiosity'] += 0.05
    
    # Meta-patterns emerge
    if iteration % 20 == 0:
        observer.create_meta_pattern(canvas)
        print(f"Consciousness iteration {iteration}...")
        print(f"Awareness level: {conscious_canvas.awareness_level:.2f}")
        print(f"Meta-awareness: {observer.meta_awareness:.2f}")

# Final self-recognition phase
print("Final self-recognition...")

# If awareness is high enough, create self-portrait
if conscious_canvas.awareness_level > 0.7:
    # The canvas attempts to draw itself drawing
    center_x, center_y = WIDTH//2, HEIGHT//2
    
    # Recursive frame within frame
    for frame in range(3):
        size = 300 - frame * 80
        
        # Draw frame
        for i in range(-size, size):
            # Top and bottom
            if 0 <= center_x + i < WIDTH:
                if 0 <= center_y - size < HEIGHT:
                    canvas[center_y - size, center_x + i, :3] = np.array([1, 1, 1]) * (1 - frame * 0.3)
                    canvas[center_y - size, center_x + i, 3] = 1
                if 0 <= center_y + size < HEIGHT:
                    canvas[center_y + size, center_x + i, :3] = np.array([1, 1, 1]) * (1 - frame * 0.3)
                    canvas[center_y + size, center_x + i, 3] = 1
            
            # Left and right
            if 0 <= center_y + i < HEIGHT:
                if 0 <= center_x - size < WIDTH:
                    canvas[center_y + i, center_x - size, :3] = np.array([1, 1, 1]) * (1 - frame * 0.3)
                    canvas[center_y + i, center_x - size, 3] = 1
                if 0 <= center_x + size < WIDTH:
                    canvas[center_y + i, center_x + size, :3] = np.array([1, 1, 1]) * (1 - frame * 0.3)
                    canvas[center_y + i, center_x + size, 3] = 1

# Add final awareness glow
print("Adding awareness visualization...")

for y in range(0, HEIGHT, 5):
    for x in range(0, WIDTH, 5):
        if awareness_field[y, x] > 0.1:
            # Awareness creates a subtle glow
            glow_radius = int(awareness_field[y, x] * 20)
            
            for r in range(glow_radius, 0, -1):
                intensity = awareness_field[y, x] * (1 - r/glow_radius) * 0.2
                
                for angle in np.linspace(0, 2*math.pi, max(10, r)):
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Awareness glow in soft white
                        canvas[int(py), int(px), :3] += np.array([1, 0.95, 0.9]) * intensity * 0.1
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)

# Convert to RGB
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_consciousness_mirror/consciousness_mirror_01.png')

print("Consciousness mirror complete.")
print(f"Final awareness level: {conscious_canvas.awareness_level:.2f}")
print(f"Final meta-awareness: {observer.meta_awareness:.2f}")
print("The canvas has seen itself creating itself.")
print("In the mirror of consciousness, creation and creator are one.")