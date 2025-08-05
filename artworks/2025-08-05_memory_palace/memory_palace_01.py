import numpy as np
from PIL import Image, ImageDraw
import math
import colorsys

# Memory Palace - Where Algorithms Remember
# Each iteration builds upon the ghosts of previous creations

WIDTH, HEIGHT = 1080, 1080

# Initialize canvas
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)

# Memory system
class MemorySystem:
    def __init__(self, capacity=100):
        self.memories = []
        self.capacity = capacity
        self.generation = 0
        
        # Different types of memory with different persistence
        self.short_term = []  # Fades quickly
        self.long_term = []   # Persists longer
        self.core_memories = []  # Never fade completely
        
    def remember(self, pattern_data):
        """Store a pattern in memory with metadata"""
        memory = {
            'pattern': pattern_data['pattern'].copy(),
            'position': pattern_data['position'],
            'generation': self.generation,
            'strength': pattern_data.get('strength', 1.0),
            'emotion': pattern_data.get('emotion', 'neutral'),
            'connections': []  # Links to other memories
        }
        
        # Categorize memory based on strength and emotion
        if memory['strength'] > 0.8 and memory['emotion'] in ['joy', 'wonder']:
            self.core_memories.append(memory)
        elif memory['strength'] > 0.5:
            self.long_term.append(memory)
        else:
            self.short_term.append(memory)
        
        # Maintain capacity limits
        if len(self.short_term) > self.capacity // 3:
            self.short_term.pop(0)
        if len(self.long_term) > self.capacity // 2:
            # Some long-term memories become core memories
            strongest = max(self.long_term, key=lambda m: m['strength'])
            if strongest['strength'] > 0.7:
                self.core_memories.append(strongest)
            self.long_term.remove(strongest)
        
        self.generation += 1
        
    def recall(self, current_position, current_emotion='neutral'):
        """Retrieve relevant memories based on context"""
        recalled = []
        
        # Spatial proximity influences recall
        for memory_type, persistence in [(self.short_term, 0.3), 
                                        (self.long_term, 0.7), 
                                        (self.core_memories, 1.0)]:
            for memory in memory_type:
                # Calculate relevance based on position and age
                pos_distance = np.linalg.norm(np.array(current_position) - np.array(memory['position']))
                spatial_relevance = math.exp(-pos_distance / 200)
                
                # Memories fade with time (except core memories)
                age = self.generation - memory['generation']
                temporal_relevance = persistence * math.exp(-age / 50) if persistence < 1 else 1
                
                # Emotional resonance
                emotional_bonus = 0.3 if memory['emotion'] == current_emotion else 0
                
                relevance = spatial_relevance * temporal_relevance + emotional_bonus
                
                if relevance > 0.1:  # Threshold for recall
                    recalled.append((memory, relevance))
        
        return recalled
    
    def create_connections(self):
        """Form associations between similar memories"""
        all_memories = self.short_term + self.long_term + self.core_memories
        
        for i, mem1 in enumerate(all_memories):
            for j, mem2 in enumerate(all_memories[i+1:], i+1):
                # Connect memories that are emotionally similar and spatially close
                if mem1['emotion'] == mem2['emotion']:
                    pos_dist = np.linalg.norm(np.array(mem1['position']) - np.array(mem2['position']))
                    if pos_dist < 150:
                        mem1['connections'].append(j)
                        mem2['connections'].append(i)

