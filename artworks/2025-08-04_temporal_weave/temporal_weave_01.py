import numpy as np
from PIL import Image, ImageDraw
import math

# Temporal Weave - Time as Fabric
# Past, present, and future intertwining in a single moment

WIDTH, HEIGHT = 1080, 1080

# Create base image
image = Image.new('RGBA', (WIDTH, HEIGHT), (10, 10, 20, 255))
draw = ImageDraw.Draw(image)

# Time parameters
NUM_THREADS = 12  # Temporal threads
TIME_POINTS = 100  # Points along each thread
SPIRAL_TURNS = 3  # How many times threads spiral

# Color schemes for different temporal states
time_colors = {
    'deep_past': [(20, 30, 60), (40, 50, 80)],      # Deep blues
    'recent_past': [(60, 80, 120), (80, 100, 140)], # Lighter blues
    'present': [(200, 180, 160), (240, 220, 200)],  # Warm whites
    'near_future': [(180, 120, 100), (200, 140, 120)], # Warm oranges
    'far_future': [(120, 60, 80), (140, 80, 100)]   # Deep reds
}

def get_temporal_color(time_position):
    """Get color based on temporal position (-1 to 1)"""
    if time_position < -0.6:
        colors = time_colors['deep_past']
        factor = (time_position + 1) / 0.4
    elif time_position < -0.2:
        colors = time_colors['recent_past']
        factor = (time_position + 0.6) / 0.4
    elif time_position < 0.2:
        colors = time_colors['present']
        factor = (time_position + 0.2) / 0.4
    elif time_position < 0.6:
        colors = time_colors['near_future']
        factor = (time_position - 0.2) / 0.4
    else:
        colors = time_colors['far_future']
        factor = (time_position - 0.6) / 0.4
    
    # Interpolate between color pair
    factor = max(0, min(1, factor))
    color = []
    for i in range(3):
        color.append(int(colors[0][i] + (colors[1][i] - colors[0][i]) * factor))
    
    return tuple(color)

# Create temporal threads
print("Weaving the fabric of time...")

# Store thread paths for intersection detection
thread_paths = []

for thread_idx in range(NUM_THREADS):
    thread_angle = (thread_idx / NUM_THREADS) * 2 * np.pi
    thread_phase = thread_idx * np.pi / 6  # Phase shift for variety
    
    points = []
    
    for t in range(TIME_POINTS):
        # Normalized time from -1 (past) to 1 (future)
        time_pos = (t / TIME_POINTS) * 2 - 1
        
        # Spiral radius changes with time
        radius = 300 + 150 * math.sin(time_pos * np.pi)
        
        # Angular position - threads spiral inward/outward
        angle = thread_angle + time_pos * SPIRAL_TURNS * 2 * np.pi
        
        # Add wave perturbation
        wave = 20 * math.sin(t * 0.1 + thread_phase)
        
        # Calculate position
        x = WIDTH/2 + (radius + wave) * math.cos(angle)
        y = HEIGHT/2 + (radius + wave) * math.sin(angle)
        
        # Store point with temporal information
        points.append((x, y, time_pos))
    
    thread_paths.append(points)
    
    # Draw the thread
    for i in range(len(points) - 1):
        x1, y1, t1 = points[i]
        x2, y2, t2 = points[i + 1]
        
        # Get color based on temporal position
        color = get_temporal_color(t1)
        
        # Thread width varies with time - thicker in present
        width = int(3 + 5 * (1 - abs(t1)))
        
        # Draw thread segment
        draw.line([(x1, y1), (x2, y2)], fill=color + (255,), width=width)

# Add temporal nodes where threads intersect
print("Finding temporal intersections...")

intersection_points = []

# Check for intersections between threads
for i in range(NUM_THREADS):
    for j in range(i + 1, NUM_THREADS):
        thread1 = thread_paths[i]
        thread2 = thread_paths[j]
        
        # Simple intersection check
        for p1 in range(0, len(thread1), 5):
            x1, y1, t1 = thread1[p1]
            
            for p2 in range(0, len(thread2), 5):
                x2, y2, t2 = thread2[p2]
                
                # Check if points are close
                dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                if dist < 15:
                    # Average position and time
                    ix = (x1 + x2) / 2
                    iy = (y1 + y2) / 2
                    it = (t1 + t2) / 2
                    
                    intersection_points.append((ix, iy, it))

# Draw intersection nodes
for ix, iy, it in intersection_points:
    # Node size based on temporal position
    node_size = int(5 + 10 * (1 - abs(it)))
    
    # Nodes glow brighter near present
    if abs(it) < 0.3:
        # Present nodes - bright glow
        for r in range(node_size, 0, -1):
            alpha = int(200 * (r / node_size))
            glow_color = (240, 220, 200, alpha)
            draw.ellipse([ix-r, iy-r, ix+r, iy+r], fill=glow_color)
    else:
        # Past/future nodes - subtle
        node_color = get_temporal_color(it)
        draw.ellipse([ix-node_size/2, iy-node_size/2, 
                     ix+node_size/2, iy+node_size/2], 
                    fill=node_color + (200,))

# Add time particles flowing along threads
print("Adding temporal particles...")

np.random.seed(42)
for _ in range(200):
    # Choose random thread and position
    thread_idx = np.random.randint(0, NUM_THREADS)
    time_idx = np.random.randint(0, TIME_POINTS)
    
    x, y, t = thread_paths[thread_idx][time_idx]
    
    # Particle properties based on time
    particle_color = get_temporal_color(t)
    
    # Add slight position variation
    px = x + np.random.normal(0, 5)
    py = y + np.random.normal(0, 5)
    
    # Particle size - smaller in past/future
    size = 1 + int(2 * (1 - abs(t)))
    
    # Draw particle with glow
    alpha = int(150 + 105 * (1 - abs(t)))
    draw.ellipse([px-size, py-size, px+size, py+size], 
                fill=particle_color + (alpha,))

# Add central time vortex
center_x, center_y = WIDTH/2, HEIGHT/2
for r in range(80, 0, -2):
    # Gradient from center
    factor = (80 - r) / 80
    intensity = int(100 * factor)
    
    # Slight color shift
    color = (200 + int(55 * factor), 
             180 + int(40 * factor), 
             160 + int(20 * factor), 
             intensity)
    
    draw.ellipse([center_x-r, center_y-r, center_x+r, center_y+r], 
                fill=color)

# Save the image
image.save('/home/norsninja/Art/artworks/2025-08-04_temporal_weave/temporal_weave_01.png')

print("Temporal weave complete.")
print("Time is not a line but a tapestry.")
print("Past and future meet in the eternal now.")