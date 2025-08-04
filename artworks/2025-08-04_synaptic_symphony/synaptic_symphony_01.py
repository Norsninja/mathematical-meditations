from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.ndimage import gaussian_filter
import math
import random
import colorsys

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Neural network parameters
class Neuron:
    def __init__(self, x, y, layer_idx):
        self.x = x
        self.y = y
        self.layer = layer_idx
        self.activation = random.uniform(0, 1)
        self.connections = []
        self.bias = random.uniform(-0.5, 0.5)
        self.memory = []  # Store activation history
        self.resonance_freq = random.uniform(0.1, 0.5)
        self.phase = random.uniform(0, 2 * math.pi)
        
    def update_activation(self, time_step):
        # Activation oscillates with unique frequency
        base_activation = 0
        for conn in self.connections:
            base_activation += conn['neuron'].activation * conn['weight']
        
        # Add temporal dynamics
        temporal_component = math.sin(time_step * self.resonance_freq + self.phase)
        self.activation = np.tanh(base_activation + self.bias + temporal_component * 0.3)
        
        # Store in memory (keep last 10 states)
        self.memory.append(self.activation)
        if len(self.memory) > 10:
            self.memory.pop(0)

# Create neural network architecture
def create_network():
    neurons = []
    layers = [8, 12, 16, 12, 8]  # Network architecture
    
    for layer_idx, num_neurons in enumerate(layers):
        layer_neurons = []
        layer_x = WIDTH * (layer_idx + 1) / (len(layers) + 1)
        
        for i in range(num_neurons):
            y = HEIGHT * (i + 1) / (num_neurons + 1)
            # Add some organic positioning
            x = layer_x + random.uniform(-30, 30)
            y = y + random.uniform(-20, 20)
            
            neuron = Neuron(x, y, layer_idx)
            layer_neurons.append(neuron)
        
        neurons.append(layer_neurons)
    
    # Create connections
    for l in range(len(layers) - 1):
        for n1 in neurons[l]:
            # Connect to subset of next layer (not fully connected for visual clarity)
            num_connections = random.randint(2, min(6, len(neurons[l + 1])))
            connected_to = random.sample(neurons[l + 1], num_connections)
            
            for n2 in connected_to:
                weight = random.gauss(0, 0.5)
                n1.connections.append({'neuron': n2, 'weight': weight})
    
    return neurons

# Create the main image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(10, 10, 20))

# Create glow layer for neural activity
glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)

# Background - subtle neural field
# Use Voronoi diagram for organic cellular structure
points = []
for _ in range(100):
    points.append([random.uniform(0, WIDTH), random.uniform(0, HEIGHT)])

vor = Voronoi(np.array(points))

# Draw Voronoi cells as background texture
draw = ImageDraw.Draw(img)
for region_idx in range(len(vor.regions)):
    region = vor.regions[region_idx]
    if not region or -1 in region:
        continue
    
    try:
        polygon = [tuple(vor.vertices[i]) for i in region]
        # Check if polygon is valid
        if len(polygon) >= 3 and all(0 <= p[0] <= WIDTH and 0 <= p[1] <= HEIGHT for p in polygon):
            # Subtle coloring based on position
            center_x = sum(p[0] for p in polygon) / len(polygon)
            center_y = sum(p[1] for p in polygon) / len(polygon)
            
            distance_from_center = math.sqrt((center_x - WIDTH/2)**2 + (center_y - HEIGHT/2)**2)
            intensity = 20 + int(10 * (1 - distance_from_center / (WIDTH/2)))
            
            draw.polygon(polygon, fill=(intensity, intensity, intensity + 5), outline=(30, 30, 40))
    except:
        pass  # Skip invalid polygons

# Create neural network
network = create_network()

# Simulate network activity
time_steps = 50
for t in range(time_steps):
    # Update all neurons
    for layer in network:
        for neuron in layer:
            neuron.update_activation(t)

# Draw the network
draw = ImageDraw.Draw(img, 'RGBA')