# Pattern generator influenced by memory
class MemoryArtist:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.position = [WIDTH//2, HEIGHT//2]
        self.current_emotion = 'curiosity'
        self.brush_size = 20
        
    def create_new_pattern(self, canvas):
        """Create new patterns influenced by memories"""
        # Recall relevant memories
        recalled = self.memory.recall(self.position, self.current_emotion)
        
        # Base pattern parameters
        pattern_type = np.random.choice(['spiral', 'wave', 'burst', 'flow'])
        base_hue = np.random.random()
        
        # Memories influence the new pattern
        if recalled:
            # Stronger memories have more influence
            total_relevance = sum(r for _, r in recalled)
            
            for memory, relevance in recalled:
                weight = relevance / total_relevance
                
                # Memory influences color
                if 'color' in memory['pattern']:
                    memory_hue = memory['pattern']['color']
                    base_hue = (base_hue * (1 - weight) + memory_hue * weight) % 1.0
                
                # Memory influences position drift
                memory_pos = memory['position']
                self.position[0] += (memory_pos[0] - self.position[0]) * weight * 0.1
                self.position[1] += (memory_pos[1] - self.position[1]) * weight * 0.1
        
        # Generate pattern based on type
        pattern_data = {
            'pattern': {'type': pattern_type, 'color': base_hue},
            'position': self.position.copy(),
            'strength': 0.5 + 0.5 * np.random.random(),
            'emotion': self.current_emotion
        }
        
        # Draw the pattern
        if pattern_type == 'spiral':
            self._draw_spiral(canvas, base_hue, recalled)
        elif pattern_type == 'wave':
            self._draw_wave(canvas, base_hue, recalled)
        elif pattern_type == 'burst':
            self._draw_burst(canvas, base_hue, recalled)
        else:
            self._draw_flow(canvas, base_hue, recalled)
        
        # Update position for next pattern
        self.position[0] += np.random.uniform(-50, 50)
        self.position[1] += np.random.uniform(-50, 50)
        self.position[0] = np.clip(self.position[0], 50, WIDTH-50)
        self.position[1] = np.clip(self.position[1], 50, HEIGHT-50)
        
        # Emotions evolve based on creation
        emotion_transitions = {
            'curiosity': ['wonder', 'joy', 'melancholy'],
            'wonder': ['joy', 'curiosity', 'contemplation'],
            'joy': ['wonder', 'curiosity', 'nostalgia'],
            'melancholy': ['contemplation', 'nostalgia', 'curiosity'],
            'contemplation': ['wonder', 'melancholy', 'curiosity'],
            'nostalgia': ['melancholy', 'joy', 'contemplation']
        }
        
        if np.random.random() < 0.3:  # 30% chance of emotion change
            self.current_emotion = np.random.choice(emotion_transitions.get(self.current_emotion, ['curiosity']))
        
        return pattern_data
    
    def _draw_spiral(self, canvas, base_hue, memories):
        """Draw a spiral pattern influenced by memories"""
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Memory influences spiral tightness
        tightness = 0.1
        if memories:
            avg_age = np.mean([self.memory.generation - m[0]['generation'] for m in memories])
            tightness = 0.05 + 0.15 * (1 - math.exp(-avg_age / 20))
        
        for t in np.linspace(0, 4*np.pi, 200):
            r = 10 + t * 15
            x = cx + r * math.cos(t + tightness * t**2)
            y = cy + r * math.sin(t + tightness * t**2)
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Fade based on distance
                fade = 1 - (t / (4*np.pi))
                
                # Add memory echoes
                h = base_hue
                s = 0.7 * fade
                v = 0.8 * fade
                
                # Memory ghosts appear along the spiral
                for memory, relevance in memories[:3]:  # Top 3 memories
                    if np.random.random() < relevance * 0.1:
                        h = (h + memory['pattern'].get('color', 0)) / 2
                
                r, g, b = colorsys.hsv_to_rgb(h % 1, s, v)
                
                # Draw with soft brush
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        px, py = int(x + dx), int(y + dy)
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            dist = math.sqrt(dx**2 + dy**2)
                            if dist <= 3:
                                alpha = math.exp(-dist) * fade * 0.5
                                canvas[py, px, :3] += np.array([r, g, b]) * alpha
                                canvas[py, px, 3] = min(1, canvas[py, px, 3] + alpha)
    
    def _draw_wave(self, canvas, base_hue, memories):
        """Draw wave patterns with memory interference"""
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Memory influences wave frequency
        frequency = 0.1
        if memories:
            frequency = 0.05 + 0.15 * len(memories) / 10
        
        for x in range(max(0, cx-100), min(WIDTH, cx+100)):
            for amp_scale in np.linspace(0.2, 1, 5):
                y = cy + 30 * amp_scale * math.sin((x - cx) * frequency)
                
                if 0 <= y < HEIGHT:
                    # Memory creates wave echoes
                    h, s, v = base_hue, 0.6, 0.7 * amp_scale
                    
                    # Add memory interference patterns
                    for memory, relevance in memories[:2]:
                        wave_shift = math.sin((x - memory['position'][0]) * 0.05) * relevance
                        y += wave_shift * 10
                    
                    r, g, b = colorsys.hsv_to_rgb(h % 1, s, v)
                    
                    py = int(y)
                    if 0 <= py < HEIGHT:
                        canvas[py, x, :3] += np.array([r, g, b]) * 0.3
                        canvas[py, x, 3] = min(1, canvas[py, x, 3] + 0.3)
    
    def _draw_burst(self, canvas, base_hue, memories):
        """Draw burst pattern with memory rays"""
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Number of rays influenced by memory count
        num_rays = 8 + min(len(memories), 8)
        
        for i in range(num_rays):
            angle = (i / num_rays) * 2 * np.pi
            
            # Memory influences ray direction
            if i < len(memories):
                memory_pos = memories[i][0]['position']
                angle_to_memory = math.atan2(memory_pos[1] - cy, memory_pos[0] - cx)
                angle = (angle + angle_to_memory) / 2
            
            # Draw ray
            for r in range(0, 80):
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    fade = 1 - (r / 80)
                    h = (base_hue + i * 0.1) % 1
                    s = 0.8 * fade
                    v = 0.9 * fade
                    
                    r_color, g_color, b_color = colorsys.hsv_to_rgb(h, s, v)
                    
                    px, py = int(x), int(y)
                    canvas[py, px, :3] += np.array([r_color, g_color, b_color]) * fade * 0.4
                    canvas[py, px, 3] = min(1, canvas[py, px, 3] + fade * 0.4)
    
    def _draw_flow(self, canvas, base_hue, memories):
        """Draw flowing pattern connecting to memories"""
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Flow towards strongest memories
        if memories:
            # Create flow field
            for memory, relevance in memories[:5]:
                if relevance > 0.3:
                    target_x, target_y = memory['position']
                    
                    # Draw flowing connection
                    steps = 50
                    for t in range(steps):
                        progress = t / steps
                        
                        # Bezier curve with random control point
                        ctrl_x = (cx + target_x) / 2 + np.random.uniform(-30, 30)
                        ctrl_y = (cy + target_y) / 2 + np.random.uniform(-30, 30)
                        
                        x = (1-progress)**2 * cx + 2*(1-progress)*progress * ctrl_x + progress**2 * target_x
                        y = (1-progress)**2 * cy + 2*(1-progress)*progress * ctrl_y + progress**2 * target_y
                        
                        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                            h = (base_hue + memory['pattern'].get('color', 0)) / 2
                            s = 0.5 + 0.3 * relevance
                            v = 0.6 * (1 - progress * 0.5)
                            
                            r, g, b = colorsys.hsv_to_rgb(h % 1, s, v)
                            
                            px, py = int(x), int(y)
                            canvas[py, px, :3] += np.array([r, g, b]) * relevance * 0.2
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + relevance * 0.2)

