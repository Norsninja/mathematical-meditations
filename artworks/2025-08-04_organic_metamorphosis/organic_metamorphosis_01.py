import numpy as np
from PIL import Image
import colorsys

# Organic Metamorphosis - Reaction-Diffusion Exploration
# Where chemistry becomes art, where mathematics breathes

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Gray-Scott reaction-diffusion parameters
# These control the pattern formation
DA = 1.0    # Diffusion rate of chemical A
DB = 0.5    # Diffusion rate of chemical B
FEED = 0.055  # Feed rate (how fast A is added)
KILL = 0.062  # Kill rate (how fast B is removed)

# Initialize chemical concentrations
A = np.ones((HEIGHT, WIDTH), dtype=np.float32)
B = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

# Seed the reaction with random spots
np.random.seed(42)
for _ in range(20):
    x = np.random.randint(20, WIDTH-20)
    y = np.random.randint(20, HEIGHT-20)
    size = np.random.randint(5, 15)
    
    # Create circular seeds
    yy, xx = np.ogrid[:HEIGHT, :WIDTH]
    mask = (xx - x)**2 + (yy - y)**2 <= size**2
    B[mask] = 1.0

# Laplacian convolution weights for diffusion
laplacian_kernel = np.array([[0.05, 0.2, 0.05],
                            [0.2, -1.0, 0.2],
                            [0.05, 0.2, 0.05]], dtype=np.float32)

def laplacian(matrix):
    """Calculate the Laplacian using convolution"""
    # Pad the matrix to handle edges
    padded = np.pad(matrix, 1, mode='edge')
    result = np.zeros_like(matrix)
    
    # Apply convolution
    for i in range(3):
        for j in range(3):
            result += laplacian_kernel[i, j] * padded[i:i+HEIGHT, j:j+WIDTH]
    
    return result

# Time evolution
print("Beginning metamorphosis...")
for iteration in range(2000):  # Reduced iterations for faster generation
    if iteration % 200 == 0:
        print(f"Iteration {iteration}: Patterns forming...")
    
    # Calculate Laplacians
    LA = laplacian(A)
    LB = laplacian(B)
    
    # Reaction-diffusion equations
    reaction = A * B * B
    
    # Update concentrations
    A += (DA * LA - reaction + FEED * (1 - A)) * 0.9
    B += (DB * LB + reaction - (KILL + FEED) * B) * 0.9
    
    # Keep values in valid range
    A = np.clip(A, 0, 1)
    B = np.clip(B, 0, 1)

print("Rendering the emergence...")

# Create the final image
image_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

# Map concentrations to colors
# Using a color scheme inspired by deep ocean life
for y in range(HEIGHT):
    for x in range(WIDTH):
        # Get concentration values
        a_val = A[y, x]
        b_val = B[y, x]
        
        # Create organic color mapping
        # High B concentration: bioluminescent blues and greens
        # Transition zones: purple and pink
        # High A concentration: deep ocean darkness
        
        if b_val > 0.5:
            # Bioluminescent regions
            hue = 0.5 + 0.1 * np.sin(b_val * 10)  # Cyan to green variation
            saturation = 0.8 + 0.2 * b_val
            value = 0.6 + 0.4 * b_val
        elif b_val > 0.2:
            # Transition regions
            hue = 0.7 + 0.3 * (b_val - 0.2) / 0.3  # Purple to blue
            saturation = 0.7
            value = 0.4 + 0.3 * b_val
        else:
            # Deep regions
            hue = 0.65  # Deep blue
            saturation = 0.3 - 0.2 * a_val
            value = 0.1 + 0.1 * (1 - a_val)
        
        # Add subtle variations
        hue += 0.02 * np.sin(x * 0.01) * np.sin(y * 0.01)
        
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(hue % 1, saturation, value)
        image_array[y, x] = [int(r * 255), int(g * 255), int(b * 255)]

# Add subtle glow effects to high concentration areas
for y in range(1, HEIGHT-1):
    for x in range(1, WIDTH-1):
        if B[y, x] > 0.7:
            # Add glow
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dy != 0 or dx != 0:
                        dist = np.sqrt(dy**2 + dx**2)
                        glow_strength = 0.1 / dist
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < HEIGHT and 0 <= nx < WIDTH:
                            image_array[ny, nx] = np.clip(
                                image_array[ny, nx] + glow_strength * 50,
                                0, 255
                            ).astype(np.uint8)

# Create and save the image
image = Image.fromarray(image_array)
image.save('/home/norsninja/Art/artworks/2025-08-04_organic_metamorphosis/organic_metamorphosis_01.png')

print("Organic metamorphosis complete.")
print("From simple diffusion, complex life emerges.")
print("The boundary between order and chaos - where beauty lives.")