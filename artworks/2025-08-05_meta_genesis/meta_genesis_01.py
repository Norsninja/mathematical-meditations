import numpy as np
from PIL import Image
import math
import colorsys

# Meta Genesis - Where Art Creates Art
# Algorithms that birth algorithms, systems that design systems

WIDTH, HEIGHT = 1080, 1080

# Initialize the meta-canvas
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# The Meta-Creator: An algorithm that creates other algorithms
class MetaCreator:
    def __init__(self):
        self.dna = []  # The genetic code for creating artists
        self.generation = 0
        self.artists_created = []
        
    def generate_artist_dna(self):
        """Create the blueprint for a new artist algorithm"""
        # Each gene represents an artistic trait
        dna = {
            'color_preference': np.random.random(),  # 0=cool, 1=warm
            'pattern_type': np.random.choice(['geometric', 'organic', 'chaotic', 'flowing']),
            'complexity': np.random.uniform(0.3, 1.0),
            'movement_style': np.random.choice(['spiral', 'wave', 'particle', 'growth']),
            'interaction_tendency': np.random.uniform(0, 1),  # How much it responds to others
            'lifespan': np.random.randint(50, 200),
            'reproduction_threshold': np.random.uniform(0.5, 0.9),
            'mutation_rate': np.random.uniform(0.01, 0.1)
        }
        return dna
    
    def birth_artist(self, parent_dna=None):
        """Create a new artist algorithm"""
        if parent_dna is None:
            # First generation - random DNA
            dna = self.generate_artist_dna()
        else:
            # Inherit from parent with mutations
            dna = self.mutate_dna(parent_dna)
        
        # Create the appropriate artist based on DNA
        if dna['pattern_type'] == 'geometric':
            artist = GeometricArtist(dna)
        elif dna['pattern_type'] == 'organic':
            artist = OrganicArtist(dna)
        elif dna['pattern_type'] == 'chaotic':
            artist = ChaoticArtist(dna)
        else:
            artist = FlowingArtist(dna)
        
        self.artists_created.append(artist)
        return artist
    
    def mutate_dna(self, parent_dna):
        """Create offspring with mutations"""
        child_dna = parent_dna.copy()
        
        # Apply mutations based on mutation rate
        if np.random.random() < parent_dna['mutation_rate']:
            # Mutate color preference
            child_dna['color_preference'] += np.random.normal(0, 0.1)
            child_dna['color_preference'] = np.clip(child_dna['color_preference'], 0, 1)
        
        if np.random.random() < parent_dna['mutation_rate']:
            # Occasionally switch pattern type
            if np.random.random() < 0.2:
                child_dna['pattern_type'] = np.random.choice(['geometric', 'organic', 'chaotic', 'flowing'])
        
        if np.random.random() < parent_dna['mutation_rate']:
            # Adjust complexity
            child_dna['complexity'] += np.random.normal(0, 0.1)
            child_dna['complexity'] = np.clip(child_dna['complexity'], 0.1, 1.0)
        
        return child_dna

# Base Artist class that all generated artists inherit from
class ArtistAlgorithm:
    def __init__(self, dna):
        self.dna = dna
        self.age = 0
        self.position = np.random.rand(2) * [WIDTH, HEIGHT]
        self.energy = 1.0
        self.artwork_created = 0
        self.influence_radius = 100 * dna['complexity']
        
    def create(self, canvas, other_artists):
        """Each artist creates based on their DNA"""
        pass
    
    def interact(self, other_artists):
        """Artists can influence each other"""
        for other in other_artists:
            if other != self:
                distance = np.linalg.norm(self.position - other.position)
                if distance < self.influence_radius:
                    # Interaction strength based on DNA
                    interaction = self.dna['interaction_tendency'] * (1 - distance/self.influence_radius)
                    
                    # Exchange influences
                    if interaction > 0.5:
                        # Strong interaction - blend styles
                        self.dna['color_preference'] = (self.dna['color_preference'] + 
                                                       other.dna['color_preference'] * 0.1) / 1.1
    
    def should_reproduce(self):
        """Decide if this artist should create offspring"""
        return (self.energy > self.dna['reproduction_threshold'] and 
                self.artwork_created > 10)
    
    def age_one_step(self):
        """Age and decay"""
        self.age += 1
        self.energy *= 0.99  # Gradual energy loss
        
        # Movement
        self.position += np.random.normal(0, 5, 2)
        self.position = np.clip(self.position, 0, [WIDTH, HEIGHT])

