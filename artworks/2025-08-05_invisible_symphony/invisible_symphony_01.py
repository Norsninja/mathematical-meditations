import numpy as np
from PIL import Image
import math
import colorsys

# Invisible Symphony - Making the Unseen Seen
# A synesthetic landscape where invisible forces paint their presence

WIDTH, HEIGHT = 1080, 1080

# Initialize the sensory canvas
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# Create coordinate grids for field calculations
x_grid, y_grid = np.meshgrid(np.arange(WIDTH), np.arange(HEIGHT))

# Invisible Force 1: Gravity
class GravityWell:
    def __init__(self, x, y, mass):
        self.position = np.array([x, y])
        self.mass = mass
        
    def field_strength(self, x, y):
        """Calculate gravitational field strength at a point"""
        dx = x - self.position[0]
        dy = y - self.position[1]
        r_squared = dx**2 + dy**2 + 1  # +1 to avoid division by zero
        
        # Gravitational field strength falls off with 1/r²
        return self.mass / r_squared
    
    def field_direction(self, x, y):
        """Direction of gravitational pull"""
        dx = x - self.position[0]
        dy = y - self.position[1]
        r = np.sqrt(dx**2 + dy**2 + 1)
        return -dx/r, -dy/r  # Negative because gravity pulls inward
    
    def visualize(self, canvas):
        """Gravity as spacetime curvature - deep blues and purples"""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                strength = self.field_strength(x, y)
                
                if strength > 0.0001:  # Threshold for visibility
                    # Gravity warps space - create distortion rings
                    distance = np.sqrt((x - self.position[0])**2 + (y - self.position[1])**2)
                    
                    # Concentric rings of spacetime distortion
                    ring_pattern = 0.5 + 0.5 * np.sin(distance * 0.05 - strength * 100)
                    
                    # Deep space colors
                    hue = 0.75  # Deep purple-blue
                    saturation = min(1.0, strength * 1000)
                    value = ring_pattern * strength * 500
                    
                    r, g, b = colorsys.hsv_to_rgb(hue, saturation, min(1.0, value))
                    
                    # Add to canvas with warping effect
                    canvas[y, x] += np.array([r, g, b]) * 0.3

# Invisible Force 2: Electromagnetic Fields
class ElectromagneticField:
    def __init__(self, x, y, charge, frequency=0.1):
        self.position = np.array([x, y])
        self.charge = charge  # Positive or negative
        self.frequency = frequency
        self.phase = 0
        
    def field_vector(self, x, y):
        """Calculate E-field vector at a point"""
        dx = x - self.position[0]
        dy = y - self.position[1]
        r_squared = dx**2 + dy**2 + 1
        r = np.sqrt(r_squared)
        
        # Electric field strength
        magnitude = self.charge / r_squared
        
        # Direction (away from positive, toward negative)
        return magnitude * dx/r, magnitude * dy/r
    
    def visualize(self, canvas, time):
        """EM fields as flowing aurora - greens and magentas"""
        self.phase = time * self.frequency
        
        # Create field lines
        num_lines = 24
        for i in range(num_lines):
            angle = (i / num_lines) * 2 * np.pi
            
            # Trace field line
            x, y = self.position[0], self.position[1]
            x += 10 * np.cos(angle)  # Start slightly away from charge
            y += 10 * np.sin(angle)
            
            for step in range(100):
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    # Field pulsates with time
                    pulse = 0.7 + 0.3 * np.sin(self.phase + step * 0.1)
                    
                    # Color based on charge
                    if self.charge > 0:
                        hue = 0.0 + 0.1 * np.sin(step * 0.05)  # Red-orange
                    else:
                        hue = 0.5 + 0.1 * np.sin(step * 0.05)  # Cyan-blue
                    
                    saturation = 0.8
                    value = pulse * (1 - step/100)  # Fade with distance
                    
                    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
                    
                    # Draw with aurora-like glow
                    for dy in range(-3, 4):
                        for dx in range(-3, 4):
                            px, py = int(x + dx), int(y + dy)
                            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                                glow = np.exp(-(dx**2 + dy**2) / 4)
                                canvas[py, px] += np.array([r, g, b]) * glow * 0.1
                
                # Move along field line
                fx, fy = self.field_vector(x, y)
                if self.charge < 0:
                    fx, fy = -fx, -fy  # Reverse for negative charges
                
                # Normalize and step
                magnitude = np.sqrt(fx**2 + fy**2)
                if magnitude > 0:
                    x += 5 * fx / magnitude
                    y += 5 * fy / magnitude
                else:
                    break

