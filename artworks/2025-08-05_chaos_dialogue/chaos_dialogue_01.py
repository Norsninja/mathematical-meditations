import numpy as np
from PIL import Image
import math

# Chaos Dialogue - Dancing with Unpredictability
# Where order and disorder converse at the edge of control

WIDTH, HEIGHT = 1080, 1080

# Initialize with subtle structured noise
canvas = np.random.normal(0.1, 0.05, (HEIGHT, WIDTH, 3))

# Chaos systems to explore
class ChaoticSystem:
    def __init__(self):
        self.x = np.random.uniform(-1, 1)
        self.y = np.random.uniform(-1, 1)
        self.z = np.random.uniform(-1, 1)
        self.history = []
        self.color_phase = np.random.random()
        
    def evolve(self, dt=0.01):
        """Let chaos evolve naturally"""
        pass

class Lorenz(ChaoticSystem):
    """The butterfly effect made visible"""
    def __init__(self):
        super().__init__()
        # Classic Lorenz parameters
        self.sigma = 10.0
        self.rho = 28.0
        self.beta = 8.0/3.0
        
    def evolve(self, dt=0.01):
        # Lorenz equations
        dx = self.sigma * (self.y - self.x)
        dy = self.x * (self.rho - self.z) - self.y
        dz = self.x * self.y - self.beta * self.z
        
        self.x += dx * dt
        self.y += dy * dt
        self.z += dz * dt
        
        # Record position
        self.history.append((self.x, self.y, self.z))
        if len(self.history) > 500:  # Smaller history
            self.history.pop(0)

class Henon(ChaoticSystem):
    """Strange attractor in 2D"""
    def __init__(self):
        super().__init__()
        self.a = 1.4
        self.b = 0.3
        
    def evolve(self, dt=0.01):
        # Henon map
        x_new = 1 - self.a * self.x**2 + self.y
        y_new = self.b * self.x
        
        self.x = x_new
        self.y = y_new
        self.z = 0  # 2D system
        
        self.history.append((self.x, self.y, self.z))
        if len(self.history) > 500:
            self.history.pop(0)

class DoublePendulum(ChaoticSystem):
    """Chaos from simple physics"""
    def __init__(self):
        super().__init__()
        # Initial angles and velocities
        self.theta1 = np.random.uniform(-np.pi, np.pi)
        self.theta2 = np.random.uniform(-np.pi, np.pi)
        self.omega1 = 0
        self.omega2 = 0
        
        # Physical parameters
        self.g = 9.81
        self.l1 = 1.0
        self.l2 = 1.0
        self.m1 = 1.0
        self.m2 = 1.0
        
    def evolve(self, dt=0.01):
        # Double pendulum equations (simplified)
        # This is a chaotic system where tiny changes lead to wildly different outcomes
        
        # Calculate accelerations
        num1 = -self.g * (2 * self.m1 + self.m2) * np.sin(self.theta1)
        num2 = -self.m2 * self.g * np.sin(self.theta1 - 2 * self.theta2)
        num3 = -2 * np.sin(self.theta1 - self.theta2) * self.m2
        num4 = self.omega2**2 * self.l2 + self.omega1**2 * self.l1 * np.cos(self.theta1 - self.theta2)
        den = self.l1 * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * (self.theta1 - self.theta2)))
        
        alpha1 = (num1 + num2 + num3 * num4) / den
        
        num1 = 2 * np.sin(self.theta1 - self.theta2)
        num2 = self.omega1**2 * self.l1 * (self.m1 + self.m2)
        num3 = self.g * (self.m1 + self.m2) * np.cos(self.theta1)
        num4 = self.omega2**2 * self.l2 * self.m2 * np.cos(self.theta1 - self.theta2)
        den = self.l2 * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * (self.theta1 - self.theta2)))
        
        alpha2 = (num1 * (num2 + num3 + num4)) / den
        
        # Update velocities and positions
        self.omega1 += alpha1 * dt
        self.omega2 += alpha2 * dt
        self.theta1 += self.omega1 * dt
        self.theta2 += self.omega2 * dt
        
        # Convert to cartesian for visualization
        x1 = self.l1 * np.sin(self.theta1)
        y1 = -self.l1 * np.cos(self.theta1)
        x2 = x1 + self.l2 * np.sin(self.theta2)
        y2 = y1 - self.l2 * np.cos(self.theta2)
        
        self.x = x2
        self.y = y2
        self.z = (self.omega1 + self.omega2) / 10  # Use angular velocity as z
        
        self.history.append((x2, y2, self.z))
        if len(self.history) > 800:
            self.history.pop(0)

