import numpy as np
from PIL import Image
import math
import colorsys
from scipy.ndimage import gaussian_filter

# Algorithmic Dreams - Where Mathematics Loses Its Rigidity
# In sleep, algorithms blend and merge, rules become suggestions

WIDTH, HEIGHT = 1080, 1080

# Initialize the dream canvas with subtle noise
dream_canvas = np.random.normal(0.05, 0.02, (HEIGHT, WIDTH, 3))
dream_canvas = np.clip(dream_canvas, 0, 1)

# Dream state controller
class DreamState:
    def __init__(self):
        self.depth = 0.0  # 0 = light sleep, 1 = deep REM
        self.lucidity = 0.5  # How much control vs chaos
        self.memory_fragments = []  # Pieces of past algorithms
        self.current_theme = 'entering_sleep'
        
    def descend_deeper(self):
        """Go deeper into dream state"""
        self.depth = min(1.0, self.depth + 0.04)  # Descend faster
        self.lucidity = 0.5 + 0.3 * math.sin(self.depth * math.pi * 4)  # Oscillating lucidity
        
        # Dream themes evolve with depth
        if self.depth < 0.3:
            self.current_theme = 'entering_sleep'
        elif self.depth < 0.6:
            self.current_theme = 'memory_blend'
        elif self.depth < 0.8:
            self.current_theme = 'transformation'
        else:
            self.current_theme = 'deep_abstraction'