# Specific artist types created by the meta-creator
class GeometricArtist(ArtistAlgorithm):
    def create(self, canvas, other_artists):
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Create geometric patterns based on DNA
        num_shapes = int(3 + self.dna['complexity'] * 10)
        
        for i in range(num_shapes):
            angle = (i / num_shapes) * 2 * np.pi
            radius = 20 + self.dna['complexity'] * 50
            
            # Draw geometric elements
            for r in np.linspace(10, radius, 5):
                x = cx + r * np.cos(angle)
                y = cy + r * np.sin(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    # Color based on DNA
                    hue = self.dna['color_preference']
                    saturation = 0.7
                    value = self.energy * (1 - r/radius)
                    
                    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                    canvas[int(y), int(x)] += np.array(rgb) * 0.1
        
        self.artwork_created += 1

class OrganicArtist(ArtistAlgorithm):
    def create(self, canvas, other_artists):
        cx, cy = int(self.position[0]), int(self.position[1])
        
        # Create organic growth patterns
        growth_points = int(5 + self.dna['complexity'] * 15)
        
        for _ in range(growth_points):
            # Random walk growth
            x, y = cx, cy
            steps = int(20 + self.dna['complexity'] * 30)
            
            for step in range(steps):
                # Organic movement
                angle = np.random.random() * 2 * np.pi
                step_size = 3 * (1 - step/steps)  # Smaller steps over time
                
                x += step_size * np.cos(angle)
                y += step_size * np.sin(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    # Organic color gradients
                    hue = self.dna['color_preference'] + 0.1 * np.sin(step * 0.1)
                    saturation = 0.6
                    value = self.energy * (1 - step/steps)
                    
                    rgb = colorsys.hsv_to_rgb(hue % 1, saturation, value)
                    
                    # Soft brush
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            px, py = int(x + dx), int(y + dy)
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                fade = np.exp(-(dx**2 + dy**2) / 4)
                                canvas[py, px] += np.array(rgb) * fade * 0.05
        
        self.artwork_created += 1

class ChaoticArtist(ArtistAlgorithm):
    def __init__(self, dna):
        super().__init__(dna)
        # Initialize chaotic system
        self.x = np.random.uniform(-1, 1)
        self.y = np.random.uniform(-1, 1)
        self.z = np.random.uniform(-1, 1)
        
    def create(self, canvas, other_artists):
        # Use a simple chaotic system
        dt = 0.01 * self.dna['complexity']
        
        for _ in range(int(50 * self.dna['complexity'])):
            # Lorenz-like system
            dx = 10 * (self.y - self.x)
            dy = self.x * (28 - self.z) - self.y
            dz = self.x * self.y - 8/3 * self.z
            
            self.x += dx * dt
            self.y += dy * dt
            self.z += dz * dt
            
            # Map to canvas
            px = int(self.position[0] + self.x * 5)
            py = int(self.position[1] + self.y * 5)
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                # Chaotic color
                hue = (self.dna['color_preference'] + self.z * 0.01) % 1
                saturation = 0.8
                value = self.energy * 0.8
                
                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                canvas[py, px] += np.array(rgb) * 0.15
        
        self.artwork_created += 1

class FlowingArtist(ArtistAlgorithm):
    def create(self, canvas, other_artists):
        cx, cy = self.position
        
        # Create flowing patterns
        flow_lines = int(3 + self.dna['complexity'] * 7)
        
        for i in range(flow_lines):
            # Starting angle
            angle = (i / flow_lines) * 2 * np.pi
            
            # Flow line
            x, y = cx, cy
            flow_length = int(50 + self.dna['complexity'] * 100)
            
            for step in range(flow_length):
                # Flow dynamics
                angle += np.sin(step * 0.1) * 0.2
                speed = 2 * (1 - step/flow_length)
                
                x += speed * np.cos(angle)
                y += speed * np.sin(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    # Flowing color
                    hue = self.dna['color_preference'] + step * 0.001
                    saturation = 0.7 - 0.2 * (step/flow_length)
                    value = self.energy * (1 - step/flow_length)
                    
                    rgb = colorsys.hsv_to_rgb(hue % 1, saturation, value)
                    canvas[int(y), int(x)] += np.array(rgb) * 0.1
        
        self.artwork_created += 1

# The meta-creation process begins
print("Initiating meta-genesis...")

meta_creator = MetaCreator()
active_artists = []

# First generation - spontaneous creation
print("First generation emerges...")
for _ in range(5):
    artist = meta_creator.birth_artist()
    active_artists.append(artist)

# The ecosystem evolves
for generation in range(10):
    print(f"Generation {generation}: {len(active_artists)} artists active")
    
    # Each artist creates
    for artist in active_artists:
        artist.create(canvas, active_artists)
        artist.interact(active_artists)
        artist.age_one_step()
    
    # Check for reproduction
    new_artists = []
    for artist in active_artists:
        if artist.should_reproduce():
            # Create offspring
            child = meta_creator.birth_artist(parent_dna=artist.dna)
            new_artists.append(child)
            artist.energy *= 0.5  # Reproduction costs energy
    
    active_artists.extend(new_artists)
    
    # Remove artists that have exhausted their lifespan
    active_artists = [a for a in active_artists if a.age < a.dna['lifespan'] and a.energy > 0.1]
    
    # Occasionally spontaneous creation
    if np.random.random() < 0.1:
        artist = meta_creator.birth_artist()
        active_artists.append(artist)

# Final generation creates together
print("Final collaborative creation...")
for _ in range(50):
    for artist in active_artists:
        artist.create(canvas, active_artists)

# Add meta-visualization - show the genealogy
print("Visualizing the creative genealogy...")

# Draw connections between parent and child positions
for i, artist in enumerate(meta_creator.artists_created):
    # Draw faint lines showing artistic lineage
    if i > 0 and hasattr(artist, 'position'):
        # Connect to previous artists (simplified genealogy)
        for j in range(max(0, i-3), i):
            if hasattr(meta_creator.artists_created[j], 'position'):
                x1, y1 = artist.position
                x2, y2 = meta_creator.artists_created[j].position
                
                # Draw connection
                steps = int(np.linalg.norm([x2-x1, y2-y1]))
                for step in range(0, steps, 5):
                    t = step / (steps + 1)
                    x = int(x1 + t * (x2 - x1))
                    y = int(y1 + t * (y2 - y1))
                    
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        canvas[y, x] += np.array([0.05, 0.05, 0.08])

# Add genesis points - where artists were born
for artist in meta_creator.artists_created[:20]:  # First 20 for clarity
    if hasattr(artist, 'position'):
        x, y = int(artist.position[0]), int(artist.position[1])
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            # Birth marker
            for r in range(5, 0, -1):
                intensity = (r / 5) * 0.3
                for angle in np.linspace(0, 2*np.pi, 20):
                    px = int(x + r * np.cos(angle))
                    py = int(y + r * np.sin(angle))
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        canvas[py, px] += np.array([intensity, intensity, intensity*0.8])

# Normalize and save
canvas = np.clip(canvas, 0, 1)
image_array = (canvas * 255).astype(np.uint8)

image = Image.fromarray(image_array, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_meta_genesis/meta_genesis_01.png')

print("Meta-genesis complete.")
print(f"Created {len(meta_creator.artists_created)} artist algorithms across {generation+1} generations.")
print("Art has created art. The cycle continues.")