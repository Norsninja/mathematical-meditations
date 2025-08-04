from PIL import Image, ImageDraw
import numpy as np
import random

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Initialize with random state in the center
def initialize_grid(size):
    grid = np.zeros((size, size), dtype=int)
    # Seed the center with random cells
    center = size // 2
    spread = size // 8
    for _ in range(spread * spread // 4):
        x = center + random.randint(-spread, spread)
        y = center + random.randint(-spread, spread)
        if 0 <= x < size and 0 <= y < size:
            grid[x, y] = 1
    return grid

# Custom rule: cells birth and die based on neighbor patterns
def evolve(grid):
    new_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    
    for i in range(rows):
        for j in range(cols):
            # Count neighbors
            neighbors = 0
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbors += grid[ni, nj]
            
            # Rules for life and death
            if grid[i, j] == 1:
                # Living cell survives with 2 or 3 neighbors
                if neighbors in [2, 3]:
                    new_grid[i, j] = 1
            else:
                # Dead cell births with exactly 3 neighbors
                if neighbors == 3:
                    new_grid[i, j] = 1
    
    return new_grid

# Create the image with gradient colors
def create_image(history):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(10, 10, 20))
    draw = ImageDraw.Draw(img)
    
    cell_size = WIDTH // len(history[0])
    
    # Layer the history with fading intensity
    for t, grid in enumerate(history):
        alpha = (t + 1) / len(history)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] == 1:
                    # Color shifts from deep blue to bright cyan over time
                    r = int(20 + alpha * 60)
                    g = int(50 + alpha * 150)
                    b = int(180 + alpha * 75)
                    
                    x = j * cell_size
                    y = i * cell_size
                    
                    # Add slight variation in cell rendering
                    offset = int(alpha * 2)
                    draw.rectangle(
                        [x + offset, y + offset, 
                         x + cell_size - offset, y + cell_size - offset],
                        fill=(r, g, b)
                    )
    
    return img

# Main generation
grid_size = 108  # Divides evenly into 1080
grid = initialize_grid(grid_size)

# Evolve and record history
history = []
for generation in range(50):
    history.append(grid.copy())
    grid = evolve(grid)
    
    # Add some chaos - occasional random births
    if generation % 10 == 0:
        for _ in range(5):
            x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
            grid[x, y] = 1

# Create and save the image
img = create_image(history[-30:])  # Use last 30 generations for depth
img.save('emergence_01.png')
print("First piece 'Emergence' created: emergence_01.png")