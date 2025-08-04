from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(5, 5, 15))
draw = ImageDraw.Draw(img, 'RGBA')

# Electromagnetic source class
class EMSource:
    def __init__(self, x, y, charge, frequency):
        self.x = x
        self.y = y
        self.charge = charge  # Positive or negative
        self.frequency = frequency
        self.phase = random.uniform(0, 2 * math.pi)
        self.strength = abs(charge)
        
    def field_at_point(self, px, py, time):
        """Calculate electromagnetic field strength at a point"""
        dx = px - self.x
        dy = py - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 1:
            return (0, 0, 0)
        
        # Electric field decreases with square of distance
        field_magnitude = self.strength / (distance * distance) * 10000
        
        # Add wave component
        wave = math.sin(distance * 0.05 - time * self.frequency + self.phase)
        field_magnitude *= (0.7 + 0.3 * wave)
        
        # Direction away from (positive) or toward (negative) charge
        if self.charge > 0:
            ex = field_magnitude * dx / distance
            ey = field_magnitude * dy / distance
        else:
            ex = -field_magnitude * dx / distance
            ey = -field_magnitude * dy / distance
            
        # Magnetic component (perpendicular to electric)
        bz = field_magnitude * 0.5 * wave
        
        return (ex, ey, bz)

# Gravitational mass class
class GravityWell:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        
    def field_at_point(self, px, py):
        """Calculate gravitational field at a point"""
        dx = px - self.x
        dy = py - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 10:
            distance = 10
            
        # Gravitational field
        field_magnitude = self.mass / (distance * distance) * 5000
        
        # Always attractive (toward mass)
        gx = -field_magnitude * dx / distance
        gy = -field_magnitude * dy / distance
        
        return (gx, gy)

# Create sources
em_sources = []
# Positive charges
for _ in range(3):
    x = random.uniform(WIDTH * 0.2, WIDTH * 0.8)
    y = random.uniform(HEIGHT * 0.2, HEIGHT * 0.8)
    charge = random.uniform(0.5, 1.5)
    freq = random.uniform(0.02, 0.05)
    em_sources.append(EMSource(x, y, charge, freq))

# Negative charges
for _ in range(3):
    x = random.uniform(WIDTH * 0.2, WIDTH * 0.8)
    y = random.uniform(HEIGHT * 0.2, HEIGHT * 0.8)
    charge = random.uniform(-1.5, -0.5)
    freq = random.uniform(0.02, 0.05)
    em_sources.append(EMSource(x, y, -charge, freq))

# Gravity wells
gravity_wells = []
for _ in range(2):
    x = random.uniform(WIDTH * 0.3, WIDTH * 0.7)
    y = random.uniform(HEIGHT * 0.3, HEIGHT * 0.7)
    mass = random.uniform(1, 3)
    gravity_wells.append(GravityWell(x, y, mass))

# Calculate field strengths across canvas
time = 0  # Snapshot in time

# Sample field at grid points
grid_size = 40
x_grid = np.linspace(0, WIDTH, grid_size)
y_grid = np.linspace(0, HEIGHT, grid_size)

# Draw field lines
def draw_field_line(draw, start_x, start_y, field_func, steps=100, step_size=5):
    """Trace a field line from starting point"""
    points = [(start_x, start_y)]
    x, y = start_x, start_y
    
    for _ in range(steps):
        # Get field at current position
        fx, fy = field_func(x, y)
        
        # Normalize
        magnitude = math.sqrt(fx*fx + fy*fy)
        if magnitude < 0.01:
            break
            
        # Step along field direction
        x += step_size * fx / magnitude
        y += step_size * fy / magnitude
        
        # Check bounds
        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            break
            
        points.append((x, y))
    
    return points

# Draw electromagnetic field lines
for source in em_sources:
    # Start field lines in circle around charge
    num_lines = 16
    for i in range(num_lines):
        angle = i * 2 * math.pi / num_lines
        start_x = source.x + 30 * math.cos(angle)
        start_y = source.y + 30 * math.sin(angle)
        
        # Field function for this trace
        def em_field(x, y):
            total_ex, total_ey = 0, 0
            for s in em_sources:
                ex, ey, bz = s.field_at_point(x, y, time)
                total_ex += ex
                total_ey += ey
            return (total_ex, total_ey)
        
        # Trace field line
        field_points = draw_field_line(draw, start_x, start_y, em_field)
        
        # Draw with color based on charge
        if source.charge > 0:
            base_color = (255, 100, 100)  # Red for positive
        else:
            base_color = (100, 100, 255)  # Blue for negative
            
        # Draw field line with fading
        for j in range(len(field_points) - 1):
            progress = j / len(field_points)
            alpha = int(150 * (1 - progress))
            width = int(3 * (1 - progress * 0.5))
            
            color = tuple(int(c * (0.5 + 0.5 * (1 - progress))) for c in base_color) + (alpha,)
            draw.line([field_points[j], field_points[j+1]], fill=color, width=width)

