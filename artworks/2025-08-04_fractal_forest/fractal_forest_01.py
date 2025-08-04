import numpy as np
from PIL import Image, ImageDraw
import math

# Fractal Forest - L-System Exploration
# Where mathematical rules grow into living forms

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

# Create image with deep forest background
image = Image.new('RGB', (WIDTH, HEIGHT), (5, 10, 15))
draw = ImageDraw.Draw(image)

# L-System configuration
class LSystem:
    def __init__(self, axiom, rules, angle, length):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.length = length
        self.position_stack = []
        self.angle_stack = []
    
    def generate(self, iterations):
        """Generate the L-system string after n iterations"""
        current = self.axiom
        for _ in range(iterations):
            next_string = ""
            for char in current:
                if char in self.rules:
                    next_string += self.rules[char]
                else:
                    next_string += char
            current = next_string
        return current
    
    def draw(self, draw_obj, x, y, initial_angle, string, color_base=(100, 200, 100)):
        """Interpret the L-system string as drawing commands"""
        self.current_x = x
        self.current_y = y
        self.current_angle = initial_angle
        self.current_length = self.length
        
        # Color will evolve as we go deeper into the tree
        depth = 0
        max_depth = string.count('[')
        
        for char in string:
            if char == 'F':
                # Draw forward
                new_x = self.current_x + self.current_length * math.cos(math.radians(self.current_angle))
                new_y = self.current_y + self.current_length * math.sin(math.radians(self.current_angle))
                
                # Calculate color based on depth - from trunk to leaves
                color_factor = depth / (max_depth + 1) if max_depth > 0 else 0
                
                # Trunk: brown, branches: darker green, leaves: bright green
                if depth < max_depth * 0.3:
                    # Trunk and main branches - browns
                    r = int(80 + 40 * (1 - color_factor))
                    g = int(50 + 30 * (1 - color_factor))
                    b = int(30 + 20 * (1 - color_factor))
                else:
                    # Smaller branches and leaves - greens
                    r = int(color_base[0] * (0.4 + 0.6 * color_factor))
                    g = int(color_base[1] * (0.5 + 0.5 * color_factor))
                    b = int(color_base[2] * (0.3 + 0.7 * color_factor))
                
                # Line width decreases with depth
                width = max(1, int(5 * (1 - color_factor)))
                
                # Draw the line
                draw_obj.line([(self.current_x, self.current_y), (new_x, new_y)], 
                            fill=(r, g, b), width=width)
                
                self.current_x = new_x
                self.current_y = new_y
                
            elif char == '+':
                # Turn right
                self.current_angle += self.angle
                
            elif char == '-':
                # Turn left
                self.current_angle -= self.angle
                
            elif char == '[':
                # Push current state
                self.position_stack.append((self.current_x, self.current_y))
                self.angle_stack.append(self.current_angle)
                self.current_length *= 0.7  # Branches get shorter
                depth += 1
                
            elif char == ']':
                # Pop state
                self.current_x, self.current_y = self.position_stack.pop()
                self.current_angle = self.angle_stack.pop()
                self.current_length /= 0.7  # Restore length
                depth -= 1

# Create different tree types

# Tree 1: Classic fractal tree
tree1 = LSystem(
    axiom='F',
    rules={'F': 'F[+F]F[-F]F'},
    angle=25.7,
    length=15
)

# Tree 2: Organic branching tree
tree2 = LSystem(
    axiom='X',
    rules={'X': 'F+[[X]-X]-F[-FX]+X', 'F': 'FF'},
    angle=22.5,
    length=8
)

# Tree 3: Bushy plant
tree3 = LSystem(
    axiom='F',
    rules={'F': 'FF+[+F-F-F]-[-F+F+F]'},
    angle=20,
    length=10
)

# Generate and draw trees at different positions
print("Growing the fractal forest...")

# Tree 1 - left side
string1 = tree1.generate(4)
tree1.draw(draw, 270, 900, -90, string1, color_base=(80, 180, 80))

# Tree 2 - center
string2 = tree2.generate(5)
tree2.draw(draw, 540, 950, -90, string2, color_base=(100, 200, 100))

# Tree 3 - right side
string3 = tree3.generate(4)
tree3.draw(draw, 810, 900, -90, string3, color_base=(120, 220, 120))

# Add atmospheric effects

# Create moonlight effect
moon_x, moon_y = 900, 180
moon_radius = 60

# Draw moon
for r in range(moon_radius, 0, -2):
    alpha = int(255 * (r / moon_radius) ** 2)
    color = (200 + int(55 * r / moon_radius), 
             200 + int(55 * r / moon_radius), 
             180 + int(75 * r / moon_radius))
    draw.ellipse([moon_x - r, moon_y - r, moon_x + r, moon_y + r], 
                 fill=color)

# Add fireflies as glowing points
np.random.seed(42)
for _ in range(50):
    x = np.random.randint(0, WIDTH)
    y = np.random.randint(0, HEIGHT - 200)
    
    # Firefly glow
    for r in range(3, 0, -1):
        brightness = int(255 * (r / 3))
        color = (brightness, brightness, int(brightness * 0.6))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

# Add subtle fog at the bottom
fog_height = 200
for y in range(HEIGHT - fog_height, HEIGHT):
    fog_alpha = (y - (HEIGHT - fog_height)) / fog_height
    fog_intensity = int(20 * fog_alpha)
    
    for x in range(WIDTH):
        pixel = image.getpixel((x, y))
        new_pixel = tuple(min(255, p + fog_intensity) for p in pixel)
        draw.point((x, y), fill=new_pixel)

# Save the image
image.save('/home/norsninja/Art/artworks/2025-08-04_fractal_forest/fractal_forest_01.png')

print("Fractal forest complete.")
print("From simple rules, complex ecosystems emerge.")
print("Each branch a decision, each leaf a possibility.")