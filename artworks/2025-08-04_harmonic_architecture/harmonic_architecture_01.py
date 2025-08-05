import numpy as np
from PIL import Image, ImageDraw
import math
import colorsys

# Harmonic Architecture - Building Visual Music
# Where frequencies become form, where rhythm creates structure

WIDTH, HEIGHT = 1080, 1080

# Create the canvas
image = Image.new('RGB', (WIDTH, HEIGHT), (5, 5, 10))
draw = ImageDraw.Draw(image)

# Musical parameters
FUNDAMENTAL = 55  # A1 in Hz
TEMPO = 120  # BPM
MEASURES = 4
BEATS_PER_MEASURE = 4

# Define a chord progression (in terms of frequency ratios)
chord_progression = [
    # I - Major (1:1, 5:4, 3:2) - tonic
    {'name': 'I', 'ratios': [1, 5/4, 3/2], 'color_base': 0.1},  # Red-orange
    # vi - Minor (1:1, 6:5, 3:2) - relative minor
    {'name': 'vi', 'ratios': [1, 6/5, 3/2], 'color_base': 0.7},  # Blue
    # IV - Major (4:3, 5:3, 2:1) - subdominant
    {'name': 'IV', 'ratios': [4/3, 5/3, 2], 'color_base': 0.3},  # Yellow-green
    # V - Major (3:2, 15:8, 9:4) - dominant
    {'name': 'V', 'ratios': [3/2, 15/8, 9/4], 'color_base': 0.5},  # Cyan
]

# Time parameters
total_beats = MEASURES * BEATS_PER_MEASURE
beat_duration = 60 / TEMPO  # seconds per beat

print("Composing visual music...")

# Create frequency spectrum visualization
spectrum_height = HEIGHT // 4

# Draw background frequency gradient
for y in range(spectrum_height):
    frequency_factor = y / spectrum_height
    color_value = int(10 + 20 * frequency_factor)
    draw.rectangle([(0, y), (WIDTH, y + 1)], fill=(color_value, color_value, color_value + 5))

# Visualize each chord in the progression
chord_width = WIDTH // len(chord_progression)

for chord_idx, chord in enumerate(chord_progression):
    x_start = chord_idx * chord_width
    x_end = x_start + chord_width
    
    print(f"  Rendering chord {chord['name']}...")
    
    # Draw harmonic series for this chord
    for ratio_idx, ratio in enumerate(chord['ratios']):
        frequency = FUNDAMENTAL * ratio
        
        # Map frequency to vertical position (log scale)
        y_pos = spectrum_height - int(spectrum_height * math.log2(ratio + 1) / 3)
        
        # Color based on chord and harmonic
        hue = chord['color_base'] + ratio_idx * 0.1
        saturation = 0.7 - ratio_idx * 0.15
        value = 0.8 - ratio_idx * 0.1
        
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(hue % 1, saturation, value)]
        
        # Draw frequency band
        for x in range(x_start, x_end):
            # Add wave pattern
            wave_offset = int(10 * math.sin(x * frequency / 100))
            y = y_pos + wave_offset
            
            if 0 <= y < spectrum_height:
                # Intensity falls off from center
                distance_from_center = abs(x - (x_start + x_end) / 2) / (chord_width / 2)
                intensity = 1 - distance_from_center ** 2
                
                draw.ellipse([x-2, y-2, x+2, y+2], 
                           fill=(int(r * intensity), int(g * intensity), int(b * intensity)))

# Create rhythmic patterns in the middle section
rhythm_section_y = spectrum_height
rhythm_height = HEIGHT // 2

print("Building rhythmic structures...")

# Define rhythm patterns (1 = hit, 0 = rest)
rhythm_patterns = [
    {'name': 'kick', 'pattern': [1, 0, 0, 0, 1, 0, 0, 0], 'y_offset': 0, 'size': 40, 'color': (100, 50, 50)},
    {'name': 'snare', 'pattern': [0, 0, 1, 0, 0, 0, 1, 0], 'y_offset': 60, 'size': 30, 'color': (150, 150, 100)},
    {'name': 'hihat', 'pattern': [1, 1, 1, 1, 1, 1, 1, 1], 'y_offset': 100, 'size': 15, 'color': (120, 120, 150)},
    {'name': 'accent', 'pattern': [1, 0, 0, 1, 0, 1, 0, 0], 'y_offset': 140, 'size': 25, 'color': (200, 100, 150)},
]

