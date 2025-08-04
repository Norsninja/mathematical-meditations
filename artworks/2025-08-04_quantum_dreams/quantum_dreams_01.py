from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image - the quantum void
img = Image.new('RGB', (WIDTH, HEIGHT), color=(5, 5, 15))
draw = ImageDraw.Draw(img, 'RGBA')

# Quantum particle class
class QuantumParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Uncertainty in position
        self.uncertainty_x = random.uniform(20, 100)
        self.uncertainty_y = random.uniform(20, 100)
        # Wave function parameters
        self.wavelength = random.uniform(50, 200)
        self.phase = random.uniform(0, 2 * math.pi)
        self.amplitude = random.uniform(0.5, 1.0)
        # Quantum properties
        self.spin = random.choice([-1, 1])
        self.energy = random.uniform(0.3, 1.0)
        self.entangled_with = None
        
    def wave_function(self, x, y):
        """Calculate probability amplitude at given position"""
        # Distance from particle center
        dx = x - self.x
        dy = y - self.y
        
        # Gaussian envelope (uncertainty principle)
        gaussian = math.exp(-(dx**2 / (2 * self.uncertainty_x**2) + 
                             dy**2 / (2 * self.uncertainty_y**2)))
        
        # Wave component
        r = math.sqrt(dx**2 + dy**2)
        wave = math.sin(2 * math.pi * r / self.wavelength + self.phase)
        
        return gaussian * wave * self.amplitude * self.energy
    
    def collapse_probability(self, observer_x, observer_y):
        """Observation collapses the wave function"""
        dx = observer_x - self.x
        dy = observer_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Probability of finding particle decreases with distance
        return math.exp(-distance / 100) * self.energy

# Create quantum particles
particles = []
num_particles = 12

# Primary particles
for i in range(num_particles):
    angle = (i / num_particles) * 2 * math.pi
    radius = 200 + random.uniform(-50, 50)
    x = WIDTH/2 + radius * math.cos(angle)
    y = HEIGHT/2 + radius * math.sin(angle)
    particles.append(QuantumParticle(x, y))

# Create entangled pairs
for i in range(0, len(particles), 2):
    if i + 1 < len(particles):
        particles[i].entangled_with = particles[i + 1]
        particles[i + 1].entangled_with = particles[i]

# Calculate quantum field
field = np.zeros((WIDTH, HEIGHT))
for y in range(0, HEIGHT, 2):  # Sample every 2 pixels for speed
    for x in range(0, WIDTH, 2):
        total = 0
        for particle in particles:
            # Superposition of all particle states
            amplitude = particle.wave_function(x, y)
            
            # Entanglement effects
            if particle.entangled_with:
                entangled_amplitude = particle.entangled_with.wave_function(x, y)
                # Quantum interference
                total += amplitude + entangled_amplitude * 0.5
            else:
                total += amplitude
                
        field[x, y] = total

# Normalize field
field_min = np.min(field)
field_max = np.max(field)
if field_max > field_min:
    field = (field - field_min) / (field_max - field_min)

# Render quantum field
for y in range(0, HEIGHT, 2):
    for x in range(0, WIDTH, 2):
        value = field[x, y]
        
        if abs(value) > 0.01:  # Threshold for visibility
            # Quantum color - phase determines hue
            phase = math.atan2(y - HEIGHT/2, x - WIDTH/2)
            hue = (phase / (2 * math.pi) + 0.5) % 1.0
            
            # Probability determines brightness and saturation
            probability = abs(value)
            
            # Interference patterns create color variations
            if value > 0:
                saturation = 0.3 + 0.7 * probability
                brightness = 0.2 + 0.8 * probability
            else:
                saturation = 0.5 + 0.5 * probability
                brightness = 0.1 + 0.4 * probability
            
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, brightness)]
            
            # Draw with transparency based on uncertainty
            alpha = int(200 * probability)
            draw.rectangle([x-1, y-1, x+1, y+1], fill=(r, g, b, alpha))

# Add particle cores where probability is highest
for particle in particles:
    # Particle glow
    for radius in range(30, 0, -5):
        alpha = int(50 * particle.energy * (radius / 30))
        
        # Color based on spin
        if particle.spin > 0:
            color = (100, 150, 255, alpha)  # Blue for spin up
        else:
            color = (255, 100, 150, alpha)  # Red for spin down
            
        draw.ellipse([particle.x - radius, particle.y - radius,
                     particle.x + radius, particle.y + radius],
                    fill=color)

# Draw entanglement connections
for particle in particles:
    if particle.entangled_with and particle.x < particle.entangled_with.x:
        # Quantum correlation visualization
        steps = 50
        for i in range(steps):
            t = i / steps
            x = particle.x + t * (particle.entangled_with.x - particle.x)
            y = particle.y + t * (particle.entangled_with.y - particle.y)
            
            # Oscillating connection
            offset = 10 * math.sin(t * math.pi * 4) * math.sin(t * math.pi)
            x += offset * math.cos(math.atan2(particle.entangled_with.y - particle.y,
                                             particle.entangled_with.x - particle.x) + math.pi/2)
            y += offset * math.sin(math.atan2(particle.entangled_with.y - particle.y,
                                             particle.entangled_with.x - particle.x) + math.pi/2)
            
            # Fading connection
            alpha = int(100 * (1 - 2 * abs(t - 0.5)))
            draw.ellipse([x-2, y-2, x+2, y+2], fill=(200, 200, 255, alpha))

# Observer effect - collapse points
observers = [(WIDTH * 0.2, HEIGHT * 0.2), 
            (WIDTH * 0.8, HEIGHT * 0.8),
            (WIDTH * 0.5, HEIGHT * 0.9)]

for ox, oy in observers:
    # Observation collapses nearby wave functions
    collapse_radius = 80
    
    # Draw collapsed region
    for r in range(collapse_radius, 0, -10):
        alpha = int(30 * (r / collapse_radius))
        draw.ellipse([ox - r, oy - r, ox + r, oy + r],
                    fill=(255, 255, 255, alpha))
    
    # Show collapsed particles
    for particle in particles:
        probability = particle.collapse_probability(ox, oy)
        if probability > 0.3:
            # Particle becomes classical
            draw.ellipse([particle.x - 5, particle.y - 5,
                         particle.x + 5, particle.y + 5],
                        fill=(255, 255, 255, int(255 * probability)))

# Heisenberg uncertainty visualization - grid distortion
for i in range(10):
    x = random.randint(100, WIDTH - 100)
    y = random.randint(100, HEIGHT - 100)
    
    # Uncertainty bubble
    for angle in np.linspace(0, 2 * math.pi, 20):
        for r in range(20, 60, 5):
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            
            # Distort based on uncertainty principle
            uncertainty = random.uniform(0.5, 2)
            px += random.uniform(-10, 10) * uncertainty
            py += random.uniform(-10, 10) * uncertainty
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                alpha = int(20 * (1 - r / 60))
                draw.point((px, py), fill=(150, 100, 200, alpha))

# Apply quantum blur
img = img.filter(ImageFilter.GaussianBlur(radius=1))

img.save('quantum_dreams_01.png')
print("Quantum Dreams manifested: quantum_dreams_01.png")