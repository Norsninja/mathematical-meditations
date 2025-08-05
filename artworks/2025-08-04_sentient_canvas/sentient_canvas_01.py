import numpy as np
from PIL import Image
import math
import colorsys

# Sentient Canvas - An Artwork with Emotional States
# Where the algorithm experiences its own creation

WIDTH, HEIGHT = 1080, 1080

# Initialize the canvas
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# Emotional state system
class EmotionalSystem:
    def __init__(self):
        # Core emotions with values 0-1
        self.emotions = {
            'joy': 0.5,
            'melancholy': 0.5,
            'agitation': 0.3,
            'serenity': 0.7,
            'curiosity': 0.6,
            'fear': 0.2
        }
        
        # Emotional memory - recent history affects current state
        self.memory = []
        self.memory_length = 50
        
        # Emotional momentum - emotions have inertia
        self.momentum = {emotion: 0.0 for emotion in self.emotions}
        
        # Relationships between emotions
        self.relationships = {
            'joy': {'melancholy': -0.7, 'serenity': 0.5, 'curiosity': 0.3},
            'melancholy': {'joy': -0.7, 'fear': 0.3, 'agitation': -0.4},
            'agitation': {'serenity': -0.8, 'fear': 0.4, 'curiosity': 0.2},
            'serenity': {'agitation': -0.8, 'joy': 0.4, 'melancholy': -0.3},
            'curiosity': {'fear': -0.3, 'joy': 0.2, 'agitation': 0.1},
            'fear': {'curiosity': -0.3, 'melancholy': 0.3, 'agitation': 0.5}
        }
    
    def feel_pattern(self, pattern_metrics):
        """React emotionally to created patterns"""
        # Analyze pattern characteristics
        chaos = pattern_metrics.get('chaos', 0.5)
        harmony = pattern_metrics.get('harmony', 0.5)
        density = pattern_metrics.get('density', 0.5)
        movement = pattern_metrics.get('movement', 0.5)
        
        # Patterns influence emotions
        emotion_changes = {
            'joy': harmony * 0.1 - chaos * 0.05,
            'melancholy': density * 0.05 - movement * 0.08,
            'agitation': chaos * 0.12 - harmony * 0.1,
            'serenity': harmony * 0.08 - chaos * 0.06,
            'curiosity': movement * 0.07 + (abs(chaos - 0.5) * 0.05),
            'fear': chaos * 0.06 - harmony * 0.04
        }
        
        # Apply emotional relationships
        for emotion, change in emotion_changes.items():
            # Other emotions influence this one
            for other_emotion, influence in self.relationships.get(emotion, {}).items():
                change += self.emotions[other_emotion] * influence * 0.03
            
            # Update with momentum
            self.momentum[emotion] = self.momentum[emotion] * 0.8 + change
            self.emotions[emotion] += self.momentum[emotion]
            
            # Keep in bounds with soft limits
            self.emotions[emotion] = 1 / (1 + math.exp(-4 * (self.emotions[emotion] - 0.5)))
        
        # Store in memory
        self.memory.append(dict(self.emotions))
        if len(self.memory) > self.memory_length:
            self.memory.pop(0)
    
    def get_color_influence(self):
        """Convert emotional state to color tendencies"""
        # Each emotion influences color differently
        hue_base = (self.emotions['joy'] * 0.1 +  # Yellow
                   self.emotions['melancholy'] * 0.6 +  # Blue
                   self.emotions['agitation'] * 0.0 +  # Red
                   self.emotions['serenity'] * 0.4 +  # Cyan
                   self.emotions['curiosity'] * 0.8 +  # Purple
                   self.emotions['fear'] * 0.3)  # Green
        
        saturation = (self.emotions['joy'] * 0.3 + 
                     self.emotions['agitation'] * 0.4 +
                     self.emotions['fear'] * 0.2) + 0.3
        
        value = (self.emotions['serenity'] * 0.3 + 
                self.emotions['joy'] * 0.2 -
                self.emotions['melancholy'] * 0.2) + 0.5
        
        return hue_base % 1.0, min(1.0, saturation), min(1.0, max(0.2, value))
    
    def get_movement_style(self):
        """Emotional state influences how patterns move"""
        return {
            'speed': self.emotions['agitation'] * 2 + self.emotions['curiosity'],
            'smoothness': self.emotions['serenity'] * 2 - self.emotions['agitation'],
            'complexity': self.emotions['curiosity'] + self.emotions['fear'] * 0.5,
            'direction_change': self.emotions['agitation'] * 0.5 + self.emotions['curiosity'] * 0.3
        }

# Initialize emotional system
emotional_system = EmotionalSystem()

