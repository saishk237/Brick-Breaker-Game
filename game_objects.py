import pygame
import random
import math
from pygame.locals import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Power-up types
MULTIBALL = 0
STICKY = 1
LASER = 2
SHRINK = 3
EXPAND = 4

class Player:
    def __init__(self, player_id, controls, screen_half):
        self.id = player_id
        self.score = 0
        self.lives = 3
        self.controls = controls  # Dictionary with 'left', 'right', and 'action' keys
        self.screen_half = screen_half  # 'left' or 'right' for split screen
        self.paddle = None
        self.active_powerups = []
        
    def reset(self):
        self.active_powerups = []
        
    def add_score(self, points):
        self.score += points
        
    def lose_life(self):
        self.lives -= 1
        return self.lives <= 0
        
class Paddle:
    def __init__(self, x, y, width=100, height=20, color=BLUE, speed=8):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        self.sticky = False
        self.laser_active = False
        self.laser_cooldown = 0
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def move(self, direction, boundary_left, boundary_right):
        if direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed
            
        # Keep paddle within boundaries
        if self.rect.left < boundary_left:
            self.rect.left = boundary_left
        if self.rect.right > boundary_right:
            self.rect.right = boundary_right
            
    def resize(self, factor):
        center = self.rect.centerx
        self.rect.width = int(self.rect.width * factor)
        self.rect.centerx = center
        
    def shoot_laser(self):
        if self.laser_active and self.laser_cooldown <= 0:
            self.laser_cooldown = 30  # Frames until next laser shot
            return True
        return False
        
    def update(self):
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1
            
class Ball:
    def __init__(self, x, y, radius=10, color=WHITE, speed=5):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.color = color
        self.speed = speed
        self.velocity = pygame.Vector2(random.choice([-1, 1]) * speed / 2, -speed)
        self.attached_to = None
        self.attach_offset = 0
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        
    def update(self):
        if self.attached_to is None:
            self.pos += self.velocity
        else:
            # If ball is attached to paddle (sticky powerup)
            self.pos.x = self.attached_to.rect.x + self.attach_offset
            self.pos.y = self.attached_to.rect.top - self.radius
            
    def check_wall_collision(self, left_boundary, right_boundary, top_boundary, bottom_boundary):
        # Left and right walls
        if self.pos.x - self.radius < left_boundary:
            self.pos.x = left_boundary + self.radius
            self.velocity.x = abs(self.velocity.x)
        elif self.pos.x + self.radius > right_boundary:
            self.pos.x = right_boundary - self.radius
            self.velocity.x = -abs(self.velocity.x)
            
        # Top wall
        if self.pos.y - self.radius < top_boundary:
            self.pos.y = top_boundary + self.radius
            self.velocity.y = abs(self.velocity.y)
            
        # Check if ball is below bottom boundary (lost)
        return self.pos.y + self.radius > bottom_boundary
        
    def check_paddle_collision(self, paddle):
        if self.attached_to == paddle:
            return False
            
        if self.pos.y + self.radius >= paddle.rect.top and self.pos.y - self.radius <= paddle.rect.bottom:
            if self.pos.x + self.radius >= paddle.rect.left and self.pos.x - self.radius <= paddle.rect.right:
                # Calculate bounce angle based on where ball hit the paddle
                relative_intersect_x = (paddle.rect.centerx - self.pos.x) / (paddle.rect.width / 2)
                bounce_angle = relative_intersect_x * (math.pi / 3)  # Max 60 degree bounce
                
                # Set new velocity
                speed = math.sqrt(self.velocity.x**2 + self.velocity.y**2)
                self.velocity.x = -speed * math.sin(bounce_angle)
                self.velocity.y = -speed * math.cos(bounce_angle)
                
                # Position adjustment to prevent sticking
                self.pos.y = paddle.rect.top - self.radius
                
                # Handle sticky paddle
                if paddle.sticky:
                    self.attached_to = paddle
                    self.attach_offset = self.pos.x - paddle.rect.x
                    
                return True
        return False
        
    def check_brick_collision(self, brick):
        # Calculate the closest point on the brick to the ball
        closest_x = max(brick.rect.left, min(self.pos.x, brick.rect.right))
        closest_y = max(brick.rect.top, min(self.pos.y, brick.rect.bottom))
        
        # Calculate the distance between the ball's center and this closest point
        distance_x = self.pos.x - closest_x
        distance_y = self.pos.y - closest_y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        # If the distance is less than the ball's radius, a collision occurred
        if distance < self.radius:
            # Determine bounce direction
            if abs(distance_x) > abs(distance_y):
                self.velocity.x = -self.velocity.x
            else:
                self.velocity.y = -self.velocity.y
                
            return True
        return False
        
    def release(self):
        if self.attached_to is not None:
            self.attached_to = None
            self.velocity.y = -abs(self.velocity.y)  # Ensure ball goes upward
            
class Brick:
    def __init__(self, x, y, width=60, height=20, color=RED, points=10, hits_to_break=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.points = points
        self.hits_to_break = hits_to_break
        self.hits = 0
        self.powerup_chance = 0.2  # 20% chance to drop a powerup
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def hit(self):
        self.hits += 1
        return self.hits >= self.hits_to_break
        
    def should_drop_powerup(self):
        return random.random() < self.powerup_chance
        
class PowerUp:
    def __init__(self, x, y, type_id):
        self.pos = pygame.Vector2(x, y)
        self.type = type_id
        self.radius = 10
        self.speed = 2
        self.active = True
        
        # Set color based on type
        if self.type == MULTIBALL:
            self.color = YELLOW
        elif self.type == STICKY:
            self.color = GREEN
        elif self.type == LASER:
            self.color = RED
        elif self.type == SHRINK:
            self.color = BLUE
        elif self.type == EXPAND:
            self.color = WHITE
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        
    def update(self):
        self.pos.y += self.speed
        
    def check_paddle_collision(self, paddle):
        if (self.pos.y + self.radius >= paddle.rect.top and 
            self.pos.y - self.radius <= paddle.rect.bottom and
            self.pos.x + self.radius >= paddle.rect.left and 
            self.pos.x - self.radius <= paddle.rect.right):
            return True
        return False
        
class Laser:
    def __init__(self, x, y, speed=10, color=RED):
        self.rect = pygame.Rect(x - 2, y, 4, 10)
        self.speed = speed
        self.color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def update(self):
        self.rect.y -= self.speed
        
    def check_brick_collision(self, brick):
        return self.rect.colliderect(brick.rect)
