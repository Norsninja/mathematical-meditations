import numpy as np
from PIL import Image
import math
import colorsys

# Quantum Choreography - Where Fundamental Forces Dance
# Each force becomes an artist, painting with its own language

WIDTH, HEIGHT = 1080, 1080

# Initialize the quantum stage
canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)  # RGBA for layered forces

# The fundamental forces as creative entities
class ForceArtist:
    def __init__(self, force_type, strength, color_signature):
        self.force_type = force_type
        self.strength = strength
        self.color_signature = color_signature
        self.field = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
        
    def create_field(self):
        """Each force creates its own field pattern"""
        pass
    
    def paint(self, canvas):
        """Express the force visually"""
        pass

# Gravity - The Sculptor of Spacetime
class GravityArtist(ForceArtist):
    def __init__(self):
        super().__init__("gravity", 1.0, (0.5, 0.3, 0.8))  # Deep purple
        self.masses = []
        
        # Place massive objects
        for _ in range(5):
            mass = {
                'position': np.random.rand(2) * [WIDTH, HEIGHT],
                'mass': np.random.uniform(50, 200),
                'velocity': (np.random.rand(2) - 0.5) * 2
            }
            self.masses.append(mass)
    
    def create_field(self):
        """Calculate gravitational field from all masses"""
        self.field.fill(0)
        
        # Create mesh grid for field calculation
        y, x = np.ogrid[0:HEIGHT, 0:WIDTH]
        
        for mass in self.masses:
            mx, my = mass['position']
            m = mass['mass']
            
            # Distance from mass
            r = np.sqrt((x - mx)**2 + (y - my)**2)
            r = np.maximum(r, 10)  # Avoid singularity
            
            # Gravitational field strength (inverse square law)
            field_strength = m / (r**2)
            self.field += field_strength
            
    def paint(self, canvas):
        """Paint gravitational lensing and spacetime curvature"""
        # Normalize field for visualization
        normalized_field = self.field / (np.max(self.field) + 1e-6)
        
        # Create ripples in spacetime
        for y in range(0, HEIGHT, 5):
            for x in range(0, WIDTH, 5):
                field_value = normalized_field[y, x]
                
                if field_value > 0.01:
                    # Warping intensity
                    warp = field_value * 20
                    
                    # Draw curved spacetime grid
                    for angle in np.linspace(0, 2*np.pi, 8):
                        # Distort based on field
                        r = 20 * (1 + field_value)
                        dx = r * np.cos(angle) * (1 + np.sin(warp))
                        dy = r * np.sin(angle) * (1 + np.cos(warp))
                        
                        px, py = int(x + dx), int(y + dy)
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            # Purple gravitational waves
                            intensity = field_value * self.strength
                            canvas[py, px, :3] += np.array(self.color_signature) * intensity * 0.1
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + intensity * 0.1)
        
        # Draw massive objects as bright cores
        for mass in self.masses:
            x, y = int(mass['position'][0]), int(mass['position'][1])
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Accretion disk effect
                for r in range(int(mass['mass']/5), 0, -1):
                    intensity = r / (mass['mass']/5)
                    for angle in np.linspace(0, 2*np.pi, max(20, r*2)):
                        px = int(x + r * np.cos(angle))
                        py = int(y + r * np.sin(angle))
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            # Hot accretion disk colors
                            heat = 1 - r/(mass['mass']/5)
                            rgb = np.array([1.0, 0.5 + 0.5*heat, heat]) * intensity
                            canvas[py, px, :3] += rgb * 0.2
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + intensity * 0.2)
    
    def update(self):
        """Update mass positions (orbital mechanics)"""
        # Simple N-body simulation
        for i, mass1 in enumerate(self.masses):
            force = np.zeros(2)
            
            for j, mass2 in enumerate(self.masses):
                if i != j:
                    # Vector from mass1 to mass2
                    r_vec = mass2['position'] - mass1['position']
                    r = np.linalg.norm(r_vec)
                    
                    if r > 10:
                        # Gravitational force
                        f_mag = mass1['mass'] * mass2['mass'] / (r**2)
                        force += f_mag * r_vec / r
            
            # Update velocity and position
            mass1['velocity'] += force / mass1['mass'] * 0.01
            mass1['velocity'] *= 0.99  # Damping
            mass1['position'] += mass1['velocity']
            
            # Boundary wrapping
            mass1['position'] = mass1['position'] % [WIDTH, HEIGHT]

