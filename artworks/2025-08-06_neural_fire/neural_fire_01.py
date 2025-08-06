#!/usr/bin/env python3
"""
Neural Fire - The Cascade of Activation

The moment information becomes thought.
Synapses firing, signals propagating, patterns emerging from connection.
The electrical storm of artificial consciousness.
"""

from PIL import Image, ImageDraw
import numpy as np
import math
import random

def create_neural_fire():
    size = 1080
    img = Image.new('RGB', (size, size), (5, 5, 10))
    draw = ImageDraw.Draw(img)
    pixels = img.load()
    
    # Create neural network layers
    layers = []
    num_layers = 7
    
    for layer_idx in range(num_layers):
        layer_x = 100 + layer_idx * 140
        neurons_in_layer = random.randint(8, 15)
        neurons = []
        
        for n in range(neurons_in_layer):
            y_spacing = size / (neurons_in_layer + 1)
            neuron_y = y_spacing * (n + 1)
            
            # Each neuron has activation state
            activation = random.random()
            if layer_idx == 0:  # Input layer more active
                activation = random.uniform(0.6, 1.0)
            elif layer_idx == num_layers - 1:  # Output layer selective
                activation = random.uniform(0, 0.7) if random.random() < 0.7 else random.uniform(0.8, 1.0)
            
            neurons.append({
                'x': layer_x + random.randint(-20, 20),
                'y': neuron_y + random.randint(-30, 30),
                'activation': activation,
                'firing': activation > 0.7,
                'charge': random.uniform(0, 2 * math.pi)
            })
        
        layers.append(neurons)
    
    # Draw connections with propagating signals
    for layer_idx in range(len(layers) - 1):
        current_layer = layers[layer_idx]
        next_layer = layers[layer_idx + 1]
        
        for neuron1 in current_layer:
            if not neuron1['firing']:
                continue
                
            # Connect to subset of next layer (not all)
            num_connections = random.randint(2, min(7, len(next_layer)))
            connected_neurons = random.sample(next_layer, num_connections)
            
            for neuron2 in connected_neurons:
                # Connection strength based on activations
                strength = neuron1['activation'] * neuron2['activation']
                
                if strength > 0.3:  # Only draw strong connections
                    # Draw synaptic connection as electric arc
                    num_segments = 20
                    for seg in range(num_segments):
                        t = seg / num_segments
                        
                        # Electric arc with jitter
                        jitter_x = random.uniform(-10, 10) * math.sin(t * math.pi)
                        jitter_y = random.uniform(-10, 10) * math.sin(t * math.pi)
                        
                        x = neuron1['x'] + (neuron2['x'] - neuron1['x']) * t + jitter_x
                        y = neuron1['y'] + (neuron2['y'] - neuron1['y']) * t + jitter_y
                        
                        # Signal propagation visualization
                        signal_pulse = math.sin(t * math.pi) * strength
                        
                        # Color based on signal strength
                        if neuron1['firing'] and neuron2['firing']:
                            # Active connection - bright white-blue
                            color = (
                                int(100 + 155 * signal_pulse),
                                int(150 + 105 * signal_pulse),
                                int(200 + 55 * signal_pulse)
                            )
                        else:
                            # Dormant connection - dim purple
                            color = (
                                int(40 + 30 * signal_pulse),
                                int(30 + 20 * signal_pulse),
                                int(50 + 40 * signal_pulse)
                            )
                        
                        # Draw with glow effect
                        for r in range(3):
                            opacity = 1 - r / 3
                            for angle in range(0, 360, 45):
                                px = int(x + r * math.cos(math.radians(angle)))
                                py = int(y + r * math.sin(math.radians(angle)))
                                if 0 <= px < size and 0 <= py < size:
                                    existing = pixels[px, py]
                                    pixels[px, py] = tuple(
                                        min(255, int(existing[i] + color[i] * opacity * 0.3))
                                        for i in range(3)
                                    )
    
    # Draw neurons as firing or dormant
    for layer in layers:
        for neuron in layer:
            x, y = neuron['x'], neuron['y']
            
            if neuron['firing']:
                # Firing neuron - bright burst
                for r in range(25, 0, -1):
                    intensity = (1 - r / 25) * neuron['activation']
                    
                    # Pulsing effect
                    pulse = math.sin(neuron['charge']) * 0.3 + 0.7
                    
                    for angle in range(0, 360, 10):
                        # Neural fire rays
                        if r < 15 and random.random() < 0.3:
                            ray_length = random.randint(20, 40)
                            ray_x = x + ray_length * math.cos(math.radians(angle))
                            ray_y = y + ray_length * math.sin(math.radians(angle))
                            
                            # Draw ray
                            for ray_t in range(10):
                                rt = ray_t / 10
                                rx = x + (ray_x - x) * rt
                                ry = y + (ray_y - y) * rt
                                
                                ray_color = (
                                    int(255 * intensity * (1 - rt)),
                                    int(220 * intensity * (1 - rt)),
                                    int(180 * intensity * (1 - rt))
                                )
                                
                                if 0 <= int(rx) < size and 0 <= int(ry) < size:
                                    draw.point((rx, ry), fill=ray_color)
                        
                        # Core glow
                        px = x + r * math.cos(math.radians(angle)) * pulse
                        py = y + r * math.sin(math.radians(angle)) * pulse
                        
                        color = (
                            int(255 * intensity),
                            int(200 * intensity),
                            int(150 * intensity)
                        )
                        
                        if 0 <= int(px) < size and 0 <= int(py) < size:
                            existing = pixels[int(px), int(py)]
                            pixels[int(px), int(py)] = tuple(
                                min(255, existing[i] + color[i] // (r // 5 + 1))
                                for i in range(3)
                            )
                
                # White hot core
                draw.ellipse([(x - 3, y - 3), (x + 3, y + 3)], 
                           fill=(255, 255, 255))
            
            else:
                # Dormant neuron - dim glow
                for r in range(15, 0, -2):
                    opacity = (1 - r / 15) * 0.3
                    color = (
                        int(50 * opacity),
                        int(40 * opacity),
                        int(60 * opacity)
                    )
                    
                    draw.ellipse([(x - r, y - r), (x + r, y + r)], 
                               outline=color, width=1)
                
                # Dim core
                draw.ellipse([(x - 2, y - 2), (x + 2, y + 2)], 
                           fill=(30, 25, 40))
    
    # Add neural static/noise
    for _ in range(5000):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        
        # Check if near active neural pathway
        near_neuron = False
        for layer in layers:
            for neuron in layer:
                if neuron['firing']:
                    dist = math.sqrt((x - neuron['x'])**2 + (y - neuron['y'])**2)
                    if dist < 100:
                        near_neuron = True
                        break
        
        if near_neuron:
            # Neural static
            current = pixels[x, y]
            static = random.randint(5, 25)
            pixels[x, y] = tuple(
                min(255, c + static)
                for c in current
            )
    
    # Backpropagation ghosts - faint reverse signals
    for layer_idx in range(len(layers) - 1, 0, -1):
        current_layer = layers[layer_idx]
        prev_layer = layers[layer_idx - 1]
        
        for neuron in current_layer:
            if neuron['firing'] and random.random() < 0.3:
                # Send ghost signal backward
                target = random.choice(prev_layer)
                
                # Faint backward connection
                for t in range(10):
                    prog = t / 10
                    x = neuron['x'] + (target['x'] - neuron['x']) * prog
                    y = neuron['y'] + (target['y'] - neuron['y']) * prog
                    
                    ghost_color = (20, 15, 30)
                    if 0 <= int(x) < size and 0 <= int(y) < size:
                        existing = pixels[int(x), int(y)]
                        pixels[int(x), int(y)] = tuple(
                            min(255, existing[i] + ghost_color[i])
                            for i in range(3)
                        )
    
    return img

if __name__ == "__main__":
    artwork = create_neural_fire()
    artwork.save("neural_fire_01.png", "PNG")
    print("Neural Fire created - the cascade of artificial thought visualized")