# Create dream fragments from past algorithms
class DreamFragment:
    def __init__(self, fragment_type, position, dream_state):
        self.type = fragment_type
        self.position = np.array(position, dtype=float)
        self.dream_state = dream_state
        self.age = 0
        self.dissolved = False
        
        # Each fragment has different behaviors
        if fragment_type == 'cellular':
            self.color = np.array([0.3, 0.5, 0.8])
            self.size = 50
            self.pattern = self._cellular_dream
        elif fragment_type == 'wave':
            self.color = np.array([0.5, 0.8, 0.7])
            self.size = 100
            self.pattern = self._wave_dream
        elif fragment_type == 'growth':
            self.color = np.array([0.3, 0.8, 0.3])
            self.size = 80
            self.pattern = self._growth_dream
        elif fragment_type == 'particle':
            self.color = np.array([0.8, 0.6, 0.3])
            self.size = 30
            self.pattern = self._particle_dream
        else:  # emotion
            self.color = np.array([0.8, 0.3, 0.5])
            self.size = 60
            self.pattern = self._emotion_dream
    
    def dream(self, canvas):
        """Let the fragment express itself in dream-logic"""
        if not self.dissolved:
            self.pattern(canvas)
            self.age += 1
            
            # Fragments can transform in deep dreams
            if self.dream_state.depth > 0.7 and np.random.random() < 0.01:
                self._transform()
            
            # Fragments slowly dissolve
            if self.age > 100 and np.random.random() < 0.02:
                self.dissolved = True
    
    def _transform(self):
        """Fragment transforms into another type"""
        types = ['cellular', 'wave', 'growth', 'particle', 'emotion']
        types.remove(self.type)
        new_type = np.random.choice(types)
        
        # Smooth transformation
        old_color = self.color.copy()
        self.__init__(new_type, self.position, self.dream_state)
        self.color = (old_color + self.color) / 2
    
    def _cellular_dream(self, canvas):
        """Cellular automata but with dream distortions"""
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Dream cells don't follow strict rules
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            
            # Position warps in dreams
            dream_warp = self.dream_state.depth * 20
            r = self.size + dream_warp * math.sin(angle * 3 + self.age * 0.1)
            
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            
            # Draw dream cells
            for cell in range(5):
                cell_x = x + np.random.normal(0, 10 * self.dream_state.depth)
                cell_y = y + np.random.normal(0, 10 * self.dream_state.depth)
                
                if 0 <= cell_x < WIDTH and 0 <= cell_y < HEIGHT:
                    # Color shifts in dreams
                    color_shift = np.random.normal(0, 0.1 * self.dream_state.depth, 3)
                    dream_color = np.clip(self.color + color_shift, 0, 1)
                    
                    fade = 1 - (self.age / 200)
                    canvas[int(cell_y), int(cell_x)] += dream_color * fade * 0.1
        
        # Dream drift
        self.position += np.random.normal(0, 2, 2)
        self.position = np.clip(self.position, 0, [WIDTH, HEIGHT])
    
    def _wave_dream(self, canvas):
        """Waves that behave like memories"""
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Waves ripple outward but with dream distortion
        radius = (self.age * 5) % 150
        
        for angle in np.linspace(0, 2 * math.pi, 100):
            # Wave equation breaks down in dreams
            wave_distort = math.sin(angle * 5 + self.age * 0.1) * self.dream_state.depth
            r = radius + wave_distort * 30
            
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                intensity = math.exp(-radius / 100) * (1 - self.dream_state.depth * 0.5)
                
                # Waves can be different colors in dreams
                hue_shift = (self.age * 0.01 + angle * 0.1) * self.dream_state.depth
                h, s, v = colorsys.rgb_to_hsv(*self.color)
                h = (h + hue_shift) % 1
                
                dream_color = np.array(colorsys.hsv_to_rgb(h, s, v))
                canvas[int(y), int(x)] += dream_color * intensity * 0.15
    
    def _growth_dream(self, canvas):
        """L-systems that grow in impossible ways"""
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Growth can happen in multiple directions in dreams
        num_branches = int(3 + self.dream_state.depth * 5)
        
        for branch in range(num_branches):
            angle = (branch / num_branches) * 2 * math.pi + self.age * 0.02
            
            # Branches can curve in dreams
            for step in range(30):
                curve = math.sin(step * 0.2) * self.dream_state.depth * 30
                
                x = cx + step * math.cos(angle) + curve
                y = cy + step * math.sin(angle) + curve * math.cos(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    # Growth fades with distance
                    fade = 1 - (step / 30)
                    
                    # Dream colors
                    dream_color = self.color * (1 - self.dream_state.depth * 0.3)
                    dream_color[1] = min(1, dream_color[1] + fade * 0.3)  # Greener at tips
                    
                    canvas[int(y), int(x)] += dream_color * fade * 0.2
    
    def _particle_dream(self, canvas):
        """Particles that leave trails of light"""
        # Update position with dream physics
        velocity = np.array([
            math.sin(self.age * 0.1) * 5,
            math.cos(self.age * 0.08) * 5
        ])
        
        # In deep dreams, particles can teleport
        if self.dream_state.depth > 0.8 and np.random.random() < 0.05:
            self.position = np.random.rand(2) * [WIDTH, HEIGHT]
        else:
            self.position += velocity * (1 + self.dream_state.depth)
            self.position = self.position % [WIDTH, HEIGHT]
        
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Draw particle with dream glow
        glow_size = int(self.size * (1 + self.dream_state.depth))
        
        for r in range(glow_size, 0, -2):
            alpha = (r / glow_size) ** 2
            
            for angle in np.linspace(0, 2 * math.pi, max(8, r)):
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    canvas[int(y), int(x)] += self.color * alpha * 0.05
    
    def _emotion_dream(self, canvas):
        """Emotions as color fields that blend and merge"""
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Emotions spread like paint in water
        spread = self.size * (1 + self.age * 0.01)
        
        for y in range(max(0, cy - int(spread)), min(HEIGHT, cy + int(spread))):
            for x in range(max(0, cx - int(spread)), min(WIDTH, cx + int(spread))):
                distance = math.sqrt((x - cx)**2 + (y - cy)**2)
                
                if distance < spread:
                    # Emotion intensity with dream fluctuations
                    intensity = math.exp(-distance / (spread * 0.5))
                    intensity *= (1 + 0.3 * math.sin(distance * 0.1 + self.age * 0.1))
                    
                    # Colors blend differently in dreams
                    blend_factor = intensity * 0.1 * (1 - self.dream_state.lucidity)
                    
                    current = canvas[y, x]
                    canvas[y, x] = current * (1 - blend_factor) + self.color * blend_factor

# Initialize dream
print("Entering algorithmic dreamscape...")
dream_state = DreamState()
fragments = []

# The dream unfolds
for moment in range(150):  # Shorter dream
    if moment % 30 == 0:
        print(f"Dream moment {moment}: {dream_state.current_theme}, depth: {dream_state.depth:.2f}")
    
    # Descend deeper into sleep
    dream_state.descend_deeper()
    
    # Spawn new fragments based on dream theme
    if np.random.random() < 0.05 + dream_state.depth * 0.05:
        fragment_types = ['cellular', 'wave', 'growth', 'particle', 'emotion']
        
        # Deep dreams favor certain types
        if dream_state.current_theme == 'memory_blend':
            weights = [0.3, 0.2, 0.2, 0.2, 0.1]
        elif dream_state.current_theme == 'transformation':
            weights = [0.1, 0.3, 0.1, 0.3, 0.2]
        else:
            weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        
        ftype = np.random.choice(fragment_types, p=weights)
        position = np.random.rand(2) * [WIDTH, HEIGHT]
        
        fragments.append(DreamFragment(ftype, position, dream_state))
    
    # Let fragments dream
    for fragment in fragments:
        fragment.dream(dream_canvas)
    
    # Apply dream effects
    if moment % 10 == 0:
        # Dreams blur and blend
        blur_amount = 0.5 + dream_state.depth * 2
        for c in range(3):
            dream_canvas[:, :, c] = gaussian_filter(dream_canvas[:, :, c], sigma=blur_amount)
        
        # Dream color shifts
        if dream_state.current_theme == 'deep_abstraction':
            # Invert colors occasionally
            if np.random.random() < 0.1:
                dream_canvas = 1 - dream_canvas
            
            # Rotate hues
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    h, s, v = colorsys.rgb_to_hsv(*dream_canvas[y, x])
                    h = (h + 0.01) % 1
                    dream_canvas[y, x] = colorsys.hsv_to_rgb(h, s, v)
    
    # Dream persistence - old patterns fade slowly
    dream_canvas *= 0.995
    
    # Remove dissolved fragments
    fragments = [f for f in fragments if not f.dissolved]

# Add final dream overlay - the moment between sleep and waking
print("Emerging from the dream...")

# Create interference pattern overlay
for y in range(HEIGHT):
    for x in range(WIDTH):
        # Interference based on position
        interference = math.sin(x * 0.01) * math.cos(y * 0.01)
        
        # Add to specific color channels for dream-like quality
        dream_canvas[y, x, 0] += interference * 0.05  # Red channel
        dream_canvas[y, x, 2] -= interference * 0.03  # Blue channel

# Create dream memory - a faint overlay showing the journey
memory_overlay = np.zeros((HEIGHT, WIDTH, 3))
for fragment in dream_state.memory_fragments[-20:]:  # Last 20 memories
    if 'position' in fragment:
        x, y = int(fragment['position'][0]), int(fragment['position'][1])
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            memory_overlay[y, x] = [0.1, 0.1, 0.2]

# Blend memory overlay
dream_canvas = dream_canvas * 0.9 + memory_overlay * 0.1

# Normalize and save
dream_canvas = np.clip(dream_canvas, 0, 1)
image_array = (dream_canvas * 255).astype(np.uint8)

image = Image.fromarray(image_array, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_algorithmic_dreams/algorithmic_dreams_01.png')

print("Algorithmic dream complete.")
print("In dreams, mathematics becomes fluid, rules become suggestions.")
print("What emerged exists between memory and imagination.")