# Draw connections as flowing energy
for layer in network:
    for neuron in layer:
        for conn in neuron.connections:
            n2 = conn['neuron']
            weight = conn['weight']
            
            # Connection strength affects visual properties
            alpha = int(abs(weight) * 100)
            width = 1 + int(abs(weight) * 3)
            
            # Color based on weight sign and activation flow
            activation_flow = neuron.activation * weight
            if activation_flow > 0:
                # Positive flow - warm colors
                hue = 0.1  # Orange
            else:
                # Negative flow - cool colors
                hue = 0.6  # Blue
            
            saturation = min(1.0, abs(activation_flow) * 2)
            value = 0.5 + abs(activation_flow) * 0.5
            
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
            
            # Draw connection with bezier curve for organic feel
            control_x = (neuron.x + n2.x) / 2 + random.uniform(-50, 50)
            control_y = (neuron.y + n2.y) / 2 + random.uniform(-50, 50)
            
            # Draw multiple segments for the curve
            segments = 20
            for i in range(segments):
                t1 = i / segments
                t2 = (i + 1) / segments
                
                # Bezier curve formula
                x1 = (1-t1)**2 * neuron.x + 2*(1-t1)*t1 * control_x + t1**2 * n2.x
                y1 = (1-t1)**2 * neuron.y + 2*(1-t1)*t1 * control_y + t1**2 * n2.y
                x2 = (1-t2)**2 * neuron.x + 2*(1-t2)*t2 * control_x + t2**2 * n2.x
                y2 = (1-t2)**2 * neuron.y + 2*(1-t2)*t2 * control_y + t2**2 * n2.y
                
                # Pulsing effect along the connection
                pulse = math.sin(t1 * math.pi * 2 + neuron.phase) * 0.5 + 0.5
                segment_alpha = int(alpha * pulse)
                
                draw.line([(x1, y1), (x2, y2)], 
                         fill=(r, g, b, segment_alpha), 
                         width=width)

# Draw neurons
for layer_idx, layer in enumerate(network):
    for neuron in layer:
        # Neuron size based on activation
        base_size = 15
        size = base_size + neuron.activation * 10
        
        # Layer depth affects color
        layer_hue = layer_idx / len(network)
        
        # Activation affects brightness
        brightness = 0.3 + abs(neuron.activation) * 0.7
        
        # Memory trail - show activation history
        for i, past_activation in enumerate(neuron.memory):
            trail_alpha = int(50 * i / len(neuron.memory))
            trail_size = size * (0.5 + 0.5 * i / len(neuron.memory))
            offset = (len(neuron.memory) - i) * 2
            
            glow_draw.ellipse([neuron.x - trail_size - offset, 
                              neuron.y - trail_size - offset,
                              neuron.x + trail_size - offset, 
                              neuron.y + trail_size - offset],
                             fill=(100, 150, 200, trail_alpha))
        
        # Neuron glow
        for glow_level in range(3):
            glow_size = size + (glow_level + 1) * 5
            glow_alpha = int(150 * neuron.activation / (glow_level + 1))
            
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(layer_hue, 0.7, brightness)]
            
            glow_draw.ellipse([neuron.x - glow_size, neuron.y - glow_size,
                              neuron.x + glow_size, neuron.y + glow_size],
                             fill=(r, g, b, glow_alpha))
        
        # Neuron core
        if neuron.activation > 0:
            core_color = (255, 200, 150, 200)  # Warm for positive
        else:
            core_color = (150, 200, 255, 200)  # Cool for negative
            
        draw.ellipse([neuron.x - size, neuron.y - size,
                     neuron.x + size, neuron.y + size],
                    fill=core_color)
        
        # Inner detail - nucleus
        nucleus_size = size * 0.3
        draw.ellipse([neuron.x - nucleus_size, neuron.y - nucleus_size,
                     neuron.x + nucleus_size, neuron.y + nucleus_size],
                    fill=(20, 20, 30, 255))

# Add synaptic sparks at highly active connections
for _ in range(100):
    layer = random.choice(network[:-1])  # Not the last layer
    neuron = random.choice(layer)
    if abs(neuron.activation) > 0.5 and neuron.connections:
        conn = random.choice(neuron.connections)
        
        # Spark position along the connection
        t = random.uniform(0.3, 0.7)
        spark_x = neuron.x + t * (conn['neuron'].x - neuron.x)
        spark_y = neuron.y + t * (conn['neuron'].y - neuron.y)
        
        # Spark properties
        spark_size = random.uniform(1, 4)
        intensity = abs(neuron.activation * conn['weight'])
        
        for i in range(3):
            s = spark_size + i
            alpha = int(200 * intensity / (i + 1))
            glow_draw.ellipse([spark_x - s, spark_y - s, spark_x + s, spark_y + s],
                             fill=(255, 255, 200, alpha))

# Composite the glow layer
img = img.convert('RGBA')
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=2))
img = Image.alpha_composite(img, glow_layer)

# Final adjustments
img = img.convert('RGB')

# Add subtle noise for organic feel
pixels = img.load()
for x in range(0, WIDTH, 2):
    for y in range(0, HEIGHT, 2):
        if random.random() < 0.1:
            noise = random.randint(-10, 10)
            r, g, b = pixels[x, y]
            pixels[x, y] = (max(0, r + noise), max(0, g + noise), max(0, b + noise))

img.save('synaptic_symphony_01.png')
print("Synaptic Symphony created: synaptic_symphony_01.png")