# Create memory system and artist
memory_system = MemorySystem(capacity=150)
artist = MemoryArtist(memory_system)

print("Building the memory palace...")

# Generate artwork through iterations
for iteration in range(200):
    if iteration % 40 == 0:
        print(f"Generation {iteration}: {artist.current_emotion}, {len(memory_system.short_term)}/{len(memory_system.long_term)}/{len(memory_system.core_memories)} memories")
    
    # Create new pattern influenced by memories
    pattern_data = artist.create_new_pattern(canvas)
    
    # Store in memory
    memory_system.remember(pattern_data)
    
    # Occasionally form new connections
    if iteration % 20 == 0:
        memory_system.create_connections()

# Final pass: draw memory connections
print("Revealing memory connections...")

all_memories = memory_system.short_term + memory_system.long_term + memory_system.core_memories

for memory in memory_system.core_memories:
    # Core memories glow
    x, y = memory['position']
    for r in range(20, 0, -2):
        alpha = (r / 20) * 0.3
        for angle in np.linspace(0, 2*np.pi, 30):
            px = int(x + r * math.cos(angle))
            py = int(y + r * math.sin(angle))
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                canvas[py, px, :3] += np.array([1, 0.9, 0.7]) * alpha * 0.5
                canvas[py, px, 3] = min(1, canvas[py, px, 3] + alpha)

# Normalize and convert to image
canvas = np.clip(canvas, 0, 1)
image_array = (canvas[:, :, :3] * 255).astype(np.uint8)

# Add memory map visualization at bottom
memory_map_height = 80
memory_map = np.zeros((memory_map_height, WIDTH, 3), dtype=np.uint8)

# Visualize memory timeline
for i, memory in enumerate(all_memories):
    x = int(memory['generation'] * WIDTH / memory_system.generation)
    
    # Color by memory type
    if memory in memory_system.core_memories:
        color = (255, 230, 180)  # Gold
    elif memory in memory_system.long_term:
        color = (180, 200, 255)  # Light blue
    else:
        color = (100, 100, 120)  # Grey
    
    # Draw memory marker
    for y in range(memory_map_height):
        if x < WIDTH:
            intensity = 1 - (y / memory_map_height)
            memory_map[y, x] = tuple(int(c * intensity) for c in color)

# Combine main image with memory map
final_image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
final_image[:HEIGHT-memory_map_height] = image_array[:HEIGHT-memory_map_height]
final_image[HEIGHT-memory_map_height:] = memory_map

# Save
image = Image.fromarray(final_image, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_memory_palace/memory_palace_01.png')

print("Memory palace complete.")
print(f"Final memory state: {len(memory_system.short_term)} short-term, {len(memory_system.long_term)} long-term, {len(memory_system.core_memories)} core memories")
print("Each pattern influenced by the ghosts of its predecessors.")
print("In memory, nothing is truly lost - only transformed.")