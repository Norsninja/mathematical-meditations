import numpy as np
from PIL import Image
import math

# Particle Dance - Emergent Choreography
# Where individual movements create collective beauty

WIDTH, HEIGHT = 1080, 1080

# Create black canvas with alpha channel
image_array = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)

# Particle system parameters
NUM_PARTICLES = 400  # Reduced for faster computation
NUM_ATTRACTORS = 5
TRAIL_LENGTH = 30  # Shorter trails

# Initialize particles
particles = {
    'positions': np.random.rand(NUM_PARTICLES, 2) * [WIDTH, HEIGHT],
    'velocities': np.random.randn(NUM_PARTICLES, 2) * 0.5,
    'colors': np.zeros((NUM_PARTICLES, 3)),
    'masses': np.random.uniform(0.5, 2.0, NUM_PARTICLES),
    'trails': [[] for _ in range(NUM_PARTICLES)]
}

# Create attractors with different properties
attractors = []
for i in range(NUM_ATTRACTORS):
    angle = i * 2 * np.pi / NUM_ATTRACTORS
    radius = 250
    x = WIDTH/2 + radius * np.cos(angle)
    y = HEIGHT/2 + radius * np.sin(angle)
    
    attractor = {
        'position': np.array([x, y]),
        'strength': np.random.uniform(50, 150),
        'color': np.array([
            0.5 + 0.5 * np.cos(angle),
            0.5 + 0.5 * np.cos(angle + 2*np.pi/3),
            0.5 + 0.5 * np.cos(angle + 4*np.pi/3)
        ])
    }
    attractors.append(attractor)

# Color particles based on nearest attractor
for i in range(NUM_PARTICLES):
    pos = particles['positions'][i]
    
    # Find nearest attractor
    min_dist = float('inf')
    nearest_color = None
    
    for attractor in attractors:
        dist = np.linalg.norm(pos - attractor['position'])
        if dist < min_dist:
            min_dist = dist
            nearest_color = attractor['color']
    
    # Add variation
    variation = np.random.uniform(-0.1, 0.1, 3)
    particles['colors'][i] = np.clip(nearest_color + variation, 0, 1)

print("Beginning particle dance...")

# Simulation parameters
dt = 0.5
friction = 0.99
repulsion_radius = 20
repulsion_strength = 50

# Run simulation
for step in range(200):  # Reduced steps
    if step % 50 == 0:
        print(f"Step {step}: Particles dancing...")
    
    # Calculate forces on each particle
    forces = np.zeros((NUM_PARTICLES, 2))
    
    # Attractor forces
    for i in range(NUM_PARTICLES):
        pos = particles['positions'][i]
        mass = particles['masses'][i]
        
        for attractor in attractors:
            # Vector from particle to attractor
            r = attractor['position'] - pos
            dist = np.linalg.norm(r)
            
            if dist > 1:  # Avoid division by zero
                # Gravitational-like attraction
                force_magnitude = attractor['strength'] * mass / (dist ** 1.5)
                forces[i] += force_magnitude * r / dist
        
        # Add central repulsion to prevent clustering
        center = np.array([WIDTH/2, HEIGHT/2])
        r_center = pos - center
        dist_center = np.linalg.norm(r_center)
        if dist_center < 100:
            repel_force = 100 / (dist_center + 1)
            forces[i] += repel_force * r_center / (dist_center + 1)
    
    # Particle-particle repulsion
    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            r = particles['positions'][j] - particles['positions'][i]
            dist = np.linalg.norm(r)
            
            if dist < repulsion_radius and dist > 0:
                # Repulsive force
                force_magnitude = repulsion_strength / (dist ** 2)
                force = force_magnitude * r / dist
                
                forces[i] -= force
                forces[j] += force
    
    # Update velocities and positions
    particles['velocities'] += forces * dt / particles['masses'][:, np.newaxis]
    particles['velocities'] *= friction
    particles['positions'] += particles['velocities'] * dt
    
    # Boundary conditions - wrap around
    particles['positions'] = particles['positions'] % [WIDTH, HEIGHT]
    
    # Update trails
    for i in range(NUM_PARTICLES):
        trail = particles['trails'][i]
        trail.append(particles['positions'][i].copy())
        
        # Keep trail length limited
        if len(trail) > TRAIL_LENGTH:
            trail.pop(0)

