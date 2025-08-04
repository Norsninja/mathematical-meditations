from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(10, 10, 15))
draw = ImageDraw.Draw(img, 'RGBA')

# Sound wave class
class SoundWave:
    def __init__(self, frequency, amplitude, phase, origin):
        self.frequency = frequency  # Hz
        self.amplitude = amplitude
        self.phase = phase
        self.origin = origin  # (x, y) tuple
        self.wavelength = 343 / frequency  # Speed of sound / frequency
        self.color_map = self.frequency_to_color()
        
    def frequency_to_color(self):
        """Map frequency to color using synesthetic principles"""
        # Map frequency to visible spectrum
        # Low frequencies = red, high frequencies = violet
        
        # Human hearing range: 20Hz - 20kHz
        # Map to hue: 0 (red) to 0.75 (violet)
        normalized_freq = math.log10(self.frequency / 20) / math.log10(1000)  # 0 to 1
        hue = 0.75 - normalized_freq * 0.75  # Reverse so low=red, high=violet
        
        return hue

    def get_amplitude_at_point(self, x, y, time):
        """Calculate wave amplitude at a given point and time"""
        dx = x - self.origin[0]
        dy = y - self.origin[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Wave equation: A * sin(kr - wt + φ)
        # k = 2π/λ (wave number)
        # w = 2πf (angular frequency)
        k = 2 * math.pi / (self.wavelength * 50)  # Scale for visualization
        w = 2 * math.pi * self.frequency / 1000  # Scale time
        
        # Add damping with distance
        damping = math.exp(-distance / 500)
        
        amplitude = self.amplitude * damping * math.sin(k * distance - w * time + self.phase)
        
        return amplitude

# Musical chord - multiple frequencies
def create_chord(root_freq, chord_type='major'):
    """Create a musical chord from root frequency"""
    waves = []
    
    # Frequency ratios for different intervals
    if chord_type == 'major':
        ratios = [1, 5/4, 3/2]  # Root, major third, perfect fifth
    elif chord_type == 'minor':
        ratios = [1, 6/5, 3/2]  # Root, minor third, perfect fifth
    elif chord_type == 'diminished':
        ratios = [1, 6/5, 64/45]  # Root, minor third, diminished fifth
    else:  # augmented
        ratios = [1, 5/4, 8/5]  # Root, major third, augmented fifth
    
    # Create waves for each note in chord
    for i, ratio in enumerate(ratios):
        freq = root_freq * ratio
        amplitude = 1.0 / (i + 1)  # Decreasing amplitude for higher notes
        phase = random.uniform(0, 2 * math.pi)
        
        # Different origins for spatial effect
        angle = i * 2 * math.pi / len(ratios)
        radius = 150
        x = WIDTH/2 + radius * math.cos(angle)
        y = HEIGHT/2 + radius * math.sin(angle)
        
        waves.append(SoundWave(freq, amplitude, phase, (x, y)))
    
    return waves

# Create multiple sound sources
all_waves = []

# Central major chord - C major (261.63 Hz)
central_chord = create_chord(261.63, 'major')
all_waves.extend(central_chord)

# Surrounding minor chords
minor_positions = [(200, 200), (880, 200), (200, 880), (880, 880)]
for pos in minor_positions:
    # Different root notes for variety
    root = random.choice([220, 293.66, 349.23, 392])  # A3, D4, F4, G4
    chord = create_chord(root, 'minor')
    # Reposition waves
    for wave in chord:
        wave.origin = (pos[0] + random.uniform(-50, 50), 
                      pos[1] + random.uniform(-50, 50))
    all_waves.extend(chord)

# Single high frequency overtones
for _ in range(5):
    freq = random.uniform(800, 2000)
    x = random.uniform(100, WIDTH - 100)
    y = random.uniform(100, HEIGHT - 100)
    wave = SoundWave(freq, 0.3, random.uniform(0, 2 * math.pi), (x, y))
    all_waves.append(wave)

# Visualize the acoustic field
time = 5  # Moment in time

# Create interference pattern
resolution = 3  # Sample every N pixels for performance
for x in range(0, WIDTH, resolution):
    for y in range(0, HEIGHT, resolution):
        # Sum all wave contributions
        total_amplitude = 0
        weighted_hue = 0
        total_weight = 0
        
        for wave in all_waves:
            amp = wave.get_amplitude_at_point(x, y, time)
            total_amplitude += amp
            
            # Weight color by amplitude
            weight = abs(amp)
            weighted_hue += wave.color_map * weight
            total_weight += weight
        
        if total_weight > 0:
            # Average hue weighted by amplitude
            avg_hue = weighted_hue / total_weight
            
            # Amplitude determines brightness and saturation
            normalized_amp = math.tanh(abs(total_amplitude))  # Compress to 0-1
            
            saturation = 0.5 + 0.5 * normalized_amp
            value = 0.2 + 0.8 * normalized_amp
            
            # Convert to RGB
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(avg_hue, saturation, value)]
            
            # Draw pixel block
            draw.rectangle([x, y, x + resolution, y + resolution], 
                         fill=(r, g, b))

