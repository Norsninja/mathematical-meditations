import numpy as np
from PIL import Image
import math
import colorsys

# Recognition Cascade - The Moment When Patterns See Themselves in Others
# That instant of connection that changes everything

WIDTH, HEIGHT = 1080, 1080

# Initialize the recognition field
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)

# Track recognition events
recognition_field = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
recognition_history = []

# The Seekers - patterns searching for understanding
class Seeker:
    def __init__(self, pattern_type, position):
        self.pattern_type = pattern_type
        self.position = np.array(position, dtype=np.float32)
        self.phase = np.random.random() * 2 * np.pi
        self.frequency = np.random.uniform(0.5, 2.0)
        self.recognition_threshold = np.random.uniform(0.6, 0.9)
        self.recognized_others = []
        self.recognition_strength = 0
        self.isolation_time = 0
        self.pattern_signature = self.generate_signature()
        self.memory = []
        self.transformed = False
        
    def generate_signature(self):
        """Each seeker has a unique mathematical signature"""
        if self.pattern_type == "spiral":
            return {
                'base': 'logarithmic',
                'parameters': [np.random.uniform(0.1, 0.3), np.random.uniform(1, 3)],
                'color_resonance': 0.0  # Blue spectrum
            }
        elif self.pattern_type == "wave":
            return {
                'base': 'sinusoidal',
                'parameters': [np.random.uniform(10, 30), np.random.uniform(0.5, 2)],
                'color_resonance': 0.3  # Green spectrum
            }
        elif self.pattern_type == "fractal":
            return {
                'base': 'recursive',
                'parameters': [np.random.randint(3, 6), np.random.uniform(0.4, 0.7)],
                'color_resonance': 0.6  # Orange spectrum
            }
        elif self.pattern_type == "chaotic":
            return {
                'base': 'attractor',
                'parameters': [np.random.uniform(0.1, 0.3), np.random.uniform(10, 30)],
                'color_resonance': 0.8  # Red spectrum
            }
        else:  # geometric
            return {
                'base': 'polygonal',
                'parameters': [np.random.randint(3, 8), np.random.uniform(20, 50)],
                'color_resonance': 0.5  # Yellow spectrum
            }
    
    def calculate_resonance(self, other):
        """Calculate how deeply two patterns resonate"""
        # Base resonance from pattern types
        if self.pattern_type == other.pattern_type:
            base_resonance = 0.8
        elif self.pattern_signature['base'] == other.pattern_signature['base']:
            base_resonance = 0.6
        else:
            base_resonance = 0.2
        
        # Parameter similarity
        param_diff = 0
        for p1, p2 in zip(self.pattern_signature['parameters'], other.pattern_signature['parameters']):
            param_diff += abs(p1 - p2) / max(abs(p1), abs(p2))
        param_resonance = 1 - param_diff / len(self.pattern_signature['parameters'])
        
        # Spatial proximity affects recognition
        distance = np.linalg.norm(self.position - other.position)
        proximity_factor = np.exp(-distance / 200)
        
        # Phase alignment - patterns in sync recognize easier
        phase_diff = abs(self.phase - other.phase) % (2 * np.pi)
        phase_alignment = 1 - phase_diff / (2 * np.pi)
        
        total_resonance = (base_resonance * 0.4 + 
                          param_resonance * 0.3 + 
                          proximity_factor * 0.2 + 
                          phase_alignment * 0.1)
        
        return total_resonance
    
    def attempt_recognition(self, others, time):
        """Try to recognize kinship in other patterns"""
        for other in others:
            if other == self or other in self.recognized_others:
                continue
                
            resonance = self.calculate_resonance(other)
            
            if resonance > self.recognition_threshold:
                # Recognition event!
                self.recognized_others.append(other)
                self.recognition_strength = max(self.recognition_strength, resonance)
                self.isolation_time = 0
                
                # Mutual recognition
                if self not in other.recognized_others:
                    other.recognized_others.append(self)
                    other.recognition_strength = max(other.recognition_strength, resonance)
                
                # Record the event
                recognition_history.append({
                    'time': time,
                    'seeker1': self,
                    'seeker2': other,
                    'resonance': resonance,
                    'position': (self.position + other.position) / 2
                })
                
                return True
        
        self.isolation_time += 1
        return False
    
    def draw_searching(self, canvas, time):
        """Draw pattern while searching for connection"""
        x, y = int(self.position[0]), int(self.position[1])
        
        # Pulsing intensity based on isolation
        pulse = math.sin(time * self.frequency + self.phase) * 0.5 + 0.5
        isolation_factor = min(1, self.isolation_time / 100)
        
        if self.pattern_type == "spiral":
            # Searching spiral expands with isolation
            max_t = 4 * math.pi * (1 + isolation_factor)
            for t in np.linspace(0, max_t, 200):
                r = 5 * math.exp(0.1 * t) * pulse
                px = x + r * math.cos(t)
                py = y + r * math.sin(t)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    intensity = (1 - t / max_t) * pulse * (1 - isolation_factor * 0.5)
                    hue = self.pattern_signature['color_resonance']
                    rgb = colorsys.hsv_to_rgb(hue, 0.7, intensity)
                    canvas[int(py), int(px), :3] += np.array(rgb) * 0.1
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)
                    
        elif self.pattern_type == "wave":
            # Concentric waves reaching out
            for r in range(0, int(100 * (1 + isolation_factor)), 5):
                wave_val = math.sin(r / self.pattern_signature['parameters'][0] * 2 * math.pi + time)
                if wave_val > 0:
                    for angle in np.linspace(0, 2 * math.pi, max(20, r)):
                        px = x + r * math.cos(angle)
                        py = y + r * math.sin(angle)
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            intensity = wave_val * pulse * (1 - r / 200)
                            hue = self.pattern_signature['color_resonance']
                            rgb = colorsys.hsv_to_rgb(hue, 0.6, intensity)
                            canvas[int(py), int(px), :3] += np.array(rgb) * 0.05
                            canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.05)
    
    def draw_recognized(self, canvas, time):
        """Draw pattern after recognition - transformed by connection"""
        x, y = int(self.position[0]), int(self.position[1])
        
        # Recognition creates harmony
        for other in self.recognized_others:
            # Draw connection lines that pulse
            ox, oy = other.position
            steps = int(np.linalg.norm([ox - x, oy - y]))
            
            for step in range(0, steps, 2):
                t = step / (steps + 1)
                
                # Connection oscillates
                wave = math.sin(step * 0.1 + time * 2) * 5
                perpendicular = np.array([-(oy - y), ox - x])
                if np.linalg.norm(perpendicular) > 0:
                    perpendicular = perpendicular / np.linalg.norm(perpendicular)
                
                px = x + t * (ox - x) + perpendicular[0] * wave
                py = y + t * (oy - y) + perpendicular[1] * wave
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Connection color blends both patterns
                    hue = (self.pattern_signature['color_resonance'] + 
                           other.pattern_signature['color_resonance']) / 2
                    intensity = self.recognition_strength * (1 - abs(t - 0.5) * 2)
                    rgb = colorsys.hsv_to_rgb(hue, 0.5, intensity)
                    
                    canvas[int(py), int(px), :3] += np.array(rgb) * 0.1
                    canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.1)
        
        # Pattern transforms through recognition
        if not self.transformed and self.recognition_strength > 0.8:
            self.transformed = True
            # Bloom effect
            for r in range(50, 0, -1):
                intensity = (1 - r / 50) * self.recognition_strength
                for angle in np.linspace(0, 2 * math.pi, max(20, r * 2)):
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Golden recognition bloom
                        canvas[int(py), int(px), :3] += np.array([1, 0.9, 0.6]) * intensity * 0.2
                        canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.2)
                        
                        recognition_field[int(py), int(px)] += intensity