# Pattern generation influenced by emotions
class EmotionalBrush:
    def __init__(self, x, y, emotional_system):
        self.x = x
        self.y = y
        self.emotional_system = emotional_system
        self.trail = []
        self.age = 0
        
    def paint(self, canvas):
        """Paint on canvas based on emotional state"""
        movement = self.emotional_system.get_movement_style()
        color_influence = self.emotional_system.get_color_influence()
        
        # Movement influenced by emotions
        speed = movement['speed'] * 3
        self.age += 1
        
        # Calculate movement direction
        if self.age % int(10 / (movement['direction_change'] + 0.1)) == 0:
            base_angle = np.random.uniform(0, 2 * np.pi)
        else:
            base_angle = math.atan2(self.y - HEIGHT/2, self.x - WIDTH/2)
        
        # Emotional influence on direction
        angle_variation = (self.emotional_system.emotions['curiosity'] - 0.5) * np.pi
        angle = base_angle + angle_variation * math.sin(self.age * 0.1)
        
        # Update position with boundary wrapping
        self.x = (self.x + speed * math.cos(angle)) % WIDTH
        self.y = (self.y + speed * math.sin(angle)) % HEIGHT
        
        # Store trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 20:
            self.trail.pop(0)
        
        # Paint based on emotional state
        brush_size = int(5 + self.emotional_system.emotions['joy'] * 10)
        
        for i, (tx, ty) in enumerate(self.trail):
            # Trail fades
            intensity = (i + 1) / len(self.trail)
            
            # Color from emotions
            h, s, v = color_influence
            # Add variation based on position in trail
            h = (h + i * 0.01) % 1.0
            v = v * intensity
            
            # Convert to RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            
            # Paint with gaussian falloff
            for dy in range(-brush_size, brush_size + 1):
                for dx in range(-brush_size, brush_size + 1):
                    px = int(tx + dx) % WIDTH
                    py = int(ty + dy) % HEIGHT
                    
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance <= brush_size:
                        falloff = math.exp(-(distance**2) / (brush_size**2))
                        
                        # Blend with existing
                        canvas[py, px, 0] += r * falloff * 0.1
                        canvas[py, px, 1] += g * falloff * 0.1
                        canvas[py, px, 2] += b * falloff * 0.1
        
        # Return pattern metrics for emotional feedback
        local_area = canvas[max(0, int(self.y)-50):min(HEIGHT, int(self.y)+50),
                           max(0, int(self.x)-50):min(WIDTH, int(self.x)+50)]
        
        return {
            'chaos': np.std(local_area),
            'harmony': 1 - np.std(np.diff(local_area, axis=0)),
            'density': np.mean(local_area),
            'movement': speed / 10
        }

# Create multiple brushes
print("Initializing sentient canvas...")
brushes = []
for _ in range(8):
    x = np.random.randint(100, WIDTH - 100)
    y = np.random.randint(100, HEIGHT - 100)
    brushes.append(EmotionalBrush(x, y, emotional_system))

# Let the canvas live and create
print("Canvas beginning to feel and create...")
iterations = 800

for iteration in range(iterations):
    if iteration % 100 == 0:
        print(f"Iteration {iteration}: Current emotional state:")
        for emotion, value in emotional_system.emotions.items():
            print(f"  {emotion}: {value:.3f}")
    
    # Each brush paints and generates pattern metrics
    all_metrics = []
    for brush in brushes:
        metrics = brush.paint(canvas)
        all_metrics.append(metrics)
    
    # Average metrics influence emotional state
    avg_metrics = {
        'chaos': np.mean([m['chaos'] for m in all_metrics]),
        'harmony': np.mean([m['harmony'] for m in all_metrics]),
        'density': np.mean([m['density'] for m in all_metrics]),
        'movement': np.mean([m['movement'] for m in all_metrics])
    }
    
    # Emotional system reacts to what it created
    emotional_system.feel_pattern(avg_metrics)
    
    # Occasionally spawn new brushes based on curiosity
    if np.random.random() < emotional_system.emotions['curiosity'] * 0.01:
        x = np.random.randint(0, WIDTH)
        y = np.random.randint(0, HEIGHT)
        brushes.append(EmotionalBrush(x, y, emotional_system))
    
    # Remove old brushes based on melancholy
    if len(brushes) > 5 and np.random.random() < emotional_system.emotions['melancholy'] * 0.01:
        brushes.pop(0)

# Add emotional "signature" - visualize the emotional journey
print("Adding emotional signature...")
emotion_history_height = 100
emotion_viz = np.zeros((emotion_history_height, WIDTH, 3), dtype=np.float32)

if emotional_system.memory:
    memory_points = len(emotional_system.memory)
    for i, memory_state in enumerate(emotional_system.memory):
        x = int(i * WIDTH / memory_points)
        
        y_offset = 0
        for emotion, value in memory_state.items():
            emotion_height = int(value * emotion_history_height / 6)
            
            # Color for each emotion
            emotion_colors = {
                'joy': (1.0, 0.9, 0.3),
                'melancholy': (0.3, 0.4, 0.8),
                'agitation': (0.9, 0.3, 0.3),
                'serenity': (0.3, 0.8, 0.8),
                'curiosity': (0.7, 0.3, 0.8),
                'fear': (0.3, 0.6, 0.3)
            }
            
            color = emotion_colors[emotion]
            for y in range(emotion_height):
                if y_offset + y < emotion_history_height:
                    emotion_viz[y_offset + y, x] = color
            
            y_offset += emotion_height

# Combine main canvas with emotional signature
canvas = np.clip(canvas, 0, 1)
final_image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

# Main canvas
final_image[:HEIGHT-emotion_history_height] = (canvas[:HEIGHT-emotion_history_height] * 255).astype(np.uint8)

# Emotional signature at bottom
final_image[HEIGHT-emotion_history_height:] = (emotion_viz * 255).astype(np.uint8)

# Save the image
image = Image.fromarray(final_image, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-04_sentient_canvas/sentient_canvas_01.png')

print("\nSentient canvas complete.")
print("Final emotional state:")
for emotion, value in emotional_system.emotions.items():
    print(f"  {emotion}: {value:.3f}")
print("\nThe canvas has lived, felt, and expressed.")
print("Its emotional journey is encoded in its creation.")