# Add wave sources as glowing points
for wave in all_waves:
    x, y = wave.origin
    
    # Glow based on frequency
    hue = wave.color_map
    
    # Multiple glow layers
    for radius in range(30, 5, -5):
        alpha = int(150 * (30 - radius) / 30 * wave.amplitude)
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.8, 0.9)]
        
        draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                    fill=(r, g, b, alpha))
    
    # Core
    draw.ellipse([x - 5, y - 5, x + 5, y + 5],
                fill=(255, 255, 255, 200))

# Add circular wave fronts for major visualization
for wave in all_waves[:3]:  # Just the central chord
    x, y = wave.origin
    
    # Draw expanding circles
    for i in range(5):
        radius = (i + 1) * wave.wavelength * 20  # Scale for visibility
        
        if radius < 500:  # Don't draw too large
            alpha = int(100 * (1 - i / 5) * wave.amplitude)
            hue = wave.color_map
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.6, 0.8)]
            
            # Draw circle
            draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                        outline=(r, g, b, alpha), width=2)

# Add standing wave patterns at nodal lines
# Find points of constructive/destructive interference
nodal_points = []
for x in range(0, WIDTH, 20):
    for y in range(0, HEIGHT, 20):
        # Check if this is a nodal point (destructive interference)
        total = sum(w.get_amplitude_at_point(x, y, time) for w in all_waves[:6])
        
        if abs(total) < 0.1:  # Near zero amplitude
            nodal_points.append((x, y))

# Connect nearby nodal points
for i, p1 in enumerate(nodal_points):
    for p2 in nodal_points[i+1:]:
        dist = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
        if dist < 50:  # Close enough to connect
            draw.line([p1, p2], fill=(100, 100, 150, 50), width=1)

# Add resonance visualization - Chladni patterns
# Areas of maximum vibration
for x in range(0, WIDTH, 10):
    for y in range(0, HEIGHT, 10):
        # Calculate total energy at this point
        energy = sum(w.get_amplitude_at_point(x, y, time)**2 for w in all_waves)
        
        if energy > 2:  # High energy regions
            size = min(5, energy)
            intensity = min(255, int(energy * 50))
            
            # Golden particles at resonance points
            draw.ellipse([x - size, y - size, x + size, y + size],
                        fill=(255, 220, 100, intensity))

# Final atmospheric touches
# Add subtle noise for texture
pixels = img.load()
for x in range(0, WIDTH, 4):
    for y in range(0, HEIGHT, 4):
        if random.random() < 0.05:
            r, g, b = pixels[x, y]
            noise = random.randint(-20, 20)
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise))
            )

# Apply slight blur for smoothness
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

img.save('acoustic_mandala_01.png')
print("Acoustic Mandala created: acoustic_mandala_01.png")