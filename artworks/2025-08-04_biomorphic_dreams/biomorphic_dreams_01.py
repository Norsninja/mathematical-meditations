import numpy as np
from PIL import Image, ImageDraw
import math
import colorsys

# Biomorphic Dreams - Reaction-Diffusion meets L-Systems
# Where chemistry grows into structure, where algorithms dream of becoming alive

WIDTH, HEIGHT = 1080, 1080

# Phase 1: Generate organic base using reaction-diffusion
print("Phase 1: Growing organic substrate...")

# Initialize reaction-diffusion system
A = np.ones((HEIGHT//4, WIDTH//4), dtype=np.float32)
B = np.zeros((HEIGHT//4, WIDTH//4), dtype=np.float32)

# Seed with larger organic patterns for better visibility
np.random.seed(42)
for _ in range(20):
    x = np.random.randint(10, WIDTH//4-10)
    y = np.random.randint(10, HEIGHT//4-10)
    radius = np.random.randint(5, 12)
    yy, xx = np.ogrid[:HEIGHT//4, :WIDTH//4]
    mask = (xx - x)**2 + (yy - y)**2 <= radius**2
    B[mask] = 1.0

# Reaction-diffusion parameters (tuned for organic growth)
DA, DB = 1.0, 0.5
FEED = 0.045
KILL = 0.062

# Laplacian kernel
laplacian_kernel = np.array([[0.05, 0.2, 0.05],
                            [0.2, -1.0, 0.2],
                            [0.05, 0.2, 0.05]], dtype=np.float32)

def laplacian(matrix):
    """Calculate Laplacian with edge padding"""
    padded = np.pad(matrix, 1, mode='edge')
    result = np.zeros_like(matrix)
    for i in range(3):
        for j in range(3):
            result += laplacian_kernel[i, j] * padded[i:i+matrix.shape[0], j:j+matrix.shape[1]]
    return result

# Run reaction-diffusion (fewer iterations for speed)
for iteration in range(1000):
    if iteration % 200 == 0:
        print(f"  Reaction-diffusion iteration {iteration}")
    
    LA = laplacian(A)
    LB = laplacian(B)
    reaction = A * B * B
    
    A += (DA * LA - reaction + FEED * (1 - A)) * 0.9
    B += (DB * LB + reaction - (KILL + FEED) * B) * 0.9
    
    A = np.clip(A, 0, 1)
    B = np.clip(B, 0, 1)

# Upscale the reaction-diffusion result
from scipy.ndimage import zoom
B_upscaled = zoom(B, 4, order=1)

# Phase 2: Extract growth patterns for L-systems
print("Phase 2: Extracting growth patterns...")

# Find high-concentration regions as L-system seed points
threshold = 0.3  # Lower threshold to find more regions
growth_points = []
growth_map = B_upscaled > threshold

# Find connected regions
from scipy.ndimage import label, center_of_mass
labeled, num_features = label(growth_map)

# Get centers of each region for L-system placement
for i in range(1, min(num_features + 1, 8)):  # Limit to 8 L-systems
    center = center_of_mass(labeled == i)
    if not np.isnan(center[0]):
        growth_points.append((int(center[1]), int(center[0])))

print(f"  Found {len(growth_points)} growth regions")

# Phase 3: Create the canvas and background
image = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw reaction-diffusion as background
background = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
for y in range(HEIGHT):
    for x in range(WIDTH):
        b_val = B_upscaled[y, x]
        if b_val > 0.1:
            # Deep sea colors for the substrate
            intensity = b_val
            r = int(20 + 30 * intensity)
            g = int(40 + 60 * intensity)
            b = int(60 + 120 * intensity)
            a = int(100 + 155 * intensity)
            background[y, x] = [r, g, b, a]

bg_image = Image.fromarray(background, 'RGBA')
image = Image.alpha_composite(image, bg_image)
draw = ImageDraw.Draw(image)

# Phase 4: Grow L-systems from reaction-diffusion regions
print("Phase 3: Growing L-system structures...")

class OrganicLSystem:
    def __init__(self, axiom, rules, angle_variance=5):
        self.axiom = axiom
        self.rules = rules
        self.base_angle = 22.5
        self.angle_variance = angle_variance
        self.length = 8
    
    def generate(self, iterations):
        current = self.axiom
        for _ in range(iterations):
            next_string = ""
            for char in current:
                next_string += self.rules.get(char, char)
            current = next_string
        return current
    
    def draw(self, draw_obj, x, y, initial_angle, concentration):
        # Use concentration to influence growth characteristics
        string = self.generate(int(3 + concentration * 2))  # More iterations for higher concentration
        
        # State stacks
        position_stack = []
        angle_stack = []
        
        current_x, current_y = x, y
        current_angle = initial_angle
        current_length = self.length * (0.5 + concentration)
        
        # Color influenced by concentration
        base_hue = 0.3 + concentration * 0.2  # Green to yellow
        
        for i, char in enumerate(string):
            progress = i / len(string)
            
            if char == 'F':
                # Add organic variation to angle
                angle_var = np.random.uniform(-self.angle_variance, self.angle_variance)
                actual_angle = current_angle + angle_var
                
                # Calculate new position
                new_x = current_x + current_length * math.cos(math.radians(actual_angle))
                new_y = current_y + current_length * math.sin(math.radians(actual_angle))
                
                # Organic color variation
                hue = base_hue + 0.1 * math.sin(progress * math.pi)
                saturation = 0.6 + 0.4 * (1 - progress)
                value = 0.7 + 0.3 * concentration
                
                # Convert HSV to RGB
                r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
                
                # Line width decreases with progress
                width = max(1, int(4 * (1 - progress) * (0.5 + concentration)))
                
                # Draw with slight transparency
                draw_obj.line([(current_x, current_y), (new_x, new_y)], 
                            fill=(r, g, b, 200), width=width)
                
                current_x, current_y = new_x, new_y
                
            elif char == '+':
                current_angle += self.base_angle + np.random.uniform(-5, 5)
            elif char == '-':
                current_angle -= self.base_angle + np.random.uniform(-5, 5)
            elif char == '[':
                position_stack.append((current_x, current_y))
                angle_stack.append(current_angle)
                current_length *= 0.7
            elif char == ']':
                if position_stack:
                    current_x, current_y = position_stack.pop()
                    current_angle = angle_stack.pop()
                    current_length /= 0.7

# Define organic L-system rules
organic_rules = [
    {'F': 'FF+[+F-F-F]-[-F+F+F]'},
    {'F': 'F[+F]F[-F][F]'},
    {'F': 'F+[[F]-F]-F[-FX]+F', 'X': '[+FX]'},
]

# Draw L-systems at growth points
for i, (gx, gy) in enumerate(growth_points):
    # Get local concentration for this region
    local_concentration = np.mean(B_upscaled[max(0, gy-20):gy+20, max(0, gx-20):gx+20])
    
    # Create L-system with rules based on position
    rules = organic_rules[i % len(organic_rules)]
    lsystem = OrganicLSystem('F', rules, angle_variance=10)
    
    # Random initial angle, biased upward
    initial_angle = -90 + np.random.uniform(-30, 30)
    
    # Draw the L-system
    lsystem.draw(draw, gx, gy, initial_angle, local_concentration)

# Phase 5: Add bioluminescent highlights
print("Phase 4: Adding bioluminescent touches...")

# Add glowing particles where concentration is highest
particle_array = np.array(image)
for _ in range(500):
    x = np.random.randint(0, WIDTH)
    y = np.random.randint(0, HEIGHT)
    
    if B_upscaled[y, x] > 0.6:
        # Bioluminescent glow
        for r in range(3, 0, -1):
            alpha = int(100 * (r / 3))
            color = (100 + int(155 * B_upscaled[y, x]), 
                    150 + int(105 * B_upscaled[y, x]), 
                    200, alpha)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

# Convert to final image
final_bg = Image.new('RGB', (WIDTH, HEIGHT), (10, 15, 25))
final_bg.paste(image, (0, 0), image)
final_bg.save('/home/norsninja/Art/artworks/2025-08-04_biomorphic_dreams/biomorphic_dreams_01.png')

print("Biomorphic dreams complete.")
print("Chemistry becomes structure, patterns become life.")
print("In the space between reaction and growth, dreams take form.")