# Calculate beat positions
beat_width = WIDTH / total_beats

for beat in range(total_beats):
    x_center = int(beat * beat_width + beat_width / 2)
    measure = beat // BEATS_PER_MEASURE
    beat_in_measure = beat % BEATS_PER_MEASURE
    
    # Draw measure lines
    if beat_in_measure == 0:
        draw.line([(x_center, rhythm_section_y), (x_center, rhythm_section_y + rhythm_height)],
                 fill=(60, 60, 70), width=2)
    
    # Draw rhythm patterns
    for pattern in rhythm_patterns:
        pattern_idx = beat % len(pattern['pattern'])
        if pattern['pattern'][pattern_idx]:
            y_center = rhythm_section_y + pattern['y_offset']
            
            # Draw rhythm hit with decay
            for r in range(pattern['size'], 0, -2):
                decay = r / pattern['size']
                alpha = decay ** 2
                
                color = tuple(int(c * alpha) for c in pattern['color'])
                
                # Add slight randomness for organic feel
                x_var = x_center + np.random.randint(-2, 3)
                y_var = y_center + np.random.randint(-2, 3)
                
                draw.ellipse([x_var - r, y_var - r, x_var + r, y_var + r],
                           fill=color)

# Create waveform visualization at the bottom
waveform_y = rhythm_section_y + rhythm_height
waveform_height = HEIGHT - waveform_y

print("Synthesizing waveforms...")

# Generate composite waveform
samples = WIDTH * 4  # Oversampling for smooth curves
time = np.linspace(0, total_beats * beat_duration, samples)

# Mix all frequencies from the chord progression
composite_wave = np.zeros(samples)

for t_idx, t in enumerate(time):
    # Determine which chord we're in
    beat_position = (t / beat_duration) % total_beats
    chord_idx = int(beat_position / BEATS_PER_MEASURE) % len(chord_progression)
    chord = chord_progression[chord_idx]
    
    # Sum the frequencies in the chord
    for ratio in chord['ratios']:
        frequency = FUNDAMENTAL * ratio
        # Add envelope for more musical feel
        envelope = math.exp(-0.5 * (beat_position % 1))
        composite_wave[t_idx] += envelope * math.sin(2 * math.pi * frequency * t)

# Normalize waveform
composite_wave = composite_wave / np.max(np.abs(composite_wave))

# Draw waveform
waveform_center = waveform_y + waveform_height // 2

for i in range(0, samples - 4, 4):  # Draw every 4th sample
    x1 = int(i * WIDTH / samples)
    x2 = int((i + 4) * WIDTH / samples)
    
    y1 = waveform_center + int(composite_wave[i] * waveform_height * 0.4)
    y2 = waveform_center + int(composite_wave[min(i + 4, samples - 1)] * waveform_height * 0.4)
    
    # Color based on amplitude
    amplitude = abs(composite_wave[i])
    hue = 0.6 - amplitude * 0.2  # Blue to green
    saturation = 0.5 + amplitude * 0.5
    value = 0.3 + amplitude * 0.7
    
    r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
    
    draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=2)

# Add frequency relationship lines
print("Drawing harmonic relationships...")

for i in range(len(chord_progression)):
    for j in range(i + 1, len(chord_progression)):
        chord1 = chord_progression[i]
        chord2 = chord_progression[j]
        
        # Find common tones
        for r1 in chord1['ratios']:
            for r2 in chord2['ratios']:
                if abs(r1 - r2) < 0.01:  # Common tone
                    x1 = i * chord_width + chord_width // 2
                    x2 = j * chord_width + chord_width // 2
                    
                    # Draw connecting arc
                    for t in np.linspace(0, 1, 50):
                        x = x1 + (x2 - x1) * t
                        y = spectrum_height // 2 - int(100 * math.sin(math.pi * t))
                        
                        draw.ellipse([x-1, y-1, x+1, y+1], fill=(100, 100, 150, 100))

# Save the image
image.save('/home/norsninja/Art/artworks/2025-08-04_harmonic_architecture/harmonic_architecture_01.png')

print("Harmonic architecture complete.")
print("Music is mathematics in time; this image is time collapsed into space.")
print("Each frequency has found its color, each rhythm its form.")