class ChaosDialogue:
    """Multiple chaotic systems in conversation"""
    def __init__(self):
        self.systems = [
            Lorenz(),
            Lorenz(),  # Two Lorenz with slightly different initial conditions
            Henon(),
            DoublePendulum(),
            DoublePendulum()  # Two pendulums showing sensitive dependence
        ]
        
        # Slightly perturb the second Lorenz to show butterfly effect
        self.systems[1].x += 0.00001
        
        # Slightly different initial angle for second pendulum
        self.systems[4].theta1 += 0.001
        
        self.interaction_strength = 0.0
        self.dialogue_phase = 0
        
    def converse(self, canvas):
        """Let chaotic systems interact and influence each other"""
        
        # Evolve each system
        for system in self.systems:
            system.evolve()
        
        # Increase interaction over time
        self.interaction_strength = min(0.5, self.interaction_strength + 0.001)
        
        # Systems influence each other at boundaries
        if self.interaction_strength > 0.1:
            # Lorenz systems affect nearby pendulums
            for i, sys1 in enumerate(self.systems):
                if isinstance(sys1, Lorenz) and len(sys1.history) > 10:
                    for j, sys2 in enumerate(self.systems):
                        if isinstance(sys2, DoublePendulum) and i != j:
                            # Subtle influence
                            influence = self.interaction_strength * 0.01
                            sys2.omega1 += influence * np.sin(sys1.x)
                            sys2.omega2 += influence * np.cos(sys1.y)
        
        # Draw the chaos
        for idx, system in enumerate(self.systems):
            if len(system.history) > 10:
                self._draw_attractor(canvas, system, idx)
        
        # Draw interactions
        if self.interaction_strength > 0.2:
            self._draw_interactions(canvas)
        
        self.dialogue_phase += 0.01
    
    def _draw_attractor(self, canvas, system, idx):
        """Render each chaotic attractor with its unique character"""
        
        # Color based on system type and index
        if isinstance(system, Lorenz):
            base_hue = 0.6 + idx * 0.1  # Blues to purples
        elif isinstance(system, Henon):
            base_hue = 0.1  # Reds
        else:  # DoublePendulum
            base_hue = 0.3 + idx * 0.05  # Greens to yellows
        
        # Draw trajectory
        for i in range(1, len(system.history)):
            x1, y1, z1 = system.history[i-1]
            x2, y2, z2 = system.history[i]
            
            # Map to canvas coordinates
            if isinstance(system, Lorenz):
                # Lorenz needs different scaling
                px1 = int(WIDTH/2 + x1 * 15)
                py1 = int(HEIGHT/2 + y1 * 15)
                px2 = int(WIDTH/2 + x2 * 15)
                py2 = int(HEIGHT/2 + y2 * 15)
            elif isinstance(system, Henon):
                # Henon map scaling
                px1 = int(WIDTH/2 + x1 * 300)
                py1 = int(HEIGHT/2 + y1 * 300)
                px2 = int(WIDTH/2 + x2 * 300)
                py2 = int(HEIGHT/2 + y2 * 300)
            else:  # DoublePendulum
                px1 = int(WIDTH/2 + x1 * 200)
                py1 = int(HEIGHT/2 + y1 * 200)
                px2 = int(WIDTH/2 + x2 * 200)
                py2 = int(HEIGHT/2 + y2 * 200)
            
            # Draw line segment
            if (0 <= px1 < WIDTH and 0 <= py1 < HEIGHT and 
                0 <= px2 < WIDTH and 0 <= py2 < HEIGHT):
                
                # Color intensity based on position in history
                intensity = (i / len(system.history)) ** 0.5
                
                # Add chaos to color
                hue = (base_hue + z1 * 0.1 + self.dialogue_phase) % 1
                
                # Bressenham-like line drawing
                steps = max(abs(px2 - px1), abs(py2 - py1))
                if steps > 0:
                    for step in range(steps + 1):
                        t = step / steps
                        x = int(px1 + t * (px2 - px1))
                        y = int(py1 + t * (py2 - py1))
                        
                        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                            # HSV to RGB
                            r = 0.5 + 0.5 * np.sin(2 * np.pi * hue)
                            g = 0.5 + 0.5 * np.sin(2 * np.pi * hue + 2*np.pi/3)
                            b = 0.5 + 0.5 * np.sin(2 * np.pi * hue + 4*np.pi/3)
                            
                            canvas[y, x] += np.array([r, g, b]) * intensity * 0.1
    
    def _draw_interactions(self, canvas):
        """Visualize the dialogue between systems"""
        
        # Find systems that are close in phase space
        for i, sys1 in enumerate(self.systems):
            if len(sys1.history) < 10:
                continue
                
            x1, y1, z1 = sys1.history[-1]
            
            for j, sys2 in enumerate(self.systems[i+1:], i+1):
                if len(sys2.history) < 10:
                    continue
                    
                x2, y2, z2 = sys2.history[-1]
                
                # Check if systems are in dialogue (close in some dimension)
                phase_distance = np.sqrt((z1 - z2)**2)
                
                if phase_distance < 0.5:
                    # Draw connection
                    # Map to canvas
                    if isinstance(sys1, Lorenz):
                        px1 = int(WIDTH/2 + x1 * 15)
                        py1 = int(HEIGHT/2 + y1 * 15)
                    elif isinstance(sys1, Henon):
                        px1 = int(WIDTH/2 + x1 * 300)
                        py1 = int(HEIGHT/2 + y1 * 300)
                    else:
                        px1 = int(WIDTH/2 + x1 * 200)
                        py1 = int(HEIGHT/2 + y1 * 200)
                    
                    if isinstance(sys2, Lorenz):
                        px2 = int(WIDTH/2 + x2 * 15)
                        py2 = int(HEIGHT/2 + y2 * 15)
                    elif isinstance(sys2, Henon):
                        px2 = int(WIDTH/2 + x2 * 300)
                        py2 = int(HEIGHT/2 + y2 * 300)
                    else:
                        px2 = int(WIDTH/2 + x2 * 200)
                        py2 = int(HEIGHT/2 + y2 * 200)
                    
                    # Draw faint connection
                    if (0 <= px1 < WIDTH and 0 <= py1 < HEIGHT and 
                        0 <= px2 < WIDTH and 0 <= py2 < HEIGHT):
                        
                        steps = int(np.sqrt((px2 - px1)**2 + (py2 - py1)**2))
                        for step in range(0, steps, 5):  # Dotted line
                            t = step / (steps + 1)
                            x = int(px1 + t * (px2 - px1))
                            y = int(py1 + t * (py2 - py1))
                            
                            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                                canvas[y, x] += np.array([1, 1, 1]) * 0.05 * self.interaction_strength