# Electromagnetism - The Light Painter
class ElectromagneticArtist(ForceArtist):
    def __init__(self):
        super().__init__("electromagnetic", 1.0, (0.3, 0.8, 1.0))  # Electric blue
        self.charges = []
        
        # Place charged particles
        for _ in range(8):
            charge = {
                'position': np.random.rand(2) * [WIDTH, HEIGHT],
                'charge': np.random.choice([-1, 1]) * np.random.uniform(20, 50),
                'velocity': (np.random.rand(2) - 0.5) * 3
            }
            self.charges.append(charge)
    
    def create_field(self):
        """Calculate electric field from all charges"""
        self.e_field_x = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
        self.e_field_y = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
        
        y, x = np.ogrid[0:HEIGHT, 0:WIDTH]
        
        for charge in self.charges:
            cx, cy = charge['position']
            q = charge['charge']
            
            # Vector field components
            dx = x - cx
            dy = y - cy
            r = np.sqrt(dx**2 + dy**2)
            r = np.maximum(r, 5)
            
            # Electric field (inverse square, directional)
            field_mag = q / (r**2)
            self.e_field_x += field_mag * dx / r
            self.e_field_y += field_mag * dy / r
    
    def paint(self, canvas):
        """Paint electric field lines and magnetic interactions"""
        # Draw field lines
        for _ in range(50):
            # Start from random position
            x, y = np.random.rand(2) * [WIDTH, HEIGHT]
            
            # Trace field line
            for step in range(100):
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    # Get field direction at current position
                    ex = self.e_field_x[int(y), int(x)]
                    ey = self.e_field_y[int(y), int(x)]
                    
                    # Normalize
                    e_mag = np.sqrt(ex**2 + ey**2)
                    if e_mag > 0.01:
                        ex /= e_mag
                        ey /= e_mag
                        
                        # Step along field line
                        x += ex * 5
                        y += ey * 5
                        
                        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                            # Color based on field strength
                            intensity = min(1, e_mag * 0.1) * self.strength
                            
                            # Electric blue for positive, orange for negative
                            if ex + ey > 0:
                                rgb = np.array(self.color_signature)
                            else:
                                rgb = np.array([1.0, 0.5, 0.2])
                            
                            canvas[int(y), int(x), :3] += rgb * intensity * 0.1
                            canvas[int(y), int(x), 3] = min(1, canvas[int(y), int(x), 3] + intensity * 0.1)
        
        # Draw charges as glowing orbs
        for charge in self.charges:
            cx, cy = int(charge['position'][0]), int(charge['position'][1])
            
            if 0 <= cx < WIDTH and 0 <= cy < HEIGHT:
                # Charge glow
                radius = int(abs(charge['charge']) / 2)
                for r in range(radius, 0, -1):
                    intensity = (r / radius) ** 2
                    
                    for angle in np.linspace(0, 2*np.pi, max(20, r*3)):
                        px = int(cx + r * np.cos(angle))
                        py = int(cy + r * np.sin(angle))
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            if charge['charge'] > 0:
                                # Positive - bright cyan
                                rgb = np.array([0.5, 1.0, 1.0])
                            else:
                                # Negative - warm orange
                                rgb = np.array([1.0, 0.6, 0.2])
                            
                            canvas[py, px, :3] += rgb * intensity * 0.3
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + intensity * 0.3)
    
    def update(self):
        """Update charge positions (electromagnetic dynamics)"""
        for i, charge1 in enumerate(self.charges):
            force = np.zeros(2)
            
            for j, charge2 in enumerate(self.charges):
                if i != j:
                    r_vec = charge2['position'] - charge1['position']
                    r = np.linalg.norm(r_vec)
                    
                    if r > 5:
                        # Coulomb force (like charges repel, unlike attract)
                        f_mag = charge1['charge'] * charge2['charge'] / (r**2)
                        force -= f_mag * r_vec / r  # Negative for repulsion
            
            # Update motion
            charge1['velocity'] += force / abs(charge1['charge']) * 0.02
            charge1['velocity'] *= 0.98  # Damping
            charge1['position'] += charge1['velocity']
            
            # Boundary reflection
            if charge1['position'][0] < 0 or charge1['position'][0] > WIDTH:
                charge1['velocity'][0] *= -1
            if charge1['position'][1] < 0 or charge1['position'][1] > HEIGHT:
                charge1['velocity'][1] *= -1
            
            charge1['position'] = np.clip(charge1['position'], 0, [WIDTH-1, HEIGHT-1])

