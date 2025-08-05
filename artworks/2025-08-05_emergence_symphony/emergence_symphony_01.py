import numpy as np
from PIL import Image
import math
import colorsys

# Emergence Symphony - Where Simple Rules Birth Complex Beauty
# The moment when quantity becomes quality, when many become one

WIDTH, HEIGHT = 1080, 1080

# Initialize the emergence canvas
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)  # RGBA for layered emergence

# Track emergence metrics
emergence_map = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

# Simple Rule System 1: Flocking Particles
class Boid:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=np.float32)
        self.velocity = (np.random.rand(2) - 0.5) * 2
        self.acceleration = np.zeros(2)
        self.max_speed = 2.0
        self.max_force = 0.05
        self.perception_radius = 50
        self.trail = []
        self.hue = np.random.random()
        
    def flock(self, boids):
        """Three simple rules create complex behavior"""
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        
        # Weight the forces
        self.acceleration += alignment * 1.5
        self.acceleration += cohesion * 1.0
        self.acceleration += separation * 2.0
        
    def align(self, boids):
        """Steer towards average heading of neighbors"""
        steering = np.zeros(2)
        total = 0
        
        for other in boids:
            dist = np.linalg.norm(self.position - other.position)
            if other != self and dist < self.perception_radius:
                steering += other.velocity
                total += 1
                
        if total > 0:
            steering /= total
            steering = (steering / np.linalg.norm(steering + 1e-6)) * self.max_speed
            steering -= self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force
                
        return steering
    
    def cohere(self, boids):
        """Steer towards average position of neighbors"""
        steering = np.zeros(2)
        total = 0
        
        for other in boids:
            dist = np.linalg.norm(self.position - other.position)
            if other != self and dist < self.perception_radius:
                steering += other.position
                total += 1
                
        if total > 0:
            steering /= total
            steering -= self.position
            steering = (steering / np.linalg.norm(steering + 1e-6)) * self.max_speed
            steering -= self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force
                
        return steering
    
    def separate(self, boids):
        """Steer away from neighbors"""
        steering = np.zeros(2)
        total = 0
        
        for other in boids:
            dist = np.linalg.norm(self.position - other.position)
            if other != self and dist < self.perception_radius / 2:
                diff = self.position - other.position
                if dist > 0:
                    diff /= dist  # Weight by distance
                steering += diff
                total += 1
                
        if total > 0:
            steering /= total
            steering = (steering / np.linalg.norm(steering + 1e-6)) * self.max_speed
            steering -= self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force
                
        return steering
    
    def update(self):
        """Simple physics creates complex motion"""
        self.velocity += self.acceleration
        
        # Limit speed
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed
            
        self.position += self.velocity
        self.acceleration *= 0
        
        # Wrap around edges
        self.position[0] = self.position[0] % WIDTH
        self.position[1] = self.position[1] % HEIGHT
        
        # Keep trail
        self.trail.append(self.position.copy())
        if len(self.trail) > 20:
            self.trail.pop(0)
    
    def draw(self, canvas):
        """Leave traces of emergence"""
        # Draw trail
        for i, pos in enumerate(self.trail):
            x, y = int(pos[0]), int(pos[1])
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Trail fades
                intensity = i / len(self.trail)
                rgb = colorsys.hsv_to_rgb(self.hue, 0.7, intensity)
                canvas[y, x, :3] += np.array(rgb) * 0.1
                canvas[y, x, 3] = min(1, canvas[y, x, 3] + intensity * 0.1)
                
                # Mark emergence
                emergence_map[y, x] += 0.01

