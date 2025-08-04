from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import random
import math
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Particle-based emergence system
class Particle:
    def __init__(self, x, y, generation=0):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.age = 0
        self.generation = generation
        self.energy = 1.0
        self.connections = []
        
    def update(self, particles, width, height):
        # Age and energy decay
        self.age += 1
        self.energy *= 0.995
        
        # Attraction/repulsion to other particles
        fx, fy = 0, 0
        self.connections = []
        
        for other in particles:
            if other is self:
                continue
            
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < 1:
                continue
                
            # Connection threshold
            if dist < 100:
                self.connections.append(other)
                
            # Forces
            if dist < 30:  # Repulsion
                force = -20 / (dist * dist)
            elif dist < 150:  # Attraction
                force = 0.5 / dist
            else:
                continue
                
            fx += force * dx / dist
            fy += force * dy / dist
        
        # Update velocity with forces and damping
        self.vx = (self.vx + fx) * 0.98
        self.vy = (self.vy + fy) * 0.98
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Soft boundary wrapping
        margin = 50
        if self.x < margin:
            self.vx += 0.5
        elif self.x > width - margin:
            self.vx -= 0.5
        if self.y < margin:
            self.vy += 0.5
        elif self.y > height - margin:
            self.vy -= 0.5
            
        # Keep in bounds
        self.x = max(0, min(width, self.x))
        self.y = max(0, min(height, self.y))
        
    def should_spawn(self):
        # Spawn new particles based on energy and connections
        return (self.energy > 0.7 and 
                len(self.connections) >= 2 and 
                len(self.connections) <= 4 and
                random.random() < 0.02)

# Initialize particle system
def create_initial_particles():
    particles = []
    # Create several seed clusters
    for _ in range(5):
        cx = random.uniform(WIDTH * 0.2, WIDTH * 0.8)
        cy = random.uniform(HEIGHT * 0.2, HEIGHT * 0.8)
        
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(0, 30)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            particles.append(Particle(x, y))
    
    return particles

# Create the image
def render_particles(particles, history):
    # Create main image and layers
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(8, 12, 20))
    
    # Create glow layer
    glow = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    # Create connection layer
    connections = Image.new('RGBA', (WIDTH, HEIGHT), color=(0, 0, 0, 0))
    conn_draw = ImageDraw.Draw(connections)
    
    # Draw particle trails from history
    for i, old_particles in enumerate(history[-20:]):
        fade = i / 20.0
        for p in old_particles:
            # Color based on generation and energy
            hue = (0.5 + p.generation * 0.1) % 1.0
            saturation = 0.7 + p.energy * 0.3
            value = fade * 0.3
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
            
            size = 2 + fade * 2
            glow_draw.ellipse([p.x - size, p.y - size, p.x + size, p.y + size],
                             fill=(r//4, g//4, b//4))
    
    # Draw current particles and connections
    for p in particles:
        # Draw connections
        for other in p.connections:
            if other.x > p.x:  # Draw each connection once
                # Connection strength based on distance
                dx = other.x - p.x
                dy = other.y - p.y
                dist = math.sqrt(dx*dx + dy*dy)
                alpha = int(255 * (1 - dist / 100) * min(p.energy, other.energy))
                
                # Color gradient along connection
                hue = (0.5 + p.generation * 0.1) % 1.0
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.8, 0.7)]
                
                conn_draw.line([p.x, p.y, other.x, other.y], 
                              fill=(r, g, b, alpha), width=1)
    
    # Draw particles
    draw = ImageDraw.Draw(img)
    for p in particles:
        # Dynamic color based on energy and generation
        hue = (0.55 + p.generation * 0.08 + p.energy * 0.1) % 1.0
        saturation = 0.6 + p.energy * 0.4
        value = 0.7 + p.energy * 0.3
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
        
        # Particle size based on energy and connections
        base_size = 3 + len(p.connections) * 0.5
        size = base_size * (0.5 + p.energy)
        
        # Core particle
        draw.ellipse([p.x - size, p.y - size, p.x + size, p.y + size],
                    fill=(r, g, b))
        
        # Energy glow
        for i in range(3):
            glow_size = size + (i + 1) * 3
            glow_alpha = int(80 * p.energy / (i + 1))
            glow_draw.ellipse([p.x - glow_size, p.y - glow_size, 
                              p.x + glow_size, p.y + glow_size],
                             fill=(r//3, g//3, b//3))
    
    # Apply gaussian blur to glow
    glow = glow.filter(ImageFilter.GaussianBlur(radius=5))
    
    # Composite layers
    img = Image.blend(img, glow, 0.6)
    img.paste(connections, (0, 0), connections)
    
    return img

# Main simulation
particles = create_initial_particles()
history = []
generation_counter = 0

for step in range(150):
    # Store history snapshot
    history.append([(p.x, p.y, p.generation, p.energy) for p in particles])
    
    # Update all particles
    for p in particles:
        p.update(particles, WIDTH, HEIGHT)
    
    # Spawn new particles
    new_particles = []
    for p in particles:
        if p.should_spawn() and len(particles) + len(new_particles) < 300:
            # Spawn near parent with inherited properties
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(20, 40)
            new_p = Particle(
                p.x + dist * math.cos(angle),
                p.y + dist * math.sin(angle),
                generation_counter
            )
            new_particles.append(new_p)
    
    if new_particles:
        generation_counter += 1
        particles.extend(new_particles)
    
    # Remove dead particles
    particles = [p for p in particles if p.energy > 0.1 and p.age < 200]
    
    # Occasionally inject new energy
    if step % 30 == 0 and len(particles) < 50:
        cx = random.uniform(WIDTH * 0.3, WIDTH * 0.7)
        cy = random.uniform(HEIGHT * 0.3, HEIGHT * 0.7)
        for _ in range(10):
            particles.append(Particle(
                cx + random.uniform(-20, 20),
                cy + random.uniform(-20, 20),
                generation_counter
            ))

# Convert history to particle objects for rendering
history_particles = []
for snapshot in history:
    frame_particles = []
    for x, y, gen, energy in snapshot:
        p = Particle(x, y, gen)
        p.energy = energy
        frame_particles.append(p)
    history_particles.append(frame_particles)

# Render final image
img = render_particles(particles, history_particles)
img.save('emergence_03.png')
print("Third iteration created: emergence_03.png")