print("Rendering particle trails...")

# Create trail intensity map
trail_map = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

# Draw trails with additive blending
for i in range(NUM_PARTICLES):
    trail = particles['trails'][i]
    color = particles['colors'][i]
    
    for j, pos in enumerate(trail):
        if j > 0:
            prev_pos = trail[j-1]
            
            # Trail intensity based on position in trail
            intensity = (j / len(trail)) ** 2
            
            # Draw line segment
            x1, y1 = int(prev_pos[0]), int(prev_pos[1])
            x2, y2 = int(pos[0]), int(pos[1])
            
            # Simple line drawing
            steps = max(abs(x2 - x1), abs(y2 - y1))
            if steps > 0:
                for step in range(steps + 1):
                    t = step / steps
                    x = int(x1 + t * (x2 - x1))
                    y = int(y1 + t * (y2 - y1))
                    
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        trail_map[y, x] += intensity * 0.5

# Apply Gaussian blur to trail map for glow effect
from scipy.ndimage import gaussian_filter
trail_map = gaussian_filter(trail_map, sigma=2)

# Convert trail map to color image
for y in range(HEIGHT):
    for x in range(WIDTH):
        intensity = min(trail_map[y, x], 1.0)
        
        if intensity > 0.01:
            # Get average color of nearby particles
            nearby_colors = []
            for i in range(NUM_PARTICLES):
                pos = particles['positions'][i]
                dist = np.sqrt((pos[0] - x)**2 + (pos[1] - y)**2)
                if dist < 100:
                    weight = 1 / (dist + 10)
                    nearby_colors.append((particles['colors'][i], weight))
            
            if nearby_colors:
                # Weighted average color
                total_weight = sum(w for _, w in nearby_colors)
                avg_color = sum(c * w for c, w in nearby_colors) / total_weight
                
                # Apply color with intensity
                for c in range(3):
                    image_array[y, x, c] = int(avg_color[c] * intensity * 255)
                
                # Alpha channel
                image_array[y, x, 3] = int(intensity * 255)

# Draw current particle positions as bright points
for i in range(NUM_PARTICLES):
    x, y = int(particles['positions'][i][0]), int(particles['positions'][i][1])
    
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        # Bright core
        color = particles['colors'][i]
        image_array[y, x, :3] = (color * 255).astype(np.uint8)
        image_array[y, x, 3] = 255
        
        # Small glow
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    dist = np.sqrt(dx**2 + dy**2)
                    if dist > 0:
                        glow = 0.3 / dist
                        for c in range(3):
                            current = image_array[ny, nx, c]
                            new_val = current + color[c] * glow * 100
                            image_array[ny, nx, c] = min(255, int(new_val))

# Draw attractors as subtle points
for attractor in attractors:
    x, y = int(attractor['position'][0]), int(attractor['position'][1])
    
    # Subtle glow around attractor
    for r in range(10, 0, -1):
        alpha = 0.1 * (r / 10)
        color = (attractor['color'] * alpha * 255).astype(np.uint8)
        
        # Draw circle
        for angle in np.linspace(0, 2*np.pi, max(8, r*2)):
            px = int(x + r * np.cos(angle))
            py = int(y + r * np.sin(angle))
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                for c in range(3):
                    image_array[py, px, c] = min(255, image_array[py, px, c] + color[c])

# Create and save image
image = Image.fromarray(image_array, 'RGBA')

# Composite onto dark background
background = Image.new('RGB', (WIDTH, HEIGHT), (5, 5, 15))
background.paste(image, (0, 0), image)
background.save('/home/norsninja/Art/artworks/2025-08-04_particle_dance/particle_dance_01.png')

print("Particle dance complete.")
print("From chaos, choreography emerges.")
print("Each particle's path is unique, yet all dance together.")