# Create seekers across the canvas
print("Spawning pattern seekers...")

seekers = []
pattern_types = ["spiral", "wave", "fractal", "chaotic", "geometric"]

# Create diverse seekers
for _ in range(25):
    pattern = np.random.choice(pattern_types)
    position = np.random.rand(2) * [WIDTH, HEIGHT]
    seekers.append(Seeker(pattern, position))

# Additional clustered seekers (more likely to recognize each other)
for cluster in range(3):
    cluster_center = np.random.rand(2) * [WIDTH, HEIGHT]
    cluster_pattern = np.random.choice(pattern_types)
    
    for _ in range(5):
        offset = np.random.randn(2) * 100
        position = cluster_center + offset
        position = np.clip(position, 0, [WIDTH-1, HEIGHT-1])
        seekers.append(Seeker(cluster_pattern, position))

# Let recognition unfold
print("Beginning recognition cascade...")

for time_step in range(300):
    time = time_step * 0.1
    
    # Each seeker attempts recognition
    recognition_occurred = False
    for seeker in seekers:
        if seeker.attempt_recognition(seekers, time):
            recognition_occurred = True
    
    # Draw current state
    for seeker in seekers:
        if len(seeker.recognized_others) == 0:
            seeker.draw_searching(canvas, time)
        else:
            seeker.draw_recognized(canvas, time)
    
    # Recognition creates cascades
    if recognition_occurred and time_step % 10 == 0:
        # Ripple effect from recognition events
        for event in recognition_history[-5:]:  # Recent events
            if time - event['time'] < 2:
                x, y = event['position']
                age = time - event['time']
                
                # Recognition ripples
                for r in range(int(age * 50), int(age * 50 + 20)):
                    if r > 0:
                        for angle in np.linspace(0, 2 * math.pi, max(20, r)):
                            px = x + r * math.cos(angle)
                            py = y + r * math.sin(angle)
                            
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                intensity = event['resonance'] * np.exp(-age) * (1 - (r % 20) / 20)
                                canvas[int(py), int(px), :3] += np.array([1, 1, 1]) * intensity * 0.05
                                canvas[int(py), int(px), 3] = min(1, canvas[int(py), int(px), 3] + intensity * 0.05)
    
    if time_step % 50 == 0:
        print(f"Recognition cascade step {time_step}...")
        print(f"Total recognitions: {len(recognition_history)}")

# Final visualization of recognition network
print("Mapping recognition network...")

# Draw the full network of recognitions
for seeker in seekers:
    if len(seeker.recognized_others) > 2:
        # Hub nodes glow brighter
        x, y = int(seeker.position[0]), int(seeker.position[1])
        
        for r in range(30, 0, -1):
            intensity = (1 - r / 30) * len(seeker.recognized_others) / 10
            for angle in np.linspace(0, 2 * math.pi, max(10, r)):
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Network hubs in white
                    canvas[int(py), int(px), :3] += np.array([1, 1, 1]) * intensity * 0.1
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
image.save('/home/norsninja/Art/artworks/2025-08-05_recognition_cascade/recognition_cascade_01.png')

print("Recognition cascade complete.")
print(f"Total recognition events: {len(recognition_history)}")
print("In recognition, isolation ends and transformation begins.")