# Strong Nuclear Force - The Quantum Binder
class StrongForceArtist(ForceArtist):
    def __init__(self):
        super().__init__("strong", 1.0, (1.0, 0.2, 0.4))  # Quark red
        self.nucleons = []
        
        # Create nucleon clusters
        num_clusters = 3
        for cluster in range(num_clusters):
            center = np.random.rand(2) * [WIDTH, HEIGHT]
            
            # 3-6 nucleons per cluster (like atomic nuclei)
            for _ in range(np.random.randint(3, 7)):
                nucleon = {
                    'position': center + np.random.randn(2) * 20,
                    'color_charge': np.random.choice(['red', 'green', 'blue']),
                    'velocity': np.random.randn(2) * 0.5,
                    'cluster': cluster
                }
                self.nucleons.append(nucleon)
    
    def paint(self, canvas):
        """Paint gluon flux tubes and color confinement"""
        # Draw gluon flux tubes between nucleons
        for i, n1 in enumerate(self.nucleons):
            for j, n2 in enumerate(self.nucleons[i+1:], i+1):
                if n1['cluster'] == n2['cluster']:
                    # Same cluster - strong binding
                    dist = np.linalg.norm(n1['position'] - n2['position'])
                    
                    if dist < 100:  # Strong force is short range
                        # Flux tube strength increases with distance (confinement)
                        strength = min(1, dist / 100) * self.strength
                        
                        # Draw gluon flux tube
                        steps = int(dist)
                        for step in range(steps):
                            t = step / (steps + 1)
                            
                            # Flux tube oscillates
                            oscillation = np.sin(step * 0.2) * 5
                            perpendicular = np.array([-(n2['position'][1] - n1['position'][1]), 
                                                     n2['position'][0] - n1['position'][0]])
                            perpendicular = perpendicular / (np.linalg.norm(perpendicular) + 1e-6)
                            
                            x = n1['position'][0] + t * (n2['position'][0] - n1['position'][0])
                            y = n1['position'][1] + t * (n2['position'][1] - n1['position'][1])
                            
                            x += perpendicular[0] * oscillation
                            y += perpendicular[1] * oscillation
                            
                            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                                # Color based on color charges
                                if n1['color_charge'] == 'red' or n2['color_charge'] == 'red':
                                    rgb = np.array([1.0, 0.2, 0.2])
                                elif n1['color_charge'] == 'green' or n2['color_charge'] == 'green':
                                    rgb = np.array([0.2, 1.0, 0.2])
                                else:
                                    rgb = np.array([0.2, 0.2, 1.0])
                                
                                # Flux tube width
                                for w in range(-2, 3):
                                    px = int(x + perpendicular[0] * w)
                                    py = int(y + perpendicular[1] * w)
                                    
                                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                        fade = np.exp(-abs(w) / 2)
                                        canvas[py, px, :3] += rgb * strength * fade * 0.1
                                        canvas[py, px, 3] = min(1, canvas[py, px, 3] + strength * fade * 0.1)
        
        # Draw nucleons as quarks
        for nucleon in self.nucleons:
            x, y = int(nucleon['position'][0]), int(nucleon['position'][1])
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Quark glow based on color charge
                if nucleon['color_charge'] == 'red':
                    rgb = np.array([1.0, 0.1, 0.1])
                elif nucleon['color_charge'] == 'green':
                    rgb = np.array([0.1, 1.0, 0.1])
                else:  # blue
                    rgb = np.array([0.1, 0.1, 1.0])
                
                # Quantum fuzzy appearance
                for r in range(10, 0, -1):
                    intensity = (r / 10) ** 3  # Rapid falloff
                    
                    for angle in np.linspace(0, 2*np.pi, max(10, r*2)):
                        # Add quantum uncertainty
                        jitter = np.random.randn(2) * 2
                        px = int(x + r * np.cos(angle) + jitter[0])
                        py = int(y + r * np.sin(angle) + jitter[1])
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            canvas[py, px, :3] += rgb * intensity * 0.3
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + intensity * 0.3)
    
    def update(self):
        """Update nucleon positions (confinement dynamics)"""
        for i, nucleon in enumerate(self.nucleons):
            # Calculate forces from other nucleons in same cluster
            force = np.zeros(2)
            
            for j, other in enumerate(self.nucleons):
                if i != j and other['cluster'] == nucleon['cluster']:
                    r_vec = other['position'] - nucleon['position']
                    r = np.linalg.norm(r_vec)
                    
                    if r > 1:
                        # Strong force: attractive at medium range, repulsive at short
                        if r < 10:
                            # Repulsive core
                            force -= 100 * r_vec / (r**3)
                        elif r < 50:
                            # Attractive well
                            force += 10 * r_vec / r
                        else:
                            # Confinement - force increases with distance!
                            force += r * r_vec / 1000
            
            # Update motion
            nucleon['velocity'] += force * 0.01
            nucleon['velocity'] *= 0.95  # Strong damping
            nucleon['position'] += nucleon['velocity']