# Draw gravitational field distortion
# Create mesh grid
X, Y = np.meshgrid(np.linspace(0, WIDTH, 50), np.linspace(0, HEIGHT, 50))

# Calculate gravitational potential
potential = np.zeros_like(X)
for well in gravity_wells:
    dx = X - well.x
    dy = Y - well.y
    r = np.sqrt(dx**2 + dy**2)
    r[r < 10] = 10  # Avoid singularity
    potential -= well.mass / r * 1000

# Draw equipotential lines (spacetime curvature)
contour_levels = 20
for level in range(contour_levels):
    value = np.min(potential) + (np.max(potential) - np.min(potential)) * level / contour_levels
    
    # Find contour points
    contour_points = []
    for i in range(potential.shape[0] - 1):
        for j in range(potential.shape[1] - 1):
            # Check if contour crosses this cell
            cell_values = [
                potential[i, j], potential[i+1, j],
                potential[i, j+1], potential[i+1, j+1]
            ]
            
            if min(cell_values) <= value <= max(cell_values):
                # Approximate contour point
                x = X[i, j]
                y = Y[i, j]
                contour_points.append((x, y))
    
    # Draw contour
    if len(contour_points) > 1:
        # Space-time distortion color
        depth = level / contour_levels
        color = (
            int(50 + depth * 50),
            int(100 + depth * 50),
            int(150 + depth * 50),
            int(50 + depth * 30)
        )
        
        for point in contour_points:
            draw.ellipse([point[0]-1, point[1]-1, point[0]+1, point[1]+1], fill=color)

# Draw sources
# EM sources
for source in em_sources:
    # Source glow
    for r in range(30, 5, -5):
        alpha = int(200 * (30 - r) / 30)
        if source.charge > 0:
            color = (255, 150, 150, alpha)
        else:
            color = (150, 150, 255, alpha)
        draw.ellipse([source.x - r, source.y - r, source.x + r, source.y + r], fill=color)
    
    # Core
    symbol = "+" if source.charge > 0 else "-"
    core_color = (255, 200, 200) if source.charge > 0 else (200, 200, 255)
    draw.ellipse([source.x - 10, source.y - 10, source.x + 10, source.y + 10], 
                fill=core_color)

# Gravity wells (black holes)
for well in gravity_wells:
    # Event horizon
    radius = int(20 * well.mass)
    
    # Accretion disk
    for r in range(radius * 3, radius, -2):
        alpha = int(100 * (r - radius) / (radius * 2))
        heat = (r - radius) / (radius * 2)
        
        # Hot accretion disk colors
        color = (
            int(255 * heat),
            int(150 * heat * (1 - heat)),
            int(50 * (1 - heat)),
            alpha
        )
        draw.ellipse([well.x - r, well.y - r, well.x + r, well.y + r], 
                    outline=color, width=2)
    
    # Black hole
    draw.ellipse([well.x - radius, well.y - radius, well.x + radius, well.y + radius],
                fill=(0, 0, 0))

# Add quantum vacuum fluctuations
for _ in range(1000):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    
    # Virtual particle pairs
    if random.random() < 0.5:
        # Particle
        size = random.uniform(0.5, 1.5)
        draw.ellipse([x - size, y - size, x + size, y + size],
                    fill=(200, 200, 255, 50))
    else:
        # Antiparticle
        size = random.uniform(0.5, 1.5)
        draw.ellipse([x - size, y - size, x + size, y + size],
                    fill=(255, 200, 200, 50))

# Wave interference patterns where fields overlap
for i, s1 in enumerate(em_sources):
    for s2 in em_sources[i+1:]:
        # Midpoint between sources
        mid_x = (s1.x + s2.x) / 2
        mid_y = (s1.y + s2.y) / 2
        
        # Distance between sources
        d = math.sqrt((s1.x - s2.x)**2 + (s1.y - s2.y)**2)
        
        if d < 300:  # Close enough for visible interference
            # Draw interference pattern
            for r in range(20, 100, 10):
                for angle in np.linspace(0, 2 * math.pi, 36):
                    x = mid_x + r * math.cos(angle)
                    y = mid_y + r * math.sin(angle)
                    
                    # Calculate phase difference
                    d1 = math.sqrt((x - s1.x)**2 + (y - s1.y)**2)
                    d2 = math.sqrt((x - s2.x)**2 + (y - s2.y)**2)
                    phase_diff = (d1 - d2) * 0.1
                    
                    # Interference intensity
                    intensity = abs(math.cos(phase_diff))
                    
                    if intensity > 0.5:
                        alpha = int(100 * intensity)
                        draw.ellipse([x - 2, y - 2, x + 2, y + 2],
                                   fill=(200, 200, 150, alpha))

img.save('invisible_forces_01.png')
print("Invisible Forces manifested: invisible_forces_01.png")