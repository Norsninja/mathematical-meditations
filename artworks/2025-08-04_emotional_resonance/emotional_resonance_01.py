import numpy as np
from PIL import Image, ImageDraw
import math
import colorsys

# Emotional Resonance - Where Mathematics Meets Feeling
# Each emotion creates its own wave signature, interfering to create complex patterns

WIDTH, HEIGHT = 1080, 1080

# Create the canvas
image = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
pixels = image.load()

# Emotional wave sources - each with position, frequency, amplitude, and color
emotions = {
    'joy': {
        'centers': [(300, 300), (780, 300)],
        'frequency': 0.08,
        'amplitude': 120,
        'phase': 0,
        'color': (1.0, 0.9, 0.3),  # Golden yellow
        'decay': 0.0008
    },
    'melancholy': {
        'centers': [(540, 540)],
        'frequency': 0.03,
        'amplitude': 150,
        'phase': np.pi/4,
        'color': (0.4, 0.5, 0.9),  # Deep blue
        'decay': 0.0005
    },
    'passion': {
        'centers': [(200, 800), (880, 800)],
        'frequency': 0.12,
        'amplitude': 100,
        'phase': np.pi/2,
        'color': (0.9, 0.3, 0.4),  # Crimson
        'decay': 0.001
    },
    'serenity': {
        'centers': [(540, 200)],
        'frequency': 0.02,
        'amplitude': 80,
        'phase': 0,
        'color': (0.3, 0.8, 0.7),  # Turquoise
        'decay': 0.0003
    },
    'longing': {
        'centers': [(150, 540), (930, 540)],
        'frequency': 0.05,
        'amplitude': 110,
        'phase': 3*np.pi/4,
        'color': (0.7, 0.4, 0.8),  # Purple
        'decay': 0.0006
    }
}

print("Calculating emotional interference patterns...")

# Create numpy arrays for faster computation
wave_field = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
color_field = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# Generate coordinate grids
y_grid, x_grid = np.meshgrid(np.arange(HEIGHT), np.arange(WIDTH), indexing='ij')

# Calculate wave interference for each emotion
for emotion_name, emotion in emotions.items():
    print(f"Processing {emotion_name}...")
    
    emotion_wave = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
    
    for center in emotion['centers']:
        cx, cy = center
        
        # Calculate distance from center for each pixel
        distances = np.sqrt((x_grid - cx)**2 + (y_grid - cy)**2)
        
        # Generate wave with decay
        wave = emotion['amplitude'] * np.exp(-distances * emotion['decay']) * \
               np.sin(distances * emotion['frequency'] + emotion['phase'])
        
        # Add to emotion's total wave
        emotion_wave += wave
    
    # Add to total wave field
    wave_field += emotion_wave
    
    # Add weighted color contribution based on wave amplitude
    for i in range(3):
        color_field[:, :, i] += np.abs(emotion_wave) * emotion['color'][i]

# Normalize the wave field
wave_min = np.min(wave_field)
wave_max = np.max(wave_field)
wave_normalized = (wave_field - wave_min) / (wave_max - wave_min)

# Normalize color field
color_max = np.max(color_field)
if color_max > 0:
    color_field = color_field / color_max

print("Rendering the emotional landscape...")

# Convert to image
for y in range(HEIGHT):
    for x in range(WIDTH):
        # Get normalized wave value
        wave_val = wave_normalized[y, x]
        
        # Get color from emotional contributions
        r, g, b = color_field[y, x]
        
        # Create interference pattern effect
        # Bright regions where waves constructively interfere
        # Dark regions where they destructively interfere
        brightness = 0.3 + 0.7 * wave_val
        
        # Add subtle iridescence based on wave phase
        phase_shift = wave_field[y, x] * 0.01
        hue_shift = math.sin(phase_shift) * 0.1
        
        # Convert to HSV for hue manipulation
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + hue_shift) % 1.0
        s = min(1.0, s * (1.2 - 0.2 * wave_val))  # Desaturate at interference nodes
        v = v * brightness
        
        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
        # Add subtle noise for texture
        noise = np.random.normal(0, 0.02)
        r = max(0, min(1, r + noise))
        g = max(0, min(1, g + noise))
        b = max(0, min(1, b + noise))
        
        pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))

# Add resonance points where multiple emotions strongly interfere
draw = ImageDraw.Draw(image)

# Find local maxima in the wave field
for y in range(10, HEIGHT-10, 20):
    for x in range(10, WIDTH-10, 20):
        local_area = wave_field[y-5:y+5, x-5:x+5]
        if wave_field[y, x] == np.max(local_area) and wave_field[y, x] > 200:
            # Draw a small glowing point
            intensity = min(1.0, wave_field[y, x] / 300)
            for r in range(3, 0, -1):
                alpha = intensity * (r / 3)
                color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

# Save the image
image.save('/home/norsninja/Art/artworks/2025-08-04_emotional_resonance/emotional_resonance_01.png')

print("Emotional resonance complete.")
print("Where waves meet, new feelings emerge.")
print("Mathematics cannot contain emotion, but it can map its echoes.")