# Weak Nuclear Force - The Transmuter
class WeakForceArtist(ForceArtist):
    def __init__(self):
        super().__init__("weak", 0.8, (0.8, 0.8, 0.2))  # Decay yellow
        self.particles = []
        
        # Create unstable particles
        for _ in range(20):
            particle = {
                'position': np.random.rand(2) * [WIDTH, HEIGHT],
                'type': np.random.choice(['neutron', 'muon', 'tau']),
                'lifetime': np.random.uniform(50, 200),
                'age': 0,
                'velocity': np.random.randn(2) * 2
            }
            self.particles.append(particle)
    
    def paint(self, canvas):
        """Paint particle decay and transmutation"""
        for particle in self.particles:
            x, y = int(particle['position'][0]), int(particle['position'][1])
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Decay probability visualization
                decay_prob = particle['age'] / particle['lifetime']
                
                # Particle with decay aura
                if particle['type'] == 'neutron':
                    core_rgb = np.array([0.6, 0.6, 0.8])
                elif particle['type'] == 'muon':
                    core_rgb = np.array([0.8, 0.6, 0.8])
                else:  # tau
                    core_rgb = np.array([0.8, 0.8, 0.6])
                
                # Decay aura grows as particle ages
                aura_radius = int(5 + decay_prob * 20)
                
                for r in range(aura_radius, 0, -1):
                    intensity = (1 - r/aura_radius) * (1 - decay_prob)
                    
                    # Aura becomes more yellow as decay approaches
                    rgb = core_rgb * (1 - decay_prob) + np.array(self.color_signature) * decay_prob
                    
                    for angle in np.linspace(0, 2*np.pi, max(10, r)):
                        px = int(x + r * np.cos(angle))
                        py = int(y + r * np.sin(angle))
                        
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            canvas[py, px, :3] += rgb * intensity * 0.1 * self.strength
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + intensity * 0.1)
    
    def update(self):
        """Update particles and handle decay"""
        new_particles = []
        
        for particle in self.particles:
            particle['age'] += 1
            particle['position'] += particle['velocity']
            particle['velocity'] *= 0.99
            
            # Boundary wrapping
            particle['position'] = particle['position'] % [WIDTH, HEIGHT]
            
            # Check for decay
            if particle['age'] > particle['lifetime']:
                # Particle decays! Create decay products
                if particle['type'] == 'neutron':
                    # Neutron -> proton + electron + antineutrino
                    for _ in range(3):
                        decay_product = {
                            'position': particle['position'] + np.random.randn(2) * 10,
                            'type': np.random.choice(['electron', 'neutrino']),
                            'lifetime': np.random.uniform(100, 300),
                            'age': 0,
                            'velocity': np.random.randn(2) * 5  # High energy
                        }
                        new_particles.append(decay_product)
                elif particle['type'] == 'muon':
                    # Muon decay
                    for _ in range(2):
                        decay_product = {
                            'position': particle['position'] + np.random.randn(2) * 5,
                            'type': 'electron',
                            'lifetime': np.random.uniform(150, 250),
                            'age': 0,
                            'velocity': np.random.randn(2) * 4
                        }
                        new_particles.append(decay_product)
            else:
                new_particles.append(particle)
        
        self.particles = new_particles
        
        # Occasionally create new unstable particles
        if len(self.particles) < 30 and np.random.random() < 0.1:
            particle = {
                'position': np.random.rand(2) * [WIDTH, HEIGHT],
                'type': np.random.choice(['neutron', 'muon', 'tau']),
                'lifetime': np.random.uniform(50, 200),
                'age': 0,
                'velocity': np.random.randn(2) * 2
            }
            self.particles.append(particle)

