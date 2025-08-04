import numpy as np
from PIL import Image
import math

# Chromatic Equations - Where Mathematics Paints
# Each pixel's color determined by its position in mathematical space

WIDTH, HEIGHT = 1080, 1080

# Create array for the image
image_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

print("Solving chromatic equations...")

# Create coordinate grids normalized to [-1, 1]
x_grid = np.linspace(-1, 1, WIDTH)
y_grid = np.linspace(-1, 1, HEIGHT)
X, Y = np.meshgrid(x_grid, y_grid)

# Convert to polar coordinates
R = np.sqrt(X**2 + Y**2)
THETA = np.arctan2(Y, X)

# Mathematical functions for each color channel
# Red channel - combination of radial and angular functions
red_function = np.sin(5 * R) * np.cos(3 * THETA) + \
               0.5 * np.sin(R * 10 + THETA * 2)

# Green channel - different frequency relationships
green_function = np.cos(4 * R) * np.sin(5 * THETA) + \
                 0.3 * np.sin(R * 8 - THETA * 3) * np.cos(R * 2)

# Blue channel - complex interference patterns
blue_function = np.sin(6 * R + THETA) * np.cos(2 * R - THETA) + \
                0.4 * np.sin((X + Y) * 5) * np.cos((X - Y) * 5)

# Add interference between channels
interference = 0.2 * np.sin(10 * (red_function + green_function + blue_function))

# Apply transformations
red_transformed = red_function + interference * np.cos(THETA * 4)
green_transformed = green_function + interference * np.sin(THETA * 3)
blue_transformed = blue_function + interference * np.cos(THETA * 5)

# Create smooth transitions using additional functions
# Distance-based modulation
distance_mod = np.exp(-R**2 * 0.5)  # Gaussian falloff from center

# Angular modulation
angular_mod = 0.5 + 0.5 * np.sin(THETA * 6)

# Apply modulations
red_final = red_transformed * (0.7 + 0.3 * distance_mod) * (0.8 + 0.2 * angular_mod)
green_final = green_transformed * (0.6 + 0.4 * distance_mod) * (0.9 + 0.1 * angular_mod)
blue_final = blue_transformed * (0.8 + 0.2 * distance_mod) * (0.7 + 0.3 * angular_mod)

# Normalize to [0, 1] range
def normalize_channel(channel):
    """Normalize array to 0-1 range with enhanced contrast"""
    min_val = np.min(channel)
    max_val = np.max(channel)
    
    if max_val > min_val:
        normalized = (channel - min_val) / (max_val - min_val)
        # Apply sigmoid for smoother transitions
        normalized = 1 / (1 + np.exp(-6 * (normalized - 0.5)))
        return normalized
    return channel

red_normalized = normalize_channel(red_final)
green_normalized = normalize_channel(green_final)
blue_normalized = normalize_channel(blue_final)

print("Applying chromatic transformations...")

# Add subtle noise for organic feel
noise_scale = 0.02
red_normalized += np.random.normal(0, noise_scale, red_normalized.shape)
green_normalized += np.random.normal(0, noise_scale, green_normalized.shape)
blue_normalized += np.random.normal(0, noise_scale, blue_normalized.shape)

# Clip values and convert to uint8
image_array[:, :, 0] = np.clip(red_normalized * 255, 0, 255).astype(np.uint8)
image_array[:, :, 1] = np.clip(green_normalized * 255, 0, 255).astype(np.uint8)
image_array[:, :, 2] = np.clip(blue_normalized * 255, 0, 255).astype(np.uint8)

# Add mathematical structure overlays
print("Adding geometric harmonics...")

# Create geometric overlay
overlay = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# Concentric circles with varying opacity
for i in range(1, 8):
    radius = i * 0.15
    circle_mask = np.abs(R - radius) < 0.005
    
    # Color based on radius
    hue = i / 8
    if hue < 0.33:
        color = [1 - hue * 3, hue * 3, 0]
    elif hue < 0.67:
        color = [0, 1 - (hue - 0.33) * 3, (hue - 0.33) * 3]
    else:
        color = [(hue - 0.67) * 3, 0, 1 - (hue - 0.67) * 3]
    
    overlay[circle_mask] = color

# Radial lines
for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
    line_mask = np.abs(THETA - angle) < 0.01
    overlay[line_mask] = [0.3, 0.3, 0.3]

# Blend overlay with main image
alpha = 0.15  # Overlay transparency
for c in range(3):
    image_array[:, :, c] = np.clip(
        image_array[:, :, c] * (1 - alpha) + overlay[:, :, c] * alpha * 255,
        0, 255
    ).astype(np.uint8)

# Add central focal point
center_x, center_y = WIDTH // 2, HEIGHT // 2
for r in range(30, 0, -1):
    mask = R < (r / WIDTH)
    brightness = (30 - r) / 30
    
    for c in range(3):
        image_array[mask, c] = np.clip(
            image_array[mask, c] + brightness * 30,
            0, 255
        ).astype(np.uint8)

# Create and save the image
image = Image.fromarray(image_array, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-04_chromatic_equations/chromatic_equations_01.png')

print("Chromatic equations complete.")
print("Mathematics doesn't just describe color - it creates it.")
print("Each hue emerges from the interplay of functions in space.")