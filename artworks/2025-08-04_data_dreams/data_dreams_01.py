from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from scipy.ndimage import gaussian_filter
import math
import random
import colorsys
import struct

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create base image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(5, 5, 10))
draw = ImageDraw.Draw(img, 'RGBA')

# Data packet class
class DataPacket:
    def __init__(self, data_type, size, origin, destination):
        self.type = data_type  # 'text', 'image', 'video', 'code', 'neural'
        self.size = size
        self.origin = origin
        self.destination = destination
        self.position = list(origin)
        self.velocity = [0, 0]
        self.age = 0
        self.path_history = [list(origin)]
        self.corrupted = random.random() < 0.05  # 5% corruption rate
        self.encrypted = random.random() < 0.3  # 30% encrypted
        
        # Visual properties based on type
        self.color = self._get_type_color()
        self.pattern = self._get_type_pattern()
        
    def _get_type_color(self):
        """Color coding for different data types"""
        colors = {
            'text': (100, 200, 255),      # Blue - language
            'image': (255, 150, 100),     # Orange - visual
            'video': (255, 100, 200),     # Pink - motion
            'code': (100, 255, 150),      # Green - logic
            'neural': (200, 100, 255),    # Purple - thought
        }
        return colors.get(self.type, (200, 200, 200))
    
    def _get_type_pattern(self):
        """Visual pattern for data type"""
        patterns = {
            'text': 'lines',
            'image': 'pixels',
            'video': 'frames',
            'code': 'brackets',
            'neural': 'synapses'
        }
        return patterns.get(self.type, 'dots')
    
    def update(self):
        """Update packet position"""
        # Move toward destination
        dx = self.destination[0] - self.position[0]
        dy = self.destination[1] - self.position[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 5:
            # Normalize and apply speed based on size
            speed = 5 / (1 + self.size * 0.1)  # Smaller packets move faster
            self.velocity[0] = speed * dx / distance
            self.velocity[1] = speed * dy / distance
            
            # Add some randomness for organic movement
            self.velocity[0] += random.uniform(-0.5, 0.5)
            self.velocity[1] += random.uniform(-0.5, 0.5)
            
            # Update position
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            
            # Store path
            if len(self.path_history) < 100:
                self.path_history.append(list(self.position))
        
        self.age += 1
        
        return distance < 5  # Reached destination

# Network node class
class NetworkNode:
    def __init__(self, x, y, node_type='router'):
        self.x = x
        self.y = y
        self.type = node_type  # 'server', 'router', 'terminal', 'database', 'ai'
        self.buffer = []
        self.processing_power = random.uniform(0.5, 1.0)
        self.connections = []
        self.activity = 0
        
    def process_packet(self, packet):
        """Process incoming packet"""
        self.activity = min(1.0, self.activity + 0.1)
        
        # Different nodes handle data differently
        if self.type == 'ai':
            # AI nodes transform data
            if packet.type == 'text':
                packet.type = 'neural'
                packet.color = packet._get_type_color()
        elif self.type == 'database':
            # Databases store and replicate
            if random.random() < 0.3:
                return packet  # Replicate
        
        return None
    
    def update(self):
        """Update node state"""
        self.activity *= 0.95  # Decay activity

# Create network topology
nodes = []
node_positions = []

# Central AI core
ai_core = NetworkNode(WIDTH/2, HEIGHT/2, 'ai')
nodes.append(ai_core)
node_positions.append((ai_core.x, ai_core.y))

# Surrounding servers
for i in range(6):
    angle = i * math.pi / 3
    radius = 200
    x = WIDTH/2 + radius * math.cos(angle)
    y = HEIGHT/2 + radius * math.sin(angle)
    server = NetworkNode(x, y, 'server')
    nodes.append(server)
    node_positions.append((x, y))
    # Connect to AI core
    ai_core.connections.append(server)
    server.connections.append(ai_core)

# Edge routers
for i in range(12):
    angle = i * math.pi / 6
    radius = 350
    x = WIDTH/2 + radius * math.cos(angle)
    y = HEIGHT/2 + radius * math.sin(angle)
    router = NetworkNode(x, y, 'router')
    nodes.append(router)
    node_positions.append((x, y))
    
    # Connect to nearest servers
    for server in nodes[1:7]:
        dist = math.sqrt((x - server.x)**2 + (y - server.y)**2)
        if dist < 200:
            router.connections.append(server)
            server.connections.append(router)

# Terminal nodes (user endpoints)
for _ in range(20):
    x = random.uniform(50, WIDTH - 50)
    y = random.uniform(50, HEIGHT - 50)
    terminal = NetworkNode(x, y, 'terminal')
    nodes.append(terminal)
    node_positions.append((x, y))
    
    # Connect to nearest router
    min_dist = float('inf')
    nearest = None
    for router in nodes[7:19]:  # Just the routers
        dist = math.sqrt((x - router.x)**2 + (y - router.y)**2)
        if dist < min_dist:
            min_dist = dist
            nearest = router
    
    if nearest and min_dist < 300:
        terminal.connections.append(nearest)
        nearest.connections.append(terminal)

# Draw network infrastructure
# Connection lines
for node in nodes:
    for connected in node.connections:
        # Avoid duplicate lines
        if node.x < connected.x or (node.x == connected.x and node.y < connected.y):
            # Data highway glow
            for width in [10, 5, 2]:
                alpha = 30 + (10 - width) * 10
                draw.line([(node.x, node.y), (connected.x, connected.y)],
                         fill=(50, 50, 100, alpha), width=width)

# Create data packets
packets = []
data_types = ['text', 'image', 'video', 'code', 'neural']

# Initial burst of data
for _ in range(50):
    # Random origin and destination
    origin_node = random.choice(nodes)
    dest_node = random.choice(nodes)
    
    if origin_node != dest_node:
        data_type = random.choice(data_types)
        size = random.uniform(0.1, 1.0)
        
        packet = DataPacket(data_type, size, 
                          (origin_node.x, origin_node.y),
                          (dest_node.x, dest_node.y))
        packets.append(packet)

# Simulate data flow
for _ in range(100):
    # Update packets
    for packet in packets[:]:
        if packet.update():
            # Reached destination
            packets.remove(packet)
            
            # Sometimes spawn new packets
            if random.random() < 0.3:
                origin_node = random.choice(nodes)
                dest_node = random.choice(nodes)
                if origin_node != dest_node:
                    new_packet = DataPacket(
                        random.choice(data_types),
                        random.uniform(0.1, 1.0),
                        (origin_node.x, origin_node.y),
                        (dest_node.x, dest_node.y)
                    )
                    packets.append(new_packet)
    
    # Update nodes
    for node in nodes:
        node.update()

# Draw data streams
for packet in packets:
    # Draw path trail
    if len(packet.path_history) > 1:
        for i in range(len(packet.path_history) - 1):
            alpha = int(50 * i / len(packet.path_history))
            
            # Encrypted data has different appearance
            if packet.encrypted:
                # Dashed line for encrypted
                if i % 4 < 2:
                    draw.line([packet.path_history[i], packet.path_history[i+1]],
                             fill=packet.color + (alpha,), width=1)
            else:
                draw.line([packet.path_history[i], packet.path_history[i+1]],
                         fill=packet.color + (alpha,), width=2)
    
    # Draw packet
    x, y = packet.position
    size = 5 + packet.size * 10
    
    # Corrupted packets flicker
    if packet.corrupted:
        size *= random.uniform(0.8, 1.2)
        # Glitch colors
        r, g, b = packet.color
        r = min(255, r + random.randint(-50, 50))
        g = min(255, g + random.randint(-50, 50))
        b = min(255, b + random.randint(-50, 50))
        color = (r, g, b)
    else:
        color = packet.color
    
    # Draw based on pattern
    if packet.pattern == 'lines':
        # Text data - horizontal lines
        for i in range(3):
            y_offset = (i - 1) * 4
            draw.line([(x - size/2, y + y_offset), (x + size/2, y + y_offset)],
                     fill=color + (200,), width=1)
    elif packet.pattern == 'pixels':
        # Image data - pixel grid
        for i in range(-1, 2):
            for j in range(-1, 2):
                draw.rectangle([x + i*3 - 1, y + j*3 - 1, x + i*3 + 1, y + j*3 + 1],
                              fill=color + (150,))
    elif packet.pattern == 'frames':
        # Video data - stacked rectangles
        for i in range(3):
            offset = i * 3
            x1 = x - size/2 + offset
            y1 = y - size/2 + offset
            x2 = x + size/2 - offset
            y2 = y + size/2 - offset
            if x1 < x2 and y1 < y2:  # Ensure valid rectangle
                draw.rectangle([x1, y1, x2, y2],
                              outline=color + (180,), width=1)
    elif packet.pattern == 'brackets':
        # Code data - bracket symbols
        draw.text((x - 5, y - 5), "{}", fill=color + (200,))
    else:  # neural/synapses
        # Neural data - branching pattern
        for angle in [0, 120, 240]:
            end_x = x + size * math.cos(math.radians(angle))
            end_y = y + size * math.sin(math.radians(angle))
            draw.line([(x, y), (end_x, end_y)], fill=color + (180,), width=2)

# Draw nodes
for node in nodes:
    # Node appearance based on type and activity
    if node.type == 'ai':
        # AI core - pulsing circles
        for r in range(40, 10, -5):
            pulse = 0.5 + 0.5 * math.sin(r * 0.2)
            alpha = int(100 * pulse * (1 - r / 40))
            draw.ellipse([node.x - r, node.y - r, node.x + r, node.y + r],
                        fill=(200, 100, 255, alpha))
        # Core
        draw.ellipse([node.x - 10, node.y - 10, node.x + 10, node.y + 10],
                    fill=(255, 200, 255))
    elif node.type == 'server':
        # Server - stacked rectangles
        for i in range(3):
            y_offset = (i - 1) * 8
            color = (100, 150, 200) if node.activity < 0.5 else (200, 150, 100)
            draw.rectangle([node.x - 15, node.y + y_offset - 3,
                           node.x + 15, node.y + y_offset + 3],
                          fill=color)
    elif node.type == 'router':
        # Router - diamond
        points = [
            (node.x, node.y - 15),
            (node.x + 15, node.y),
            (node.x, node.y + 15),
            (node.x - 15, node.y)
        ]
        color = (150, 200, 150) if node.activity < 0.5 else (200, 200, 100)
        draw.polygon(points, fill=color)
    else:  # terminal
        # Terminal - simple circle
        color = (150, 150, 200) if node.activity < 0.5 else (200, 200, 255)
        draw.ellipse([node.x - 8, node.y - 8, node.x + 8, node.y + 8],
                    fill=color)

# Add digital rain effect
for _ in range(200):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    # Binary digits
    digit = random.choice(['0', '1'])
    alpha = random.randint(20, 80)
    draw.text((x, y), digit, fill=(100, 255, 100, alpha))

# Final atmospheric effects
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

# Add scan lines for digital aesthetic
for y in range(0, HEIGHT, 4):
    draw.line([(0, y), (WIDTH, y)], fill=(255, 255, 255, 5))

img.save('data_dreams_01.png')
print("Data Dreams visualized: data_dreams_01.png")