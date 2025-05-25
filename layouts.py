import math
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

def create_layout(layout_num, screen_width, screen_height, Brick):
    """
    Create a brick layout based on the layout number
    Returns a list of Brick objects
    """
    bricks = []
    brick_width = 60
    brick_height = 20
    
    if layout_num == 1:
        # Basic grid layout
        for row in range(5):
            for col in range(10):
                x = col * (brick_width + 10) + 100
                y = row * (brick_height + 5) + 50
                color = [RED, ORANGE, YELLOW, GREEN, BLUE][row]
                points = (5-row)*10
                bricks.append(Brick(x, y, brick_width, brick_height, color, points))
                
    elif layout_num == 2:
        # Pyramid layout
        for row in range(8):
            for col in range(row + 1):
                x = (screen_width // 2) - (row * brick_width // 2) + col * brick_width
                y = 50 + row * brick_height
                color = [RED, ORANGE, YELLOW, GREEN, BLUE][row % 5]
                points = (8-row)*10
                bricks.append(Brick(x, y, brick_width, brick_height, color, points))
                
    elif layout_num == 3:
        # Circular layout
        center_x = screen_width // 2
        center_y = screen_height // 3
        for angle in range(0, 360, 15):
            for radius in range(100, 200, 30):
                rad = math.radians(angle)
                x = center_x + radius * math.cos(rad) - brick_width // 2
                y = center_y + radius * math.sin(rad) - brick_height // 2
                color = [RED, ORANGE, YELLOW, GREEN, BLUE][radius % 5 // 30]
                bricks.append(Brick(x, y, brick_width, brick_height, color))
                
    elif layout_num == 4:
        # Checkerboard pattern
        for row in range(8):
            for col in range(12):
                if (row + col) % 2 == 0:
                    x = col * brick_width + 50
                    y = row * brick_height + 50
                    color = [RED, YELLOW, GREEN, BLUE][((row + col) // 2) % 4]
                    bricks.append(Brick(x, y, brick_width, brick_height, color))
                    
    elif layout_num == 5:
        # Fortress layout with stronger bricks in the center
        for row in range(10):
            for col in range(12):
                x = col * brick_width + 50
                y = row * brick_height + 50
                
                # Center bricks are stronger
                if 4 <= row <= 6 and 4 <= col <= 8:
                    color = RED
                    hits = 3
                    points = 30
                else:
                    color = [YELLOW, GREEN, BLUE][((row + col)) % 3]
                    hits = 1
                    points = 10
                    
                bricks.append(Brick(x, y, brick_width, brick_height, color, points, hits))
    
    return bricks