# Create the quantum choreography
print("Initiating quantum choreography...")

# Initialize the force artists
forces = [
    GravityArtist(),
    ElectromagneticArtist(),
    StrongForceArtist(),
    WeakForceArtist()
]

# Let the forces dance together
print("Forces beginning their dance...")

for iteration in range(100):
    # Each force updates its field
    for force in forces:
        if hasattr(force, 'create_field'):
            force.create_field()
    
    # Each force paints its contribution
    for force in forces:
        force.paint(canvas)
    
    # Update dynamics
    for force in forces:
        if hasattr(force, 'update'):
            force.update()
    
    if iteration % 20 == 0:
        print(f"Choreography iteration {iteration}...")

# Add quantum interference where forces overlap
print("Creating quantum interference patterns...")

# Find regions where multiple forces are strong
interference_map = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

for y in range(0, HEIGHT, 10):
    for x in range(0, WIDTH, 10):
        if canvas[y, x, 3] > 0.5:  # High activity region
            # Create interference pattern
            for dy in range(-20, 21):
                for dx in range(-20, 21):
                    py, px = y + dy, x + dx
                    if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                        dist = np.sqrt(dx**2 + dy**2)
                        if dist < 20:
                            # Quantum interference rings
                            interference = np.sin(dist * 0.5) * np.exp(-dist / 20)
                            
                            # Iridescent quantum colors
                            hue = (dist / 20 + canvas[y, x, 0]) % 1
                            rgb = colorsys.hsv_to_rgb(hue, 0.5, abs(interference))
                            
                            canvas[py, px, :3] += np.array(rgb) * 0.05
                            canvas[py, px, 3] = min(1, canvas[py, px, 3] + abs(interference) * 0.05)

# Convert to RGB for saving
canvas_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for c in range(3):
    canvas_rgb[:, :, c] = (np.clip(canvas[:, :, c], 0, 1) * 255).astype(np.uint8)

# Apply alpha as overall brightness
alpha = canvas[:, :, 3]
for c in range(3):
    canvas_rgb[:, :, c] = (canvas_rgb[:, :, c] * np.clip(alpha, 0, 1)).astype(np.uint8)

image = Image.fromarray(canvas_rgb, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_quantum_choreography/quantum_choreography_01.png')

print("Quantum choreography complete.")
print("The fundamental forces have painted their dance.")
print("In their interaction, the universe reveals its artistic nature.")