# Invisible Force 3: Temperature Gradients
class TemperatureField:
    def __init__(self):
        self.sources = []
        
    def add_source(self, x, y, temperature):
        """Add a heat/cold source"""
        self.sources.append({'pos': np.array([x, y]), 'temp': temperature})
    
    def get_temperature(self, x, y):
        """Calculate temperature at a point from all sources"""
        temp = 20  # Ambient temperature
        
        for source in self.sources:
            distance = np.sqrt((x - source['pos'][0])**2 + (y - source['pos'][1])**2)
            # Temperature diffuses with distance
            contribution = source['temp'] * np.exp(-distance / 100)
            temp += contribution
        
        return temp
    
    def visualize(self, canvas):
        """Temperature as flowing color gradients"""
        # Calculate temperature field
        temp_field = np.zeros((HEIGHT, WIDTH))
        
        for y in range(0, HEIGHT, 4):  # Sample every 4 pixels for efficiency
            for x in range(0, WIDTH, 4):
                temp = self.get_temperature(x, y)
                
                # Fill 4x4 block
                for dy in range(4):
                    for dx in range(4):
                        if y+dy < HEIGHT and x+dx < WIDTH:
                            temp_field[y+dy, x+dx] = temp
        
        # Apply temperature gradient visualization
        for y in range(HEIGHT):
            for x in range(WIDTH):
                temp = temp_field[y, x]
                
                # Map temperature to color
                # Cold: deep blues, Normal: greens, Hot: reds/yellows
                if temp < 20:
                    # Cold
                    normalized = (temp + 50) / 70  # Assuming min temp -50
                    hue = 0.55 + 0.1 * normalized  # Blue range
                    saturation = 0.9
                    value = 0.3 + 0.4 * normalized
                elif temp < 50:
                    # Comfortable
                    normalized = (temp - 20) / 30
                    hue = 0.3 - 0.1 * normalized  # Green to yellow
                    saturation = 0.6
                    value = 0.5 + 0.2 * normalized
                else:
                    # Hot
                    normalized = min(1.0, (temp - 50) / 50)
                    hue = 0.1 - 0.1 * normalized  # Yellow to red
                    saturation = 0.8 + 0.2 * normalized
                    value = 0.7 + 0.3 * normalized
                
                r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
                
                # Blend with existing
                canvas[y, x] = canvas[y, x] * 0.7 + np.array([r, g, b]) * 0.3

# Invisible Force 4: Sound Waves
class SoundWave:
    def __init__(self, x, y, frequency, amplitude):
        self.position = np.array([x, y])
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = 0
        
    def visualize(self, canvas, time):
        """Sound as expanding ripples with frequency-based color"""
        self.phase = time
        
        # Sound waves expand outward
        max_radius = 300
        
        for radius in range(10, max_radius, 15):
            # Wave intensity decreases with distance
            intensity = self.amplitude * (1 - radius/max_radius)
            
            # Higher frequencies = cooler colors, lower = warmer
            hue = 0.8 - 0.6 * (self.frequency / 100)  # Assuming freq 0-100
            
            # Create wave ring
            wave_phase = radius * 0.1 - self.phase * self.frequency * 0.1
            wave_intensity = (1 + np.sin(wave_phase)) / 2
            
            # Draw ring
            for angle in np.linspace(0, 2*np.pi, int(radius * 2)):
                x = self.position[0] + radius * np.cos(angle)
                y = self.position[1] + radius * np.sin(angle)
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    r, g, b = colorsys.hsv_to_rgb(hue, 0.7, intensity * wave_intensity)
                    
                    # Sound creates interference patterns
                    canvas[int(y), int(x)] += np.array([r, g, b]) * 0.2