# Simple Rule System 2: Cellular Automata Network
class CellularNetwork:
    def __init__(self, size=100):
        self.size = size
        self.grid = np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])
        self.history = []
        self.connections = np.zeros((size, size), dtype=np.float32)
        
    def update(self):
        """Conway's rules + network effects"""
        new_grid = np.zeros_like(self.grid)
        
        for i in range(self.size):
            for j in range(self.size):
                # Count neighbors
                neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = (i + di) % self.size, (j + dj) % self.size
                        neighbors += self.grid[ni, nj]
                
                # Conway's rules with twist
                if self.grid[i, j] == 1:
                    if neighbors in [2, 3]:
                        new_grid[i, j] = 1
                        # Strengthen connections
                        self.connections[i, j] = min(1, self.connections[i, j] + 0.1)
                else:
                    if neighbors == 3:
                        new_grid[i, j] = 1
                
                # Network influence
                if self.connections[i, j] > 0.5 and np.random.random() < 0.1:
                    new_grid[i, j] = 1
        
        self.grid = new_grid
        self.history.append(self.grid.copy())
        if len(self.history) > 10:
            self.history.pop(0)
    
    def draw(self, canvas, offset_x, offset_y, scale=5):
        """Visualize emergent patterns"""
        for i in range(self.size):
            for j in range(self.size):
                x = offset_x + j * scale
                y = offset_y + i * scale
                
                if self.grid[i, j] == 1:
                    # Draw cell with connection strength
                    for dx in range(scale):
                        for dy in range(scale):
                            px, py = x + dx, y + dy
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                # Color based on connectivity
                                connection_strength = self.connections[i, j]
                                hue = 0.3 + connection_strength * 0.4
                                rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.7)
                                
                                canvas[py, px, :3] += np.array(rgb) * 0.3
                                canvas[py, px, 3] = min(1, canvas[py, px, 3] + 0.3)
                                
                                emergence_map[py, px] += connection_strength * 0.05

# Simple Rule System 3: Reaction-Diffusion Waves
class ReactionDiffusion:
    def __init__(self, width=200, height=200):
        self.width = width
        self.height = height
        self.A = np.ones((height, width), dtype=np.float32)
        self.B = np.zeros((height, width), dtype=np.float32)
        
        # Seed patterns
        cx, cy = width // 2, height // 2
        for _ in range(5):
            x = np.random.randint(20, width-20)
            y = np.random.randint(20, height-20)
            self.B[y-10:y+10, x-10:x+10] = 1
        
        # Parameters
        self.dA = 1.0
        self.dB = 0.5
        self.feed = 0.055
        self.kill = 0.062
    
    def update(self):
        """Simple chemistry creates complex patterns"""
        # Laplacian convolution
        laplacian_kernel = np.array([[0.05, 0.2, 0.05],
                                     [0.2, -1, 0.2],
                                     [0.05, 0.2, 0.05]])
        
        # Compute Laplacians
        lA = np.zeros_like(self.A)
        lB = np.zeros_like(self.B)
        
        for i in range(1, self.height-1):
            for j in range(1, self.width-1):
                lA[i, j] = np.sum(laplacian_kernel * self.A[i-1:i+2, j-1:j+2])
                lB[i, j] = np.sum(laplacian_kernel * self.B[i-1:i+2, j-1:j+2])
        
        # Reaction-diffusion equations
        reaction = self.A * self.B * self.B
        self.A += self.dA * lA - reaction + self.feed * (1 - self.A)
        self.B += self.dB * lB + reaction - (self.kill + self.feed) * self.B
        
        # Keep in bounds
        self.A = np.clip(self.A, 0, 1)
        self.B = np.clip(self.B, 0, 1)
    
    def draw(self, canvas, offset_x, offset_y, scale=5):
        """Render emergent chemistry"""
        for i in range(0, self.height, 2):
            for j in range(0, self.width, 2):
                x = offset_x + j * scale
                y = offset_y + i * scale
                
                # Concentration determines color
                a = self.A[i, j]
                b = self.B[i, j]
                
                if b > 0.1:
                    for dx in range(scale*2):
                        for dy in range(scale*2):
                            px, py = x + dx, y + dy
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                # Purple-pink for B concentration
                                hue = 0.8 + b * 0.2
                                saturation = 0.9
                                value = b
                                
                                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                                canvas[py, px, :3] += np.array(rgb) * 0.4
                                canvas[py, px, 3] = min(1, canvas[py, px, 3] + b * 0.4)
                                
                                emergence_map[py, px] += b * 0.1