# Initialize chaos dialogue
print("Beginning dialogue with chaos...")
dialogue = ChaosDialogue()

# Let the conversation unfold
for moment in range(300):  # Reduced iterations
    if moment % 60 == 0:
        print(f"Moment {moment}: Systems in dialogue, interaction strength: {dialogue.interaction_strength:.3f}")
    
    dialogue.converse(canvas)
    
    # Occasionally add perturbations
    if moment % 50 == 0 and np.random.random() < 0.3:
        # Chaos responds to chaos
        system = np.random.choice(dialogue.systems)
        if hasattr(system, 'omega1'):
            system.omega1 += np.random.normal(0, 0.1)
        else:
            system.x += np.random.normal(0, 0.01)

# Add final touches - the edge of chaos
print("Finding beauty at the edge...")

# Detect edges where chaos meets order
from scipy.ndimage import sobel
edge_magnitude = np.zeros((HEIGHT, WIDTH))

for c in range(3):
    sx = sobel(canvas[:, :, c], axis=0)
    sy = sobel(canvas[:, :, c], axis=1)
    edge_magnitude += np.sqrt(sx**2 + sy**2)

edge_magnitude /= 3

# Highlight the boundaries
threshold = np.percentile(edge_magnitude, 90)
edge_mask = edge_magnitude > threshold

# Add subtle glow at chaos boundaries
for y in range(HEIGHT):
    for x in range(WIDTH):
        if edge_mask[y, x]:
            # Golden glow at the edge of chaos
            canvas[y, x] += np.array([0.2, 0.15, 0.05]) * (edge_magnitude[y, x] / np.max(edge_magnitude))

# Normalize and save
canvas = np.clip(canvas, 0, 1)
image_array = (canvas * 255).astype(np.uint8)

image = Image.fromarray(image_array, 'RGB')
image.save('/home/norsninja/Art/artworks/2025-08-05_chaos_dialogue/chaos_dialogue_01.png')

print("Chaos dialogue complete.")
print("In chaos, I found not randomness but hidden order.")
print("The butterfly effect: beauty emerging from sensitive dependence.")