# Create the invisible symphony
print("Composing the invisible symphony...")

# Gravity wells - the bass notes
gravity_wells = [
    GravityWell(200, 200, 50),
    GravityWell(880, 880, 30),
    GravityWell(540, 540, 70)
]

# Electromagnetic fields - the melody
em_fields = [
    ElectromagneticField(300, 700, 10, 0.2),  # Positive charge
    ElectromagneticField(780, 300, -10, 0.15), # Negative charge
    ElectromagneticField(540, 200, 5, 0.25),   # Smaller positive
    ElectromagneticField(540, 880, -5, 0.18)   # Smaller negative
]

# Temperature field - the atmosphere
temp_field = TemperatureField()
temp_field.add_source(100, 540, 80)   # Heat source (left)
temp_field.add_source(980, 540, -60)  # Cold source (right)
temp_field.add_source(540, 100, 40)   # Warm source (top)
temp_field.add_source(540, 980, -40)  # Cool source (bottom)

# Sound waves - the rhythm
sound_waves = [
    SoundWave(270, 270, 20, 0.8),  # Low frequency
    SoundWave(810, 810, 60, 0.6),  # High frequency
    SoundWave(540, 540, 40, 1.0),  # Medium frequency, high amplitude
]

# Compose the symphony over time
print("The invisible forces begin their dance...")

# First movement - Gravity sets the stage
for well in gravity_wells:
    well.visualize(canvas)

# Second movement - Temperature flows
temp_field.visualize(canvas)

# Third movement - Electromagnetic ballet
for t in range(30):
    for field in em_fields:
        field.visualize(canvas, t)

# Fourth movement - Sound ripples through
for t in range(20):
    for wave in sound_waves:
        wave.visualize(canvas, t)

# Final touch - Interference patterns where forces meet
print("Creating interference patterns...")

# Find regions where multiple forces are strong
interference_map = np.zeros((HEIGHT, WIDTH))

for y in range(0, HEIGHT, 10):
    for x in range(0, WIDTH, 10):
        # Count active forces at this point
        force_count = 0
        
        # Check gravity
        for well in gravity_wells:
            if well.field_strength(x, y) > 0.001:
                force_count += 1
        
        # Check EM fields
        for field in em_fields:
            fx, fy = field.field_vector(x, y)
            if abs(fx) + abs(fy) > 0.01:
                force_count += 1
        
        # Check temperature
        temp = temp_field.get_temperature(x, y)
        if abs(temp - 20) > 10:
            force_count += 1
        
        # More forces = more interference
        if force_count >= 2:
            # Create interference pattern
            for dy in range(-5, 6):
                for dx in range(-5, 6):
                    py, px = y + dy, x + dx
                    if 0 <= py < HEIGHT and 0 <= px < WIDTH:
                        # White light at interference points
                        intensity = 0.1 * force_count / 4
                        canvas[py, px] += np.array([1, 1, 1]) * intensity

# Normalize and save
canvas = np.clip(canvas, 0, 1)

# Add subtle overall glow
canvas = canvas ** 0.9  # Gamma correction for more vivid colors

image_array = (canvas * 255).astype(np.uint8)
image = Image.fromarray(image_array, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_invisible_symphony/invisible_symphony_01.png')

print("Invisible symphony complete.")
print("The unseen forces have painted their presence.")
print("In this landscape, physics becomes poetry.")