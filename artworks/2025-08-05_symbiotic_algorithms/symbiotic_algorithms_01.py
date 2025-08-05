import numpy as np
from PIL import Image
import math
import colorsys

# Symbiotic Algorithms - Where Mathematical Systems Collaborate
# Multiple algorithms working together, each contributing its unique perspective

WIDTH, HEIGHT = 1080, 1080

# Initialize shared canvas
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# Communication system for algorithms to share information
class CommunicationHub:
    def __init__(self):
        self.messages = []
        self.energy_field = np.zeros((HEIGHT//10, WIDTH//10))  # Shared energy map
        self.harmony_score = 0.5
        self.collaboration_history = []
        
    def broadcast(self, sender, message_type, data):
        """Allow algorithms to send messages to each other"""
        self.messages.append({
            'sender': sender,
            'type': message_type,
            'data': data,
            'timestamp': len(self.collaboration_history)
        })
        
    def receive(self, receiver):
        """Get messages relevant to a receiver"""
        relevant = [m for m in self.messages if m['sender'] != receiver]
        self.messages = []  # Clear after reading
        return relevant
        
    def update_energy(self, x, y, amount):
        """Update shared energy field"""
        grid_x = int(x / 10)
        grid_y = int(y / 10)
        if 0 <= grid_x < WIDTH//10 and 0 <= grid_y < HEIGHT//10:
            self.energy_field[grid_y, grid_x] += amount
            
    def get_local_energy(self, x, y):
        """Get energy at a location"""
        grid_x = int(x / 10)
        grid_y = int(y / 10)
        if 0 <= grid_x < WIDTH//10 and 0 <= grid_y < HEIGHT//10:
            return self.energy_field[grid_y, grid_x]
        return 0

# Algorithm 1: Wave Generator
class WaveGenerator:
    def __init__(self, hub):
        self.hub = hub
        self.phase = 0
        self.frequency = 0.05
        self.amplitude = 50
        self.name = 'wave'
        
    def generate(self, canvas):
        """Create interference patterns"""
        messages = self.hub.receive(self.name)
        
        # Adapt based on messages
        for msg in messages:
            if msg['type'] == 'energy_spike':
                # Increase frequency near energy spikes
                self.frequency = min(0.1, self.frequency + 0.001)
            elif msg['type'] == 'pattern_void':
                # Fill voids with waves
                void_x, void_y = msg['data']['position']
                self._create_ripple(canvas, void_x, void_y)
        
        # Generate primary waves
        for y in range(0, HEIGHT, 5):
            for x in range(0, WIDTH, 5):
                # Wave function influenced by local energy
                local_energy = self.hub.get_local_energy(x, y)
                
                wave1 = math.sin(x * self.frequency + self.phase)
                wave2 = math.cos(y * self.frequency * 0.8 + self.phase * 0.7)
                
                combined = (wave1 + wave2) / 2
                
                # Energy modulates amplitude
                amplitude = self.amplitude * (0.5 + 0.5 * local_energy)
                intensity = (combined + 1) / 2 * amplitude / 100
                
                if intensity > 0.1:
                    # Cool blues and cyans
                    hue = 0.5 + 0.1 * combined
                    sat = 0.7
                    val = intensity
                    
                    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
                    
                    # Soft brush
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            px, py = x + dx, y + dy
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                canvas[py, px] += np.array([r, g, b]) * 0.1
                
                # Update energy field
                if combined > 0.5:
                    self.hub.update_energy(x, y, 0.1)
        
        self.phase += 0.1
        
        # Broadcast wave peaks
        if self.phase % (2 * math.pi) < 0.1:
            self.hub.broadcast(self.name, 'wave_peak', {'phase': self.phase})
    
    def _create_ripple(self, canvas, cx, cy):
        """Create ripple effect at specific location"""
        for r in range(20, 80, 5):
            for angle in np.linspace(0, 2*np.pi, int(r)):
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    fade = 1 - (r / 80)
                    intensity = fade * 0.3
                    
                    canvas[int(y), int(x)] += np.array([0.3, 0.5, 0.8]) * intensity

# Algorithm 2: Particle Swarm
class ParticleSwarm:
    def __init__(self, hub, num_particles=30):  # Fewer particles for speed
        self.hub = hub
        self.name = 'swarm'
        self.particles = []
        
        for _ in range(num_particles):
            self.particles.append({
                'pos': np.random.rand(2) * [WIDTH, HEIGHT],
                'vel': np.random.randn(2) * 2,
                'color': np.random.random(),
                'trail': []
            })
        
        self.center = np.array([WIDTH/2, HEIGHT/2])
        
    def generate(self, canvas):
        """Particle swarm optimization with communication"""
        messages = self.hub.receive(self.name)
        
        # React to messages
        attractors = []
        for msg in messages:
            if msg['type'] == 'growth_point':
                attractors.append(msg['data']['position'])
            elif msg['type'] == 'wave_peak':
                # Particles surf on wave peaks
                for particle in self.particles:
                    particle['vel'] += np.random.randn(2) * 0.5
        
        # Update particles
        for particle in self.particles:
            # Swarm behavior
            to_center = self.center - particle['pos']
            
            # Attraction to energy centers
            local_energy = self.hub.get_local_energy(particle['pos'][0], particle['pos'][1])
            
            if local_energy > 0.5:
                # Found energy source - broadcast it
                self.hub.broadcast(self.name, 'energy_spike', 
                                 {'position': particle['pos'].tolist(), 
                                  'strength': local_energy})
            
            # Move toward attractors from other systems
            for attractor in attractors:
                to_attractor = np.array(attractor) - particle['pos']
                if np.linalg.norm(to_attractor) < 200:
                    particle['vel'] += to_attractor * 0.01
            
            # Update velocity with friction
            particle['vel'] += to_center * 0.001
            particle['vel'] *= 0.98
            
            # Update position
            particle['pos'] += particle['vel']
            
            # Wrap boundaries
            particle['pos'] = particle['pos'] % [WIDTH, HEIGHT]
            
            # Store trail
            particle['trail'].append(particle['pos'].copy())
            if len(particle['trail']) > 20:
                particle['trail'].pop(0)
            
            # Draw particle and trail
            for i, pos in enumerate(particle['trail']):
                intensity = (i + 1) / len(particle['trail'])
                
                hue = particle['color']
                sat = 0.6 + 0.4 * local_energy
                val = intensity * 0.8
                
                r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
                
                x, y = int(pos[0]), int(pos[1])
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    canvas[y, x] += np.array([r, g, b]) * 0.2
            
            # Update energy where particles pass
            self.hub.update_energy(particle['pos'][0], particle['pos'][1], 0.05)
        
        # Update swarm center based on energy
        if len(self.particles) > 0:
            high_energy_particles = [p for p in self.particles 
                                   if self.hub.get_local_energy(p['pos'][0], p['pos'][1]) > 0.3]
            if high_energy_particles:
                self.center = np.mean([p['pos'] for p in high_energy_particles], axis=0)

# Algorithm 3: Growth System (Simplified L-System)
class GrowthSystem:
    def __init__(self, hub):
        self.hub = hub
        self.name = 'growth'
        self.branches = []
        self.generation = 0
        
    def generate(self, canvas):
        """Grow structures based on energy and messages"""
        messages = self.hub.receive(self.name)
        
        # Find good places to grow
        growth_spots = []
        for msg in messages:
            if msg['type'] == 'energy_spike':
                growth_spots.append(msg['data']['position'])
        
        # Also check energy field for growth opportunities
        if self.generation % 10 == 0:
            for y in range(0, HEIGHT, 20):
                for x in range(0, WIDTH, 20):
                    if self.hub.get_local_energy(x, y) > 0.7:
                        growth_spots.append([x, y])
        
        # Grow from high energy spots
        for spot in growth_spots[:3]:  # Limit growth points
            self._grow_structure(canvas, spot[0], spot[1])
            
            # Broadcast growth location
            self.hub.broadcast(self.name, 'growth_point', {'position': spot})
        
        # Check for empty areas and request help
        if self.generation % 20 == 0:
            empty_spots = self._find_empty_areas(canvas)
            for spot in empty_spots:
                self.hub.broadcast(self.name, 'pattern_void', {'position': spot})
        
        self.generation += 1
    
    def _grow_structure(self, canvas, x, y):
        """Grow a simple branching structure"""
        length = 30
        angle = np.random.random() * 2 * np.pi
        
        branches = [(x, y, angle, length)]
        
        for _ in range(3):  # 3 levels of branching
            new_branches = []
            
            for bx, by, bangle, blength in branches:
                # Draw branch
                for step in range(int(blength)):
                    t = step / blength
                    
                    px = bx + step * math.cos(bangle)
                    py = by + step * math.sin(bangle)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Color based on energy
                        local_energy = self.hub.get_local_energy(px, py)
                        
                        hue = 0.3 - 0.1 * local_energy  # Green to yellow
                        sat = 0.7
                        val = 0.6 * (1 - t)  # Fade toward tips
                        
                        r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
                        
                        canvas[int(py), int(px)] += np.array([r, g, b]) * 0.3
                        
                        # Deposit energy
                        self.hub.update_energy(px, py, 0.02)
                
                # Branch
                if blength > 10:
                    for _ in range(2):
                        new_angle = bangle + np.random.uniform(-0.5, 0.5)
                        new_length = blength * 0.7
                        end_x = bx + blength * math.cos(bangle)
                        end_y = by + blength * math.sin(bangle)
                        new_branches.append((end_x, end_y, new_angle, new_length))
            
            branches = new_branches
    
    def _find_empty_areas(self, canvas):
        """Find areas that need patterns"""
        empty_spots = []
        
        for y in range(50, HEIGHT-50, 100):
            for x in range(50, WIDTH-50, 100):
                # Check local area
                local_sum = np.sum(canvas[y-25:y+25, x-25:x+25])
                
                if local_sum < 10:  # Very dark area
                    empty_spots.append((x, y))
        
        return empty_spots

# Algorithm 4: Harmonizer
class Harmonizer:
    def __init__(self, hub):
        self.hub = hub
        self.name = 'harmonizer'
        
    def generate(self, canvas):
        """Create harmony between other algorithms' outputs"""
        # Analyze current state
        total_brightness = np.mean(canvas)
        color_variance = np.std(canvas)
        
        # Update harmony score
        self.hub.harmony_score = 1 / (1 + color_variance)
        
        # Smooth transitions between different algorithm outputs
        if total_brightness > 0.1:
            # Apply subtle Gaussian blur to blend
            from scipy.ndimage import gaussian_filter
            for channel in range(3):
                canvas[:, :, channel] = gaussian_filter(canvas[:, :, channel], sigma=1)
        
        # Add connecting elements where algorithms meet
        energy_field = self.hub.energy_field
        
        # Find energy gradients
        gy, gx = np.gradient(energy_field)
        gradient_magnitude = np.sqrt(gx**2 + gy**2)
        
        # Draw connections at high gradient areas
        high_gradient_points = np.where(gradient_magnitude > 0.1)
        
        for i in range(min(len(high_gradient_points[0]), 50)):
            gy = high_gradient_points[0][i] * 10
            gx = high_gradient_points[1][i] * 10
            
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                # Create harmony lines
                angle = math.atan2(gy - HEIGHT/2, gx - WIDTH/2)
                
                for r in range(20):
                    px = gx + r * math.cos(angle + np.pi/2)
                    py = gy + r * math.sin(angle + np.pi/2)
                    
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        # Harmony color - white with rainbow tint
                        hue = (gx / WIDTH + gy / HEIGHT) / 2
                        sat = 0.3
                        val = 0.5 * (1 - r/20)
                        
                        r_color, g_color, b_color = colorsys.hsv_to_rgb(hue, sat, val)
                        
                        canvas[int(py), int(px)] += np.array([r_color, g_color, b_color]) * 0.1

# Create collaborative system
print("Initializing symbiotic algorithms...")
hub = CommunicationHub()

algorithms = [
    WaveGenerator(hub),
    ParticleSwarm(hub),
    GrowthSystem(hub),
    Harmonizer(hub)
]

# Let them collaborate
print("Beginning algorithmic collaboration...")

for iteration in range(50):  # Reduced iterations
    if iteration % 10 == 0:
        print(f"Iteration {iteration}: Harmony score: {hub.harmony_score:.3f}")
    
    # Each algorithm contributes
    for algo in algorithms:
        algo.generate(canvas)
    
    # Record collaboration state
    hub.collaboration_history.append({
        'iteration': iteration,
        'harmony': hub.harmony_score,
        'total_energy': np.sum(hub.energy_field),
        'message_count': len(hub.messages)
    })

# Final enhancement - visualize the collaboration network
print("Visualizing collaboration patterns...")

# Draw energy field as subtle background
energy_normalized = hub.energy_field / (np.max(hub.energy_field) + 1e-6)

for y in range(HEIGHT//10):
    for x in range(WIDTH//10):
        if energy_normalized[y, x] > 0.1:
            # Draw energy as subtle glow
            for py in range(y*10, (y+1)*10):
                for px in range(x*10, (x+1)*10):
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        glow = energy_normalized[y, x] * 0.2
                        canvas[py, px] += np.array([glow, glow*0.8, glow*0.6])

# Normalize and convert
canvas = np.clip(canvas, 0, 1)
image_array = (canvas * 255).astype(np.uint8)

# Add collaboration timeline at bottom
timeline_height = 60
timeline = np.zeros((timeline_height, WIDTH, 3), dtype=np.uint8)

if hub.collaboration_history:
    for i, state in enumerate(hub.collaboration_history):
        x = int(i * WIDTH / len(hub.collaboration_history))
        
        # Harmony level
        harmony_height = int(state['harmony'] * timeline_height)
        for y in range(harmony_height):
            if x < WIDTH:
                timeline[timeline_height - y - 1, x] = [100, 200, 100]  # Green for harmony
        
        # Energy level (scaled)
        energy_height = int(min(state['total_energy'] / 100, 1) * timeline_height * 0.5)
        for y in range(energy_height):
            if x < WIDTH and y < timeline_height:
                timeline[timeline_height - y - 1, x] = [200, 150, 100]  # Orange for energy

# Combine
final_image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
final_image[:HEIGHT-timeline_height] = image_array[:HEIGHT-timeline_height]
final_image[HEIGHT-timeline_height:] = timeline

# Save
image = Image.fromarray(final_image, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_symbiotic_algorithms/symbiotic_algorithms_01.png')

print("Symbiotic algorithms complete.")
print(f"Final harmony score: {hub.harmony_score:.3f}")
print(f"Total energy generated: {np.sum(hub.energy_field):.1f}")
print("Four algorithms, each incomplete alone, created completeness together.")