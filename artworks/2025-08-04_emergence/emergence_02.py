from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import random
import math

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Initialize with multiple seed points
def initialize_grid(size):
    grid = np.zeros((size, size), dtype=int)
    # Create multiple growth centers
    num_seeds = 5
    for _ in range(num_seeds):
        cx = random.randint(size//4, 3*size//4)
        cy = random.randint(size//4, 3*size//4)
        # Dense seed cluster
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx*dx + dy*dy <= 9:  # Circular seed
                    x, y = cx + dx, cy + dy
                    if 0 <= x < size and 0 <= y < size:
                        grid[x, y] = 1
    return grid

# Modified rules for more interesting patterns
def evolve(grid, generation):
    new_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    
    for i in range(rows):
        for j in range(cols):
            # Count neighbors in different ranges
            neighbors_close = 0
            neighbors_far = 0
            
            for di in range(-2, 3):
                for dj in range(-2, 3):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if abs(di) <= 1 and abs(dj) <= 1:
                            neighbors_close += grid[ni, nj]
                        else:
                            neighbors_far += grid[ni, nj]
            
            # Dynamic rules that change over time
            if grid[i, j] == 1:
                # Living cells have different survival conditions
                if generation < 20:
                    # Early: standard Conway rules
                    if neighbors_close in [2, 3]:
                        new_grid[i, j] = 1
                else:
                    # Later: more forgiving, allows patterns to persist
                    if neighbors_close in [2, 3, 4] or neighbors_far >= 3:
                        new_grid[i, j] = 1
            else:
                # Birth conditions
                if neighbors_close == 3 or (neighbors_close == 2 and neighbors_far >= 2):
                    new_grid[i, j] = 1
    
    return new_grid

# Create image with multiple visual layers
def create_image(history):
    # Background with subtle gradient
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(5, 5, 15))
    draw = ImageDraw.Draw(img)
    
    # Add gradient background
    for y in range(HEIGHT):
        intensity = int(10 * (1 - y / HEIGHT))
        draw.line([(0, y), (WIDTH, y)], fill=(intensity, intensity, intensity + 10))
    
    cell_size = WIDTH // len(history[0])
    
    # Create glow effect layer
    glow_img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    
    # Layer the history with different visual treatments
    for t, grid in enumerate(history):
        age = t / len(history)
        
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] == 1:
                    x = j * cell_size
                    y = i * cell_size
                    
                    # Calculate local density for color variation
                    density = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < grid.shape[0] and 0 <= nj < grid.shape[1]:
                                density += grid[ni, nj]
                    
                    # Color based on age and density
                    if t == len(history) - 1:  # Current generation - bright
                        r = min(255, 100 + density * 20)
                        g = min(255, 150 + density * 15)
                        b = min(255, 200 + density * 10)
                    else:  # History - fading trails
                        fade = age * 0.7
                        r = int(30 + fade * 50 * density / 9)
                        g = int(50 + fade * 80 * density / 9)
                        b = int(100 + fade * 100 * density / 9)
                    
                    # Draw with soft edges
                    if t == len(history) - 1:
                        # Current cells - solid with slight glow
                        draw.rectangle(
                            [x + 1, y + 1, x + cell_size - 1, y + cell_size - 1],
                            fill=(r, g, b)
                        )
                        # Add to glow layer
                        glow_draw.ellipse(
                            [x - 2, y - 2, x + cell_size + 2, y + cell_size + 2],
                            fill=(r//3, g//3, b//3)
                        )
                    else:
                        # Historical cells - smaller, translucent effect
                        offset = int((1 - age) * 2)
                        draw.ellipse(
                            [x + offset, y + offset, 
                             x + cell_size - offset, y + cell_size - offset],
                            fill=(r, g, b)
                        )
    
    # Apply glow effect
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=3))
    
    # Composite glow under main image
    final = Image.new('RGB', (WIDTH, HEIGHT))
    final.paste(img, (0, 0))
    final = Image.blend(final, glow_img, 0.5)
    
    return final

# Main generation
grid_size = 120  # Slightly larger cells
grid = initialize_grid(grid_size)

# Evolve with periodic perturbations
history = []
for generation in range(80):
    history.append(grid.copy())
    grid = evolve(grid, generation)
    
    # Occasional spontaneous life to prevent stagnation
    if generation % 15 == 0 and generation > 0:
        # Find edges of existing patterns and add new cells
        for i in range(1, grid_size - 1):
            for j in range(1, grid_size - 1):
                if grid[i, j] == 0:
                    neighbors = sum(grid[i+di, j+dj] for di in [-1,0,1] for dj in [-1,0,1])
                    if neighbors == 1 and random.random() < 0.3:
                        grid[i, j] = 1

# Create image using last 40 generations for depth
img = create_image(history[-40:])
img.save('emergence_02.png')
print("Second iteration created: emergence_02.png")