# Create the symphony of emergence
print("Initiating emergence symphony...")

# System 1: Flocking birds
flock = []
for _ in range(100):
    x = np.random.randint(100, WIDTH-100)
    y = np.random.randint(100, HEIGHT-100)
    flock.append(Boid(x, y))

# System 2: Cellular networks
networks = []
for _ in range(3):
    networks.append(CellularNetwork(50))

# System 3: Chemical patterns
chemistry = ReactionDiffusion(100, 100)

# Let emergence unfold
print("Simple rules creating complex beauty...")

for iteration in range(200):
    # Update flocking
    for boid in flock:
        boid.flock(flock)
        boid.update()
        boid.draw(canvas)
    
    # Update cellular networks
    if iteration % 5 == 0:
        for network in networks:
            network.update()
    
    # Draw networks at different positions
    if iteration % 10 == 0:
        networks[0].draw(canvas, 50, 50, 4)
        networks[1].draw(canvas, 800, 100, 4)
        networks[2].draw(canvas, 100, 800, 4)
    
    # Update chemistry
    if iteration % 2 == 0:
        chemistry.update()
        chemistry.draw(canvas, 400, 400, 3)
    
    if iteration % 50 == 0:
        print(f"Emergence iteration {iteration}...")

# Highlight areas of highest emergence
print("Revealing emergent structures...")

# Find emergence hotspots
threshold = np.percentile(emergence_map[emergence_map > 0], 80)

for y in range(0, HEIGHT, 5):
    for x in range(0, WIDTH, 5):
        if emergence_map[y, x] > threshold:
            # Draw subtle glow at emergence points
            for r in range(10, 0, -1):
                intensity = (1 - r/10) * 0.3
                for angle in np.linspace(0, 2*np.pi, max(10, r)):
                    px = int(x + r * np.cos(angle))
                    py = int(y + r * np.sin(angle))
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Golden glow for emergence
                        canvas[py, px, :3] += np.array([1.0, 0.9, 0.6]) * intensity * 0.1
                        canvas[py, px, 3] = min(1, canvas[py, px, 3] + intensity * 0.1)

# Add connection visualization between emergent structures
print("Connecting emergent patterns...")

# Find cluster centers
from scipy.ndimage import label, center_of_mass

# Threshold and label connected components
binary_emergence = emergence_map > threshold
labeled, num_features = label(binary_emergence)

if num_features > 1:
    # Get centers of emergent clusters
    centers = []
    for i in range(1, min(num_features + 1, 10)):  # Limit to 10 clusters
        center = center_of_mass(emergence_map, labeled, i)
        if not np.isnan(center[0]):
            centers.append(center)
    
    # Draw connections between nearby clusters
    for i, center1 in enumerate(centers):
        for j, center2 in enumerate(centers[i+1:], i+1):
            dist = np.linalg.norm(np.array(center1) - np.array(center2))
            
            if dist < 300:
                # Draw connecting arc
                steps = int(dist)
                for step in range(steps):
                    t = step / steps
                    
                    # Curved connection
                    curve_height = np.sin(t * np.pi) * 30
                    perpendicular = np.array([-(center2[0] - center1[0]), center2[1] - center1[1]])
                    if np.linalg.norm(perpendicular) > 0:
                        perpendicular = perpendicular / np.linalg.norm(perpendicular)
                    
                    x = center1[1] + t * (center2[1] - center1[1]) + perpendicular[0] * curve_height
                    y = center1[0] + t * (center2[0] - center1[0]) + perpendicular[1] * curve_height
                    
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        # Faint white connections
                        intensity = np.sin(t * np.pi) * 0.5
                        canvas[int(y), int(x), :3] += np.array([1, 1, 1]) * intensity * 0.05
                        canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + intensity * 0.05)

# Convert to RGB
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_emergence_symphony/emergence_symphony_01.png')

print("Emergence symphony complete.")
print("From simple rules, complexity blooms.")
print("The whole has become greater than the sum of its parts.")