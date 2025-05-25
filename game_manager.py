import pygame
import random
import os
from pygame.locals import *
from game_objects import Player, Paddle, Ball, Brick, PowerUp, Laser
from layouts import create_layout
from ui import Menu
from sound_manager import SoundManager

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
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

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.large_font = pygame.font.SysFont('Arial', 36)
        self.menu = Menu(screen, self.font, self.large_font)
        self.sound_manager = SoundManager()
        
        # Game objects
        self.players = []
        self.balls = []
        self.bricks = []
        self.powerups = []
        self.lasers = []
        
        # Game state
        self.paused = False
        self.current_layout = 1
        self.game_over = False
        self.winner = 0
        
        # High scores
        self.high_scores = self.load_high_scores()
        
        # Initialize game
        self.init_game()
        
    def init_game(self):
        # Create players
        player1 = Player(1, {'left': K_a, 'right': K_d, 'action': K_w}, 'left')
        player2 = Player(2, {'left': K_LEFT, 'right': K_RIGHT, 'action': K_UP}, 'right')
        
        # Create paddles
        paddle1 = Paddle(SCREEN_WIDTH//4 - 50, SCREEN_HEIGHT - 30, color=BLUE)
        paddle2 = Paddle(3*SCREEN_WIDTH//4 - 50, SCREEN_HEIGHT - 30, color=RED)
        
        player1.paddle = paddle1
        player2.paddle = paddle2
        
        self.players = [player1, player2]
        
        # Create initial balls
        ball1 = Ball(SCREEN_WIDTH//4, SCREEN_HEIGHT - 50)
        ball1.attached_to = paddle1
        ball1.attach_offset = paddle1.rect.width // 2
        
        ball2 = Ball(3*SCREEN_WIDTH//4, SCREEN_HEIGHT - 50)
        ball2.attached_to = paddle2
        ball2.attach_offset = paddle2.rect.width // 2
        
        self.balls = [ball1, ball2]
        
        # Create bricks
        self.bricks = create_layout(self.current_layout, SCREEN_WIDTH, SCREEN_HEIGHT, Brick)
        
        # Clear powerups and lasers
        self.powerups = []
        self.lasers = []
        
        # Reset game state
        self.paused = False
        self.game_over = False
        
        # Play game music
        self.sound_manager.play_music('gameplay')
        
    def load_high_scores(self):
        try:
            if os.path.exists('data/high_scores.txt'):
                with open('data/high_scores.txt', 'r') as f:
                    scores = [int(line.strip()) for line in f.readlines()]
                return sorted(scores, reverse=True)[:5]  # Top 5 scores
            return [0, 0, 0, 0, 0]
        except:
            return [0, 0, 0, 0, 0]
            
    def save_high_scores(self):
        os.makedirs('data', exist_ok=True)
        with open('data/high_scores.txt', 'w') as f:
            for score in self.high_scores:
                f.write(f"{score}\n")
                
    def update_high_scores(self, score):
        self.high_scores.append(score)
        self.high_scores = sorted(self.high_scores, reverse=True)[:5]  # Keep top 5
        self.save_high_scores()
        
    def handle_input(self, keys):
        if self.paused:
            return
            
        # Player 1 controls
        if keys[self.players[0].controls['left']]:
            self.players[0].paddle.move('left', 0, SCREEN_WIDTH//2 - 10)
        if keys[self.players[0].controls['right']]:
            self.players[0].paddle.move('right', 0, SCREEN_WIDTH//2 - 10)
            
        # Player 2 controls
        if keys[self.players[1].controls['left']]:
            self.players[1].paddle.move('left', SCREEN_WIDTH//2 + 10, SCREEN_WIDTH)
        if keys[self.players[1].controls['right']]:
            self.players[1].paddle.move('right', SCREEN_WIDTH//2 + 10, SCREEN_WIDTH)
            
    def handle_action_key(self, player_id):
        player = self.players[player_id - 1]
        
        # Find balls attached to this player's paddle
        for ball in self.balls:
            if ball.attached_to == player.paddle:
                ball.release()
                self.sound_manager.play_sound('paddle_hit')
                return
                
        # If no balls are attached, try to shoot laser
        if player.paddle.laser_active and player.paddle.shoot_laser():
            laser = Laser(player.paddle.rect.centerx, player.paddle.rect.top)
            self.lasers.append(laser)
            self.sound_manager.play_sound('laser')
            
    def update(self):
        if self.paused or self.game_over:
            return
            
        # Update paddles
        for player in self.players:
            player.paddle.update()
            
        # Update balls
        balls_to_remove = []
        for i, ball in enumerate(self.balls):
            ball.update()
            
            # Check wall collisions
            if ball.check_wall_collision(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT):
                # Ball went below bottom boundary
                balls_to_remove.append(i)
                continue
                
            # Check paddle collisions
            for player in self.players:
                if ball.check_paddle_collision(player.paddle):
                    self.sound_manager.play_sound('paddle_hit')
                    break
                    
            # Check brick collisions
            for j, brick in enumerate(self.bricks):
                if ball.check_brick_collision(brick):
                    self.sound_manager.play_sound('brick_hit')
                    if brick.hit():
                        # Brick is destroyed
                        player_id = 1 if ball.pos.x < SCREEN_WIDTH//2 else 2
                        self.players[player_id-1].add_score(brick.points)
                        
                        # Check for powerup
                        if brick.should_drop_powerup():
                            powerup_type = random.randint(0, 4)  # Random powerup
                            self.powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery, powerup_type))
                            
                        # Remove brick
                        self.bricks.pop(j)
                    break
                    
        # Remove balls that went out of bounds
        for i in sorted(balls_to_remove, reverse=True):
            if i < len(self.balls):
                self.balls.pop(i)
                
        # Check if player lost all balls in their half
        player1_has_balls = False
        player2_has_balls = False
        
        for ball in self.balls:
            if ball.pos.x < SCREEN_WIDTH//2:
                player1_has_balls = True
            else:
                player2_has_balls = True
                
        # If a player has no balls, they lose a life
        if not player1_has_balls and self.players[0].lives > 0:
            self.players[0].lose_life()
            if self.players[0].lives > 0:
                # Add a new ball
                ball = Ball(SCREEN_WIDTH//4, SCREEN_HEIGHT - 50)
                ball.attached_to = self.players[0].paddle
                ball.attach_offset = self.players[0].paddle.rect.width // 2
                self.balls.append(ball)
                
        if not player2_has_balls and self.players[1].lives > 0:
            self.players[1].lose_life()
            if self.players[1].lives > 0:
                # Add a new ball
                ball = Ball(3*SCREEN_WIDTH//4, SCREEN_HEIGHT - 50)
                ball.attached_to = self.players[1].paddle
                ball.attach_offset = self.players[1].paddle.rect.width // 2
                self.balls.append(ball)
                
        # Update powerups
        powerups_to_remove = []
        for i, powerup in enumerate(self.powerups):
            powerup.update()
            
            # Check if powerup is out of bounds
            if powerup.pos.y > SCREEN_HEIGHT:
                powerups_to_remove.append(i)
                continue
                
            # Check paddle collisions
            for player in self.players:
                if powerup.check_paddle_collision(player.paddle):
                    self.sound_manager.play_sound('powerup')
                    self.apply_powerup(powerup, player)
                    powerups_to_remove.append(i)
                    break
                    
        # Remove collected or out-of-bounds powerups
        for i in sorted(powerups_to_remove, reverse=True):
            if i < len(self.powerups):
                self.powerups.pop(i)
                
        # Update lasers
        lasers_to_remove = []
        for i, laser in enumerate(self.lasers):
            laser.update()
            
            # Check if laser is out of bounds
            if laser.rect.bottom < 0:
                lasers_to_remove.append(i)
                continue
                
            # Check brick collisions
            for j, brick in enumerate(self.bricks):
                if laser.check_brick_collision(brick):
                    # Determine which player shot the laser
                    player_id = 1 if laser.rect.x < SCREEN_WIDTH//2 else 2
                    
                    if brick.hit():
                        # Brick is destroyed
                        self.players[player_id-1].add_score(brick.points)
                        
                        # Check for powerup
                        if brick.should_drop_powerup():
                            powerup_type = random.randint(0, 4)  # Random powerup
                            self.powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery, powerup_type))
                            
                        # Remove brick
                        self.bricks.pop(j)
                        
                    lasers_to_remove.append(i)
                    self.sound_manager.play_sound('brick_hit')
                    break
                    
        # Remove lasers that hit bricks or went out of bounds
        for i in sorted(lasers_to_remove, reverse=True):
            if i < len(self.lasers):
                self.lasers.pop(i)
                
        # Check for game over conditions
        if self.players[0].lives <= 0 or self.players[1].lives <= 0:
            self.game_over = True
            self.sound_manager.play_sound('game_over')
            
            # Determine winner
            if self.players[0].lives <= 0 and self.players[1].lives <= 0:
                # Both players lost, determine winner by score
                if self.players[0].score > self.players[1].score:
                    self.winner = 1
                else:
                    self.winner = 2
            elif self.players[0].lives <= 0:
                self.winner = 2
            else:
                self.winner = 1
                
            # Update high scores
            max_score = max(self.players[0].score, self.players[1].score)
            self.update_high_scores(max_score)
            
        # Check if all bricks are destroyed
        if len(self.bricks) == 0:
            # Load next layout
            self.current_layout = (self.current_layout % 5) + 1
            self.bricks = create_layout(self.current_layout, SCREEN_WIDTH, SCREEN_HEIGHT, Brick)
            
    def apply_powerup(self, powerup, player):
        if powerup.type == MULTIBALL:
            # Add two more balls
            for _ in range(2):
                ball = Ball(
                    player.paddle.rect.centerx,
                    player.paddle.rect.top - 10,
                    speed=5
                )
                self.balls.append(ball)
                
        elif powerup.type == STICKY:
            player.paddle.sticky = True
            
        elif powerup.type == LASER:
            player.paddle.laser_active = True
            
        elif powerup.type == SHRINK:
            # Shrink opponent's paddle
            opponent = self.players[0] if player.id == 2 else self.players[1]
            opponent.paddle.resize(0.7)
            
        elif powerup.type == EXPAND:
            # Expand player's paddle
            player.paddle.resize(1.3)
            
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game UI
        self.menu.draw_game_ui(self.players)
        
        # Draw bricks
        for brick in self.bricks:
            brick.draw(self.screen)
            
        # Draw paddles
        for player in self.players:
            player.paddle.draw(self.screen)
            
        # Draw balls
        for ball in self.balls:
            ball.draw(self.screen)
            
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
            
        # Draw lasers
        for laser in self.lasers:
            laser.draw(self.screen)
            
        # Draw pause menu if paused
        if self.paused:
            self.menu.draw_pause_menu(pygame.mouse.get_pos())
            
    def toggle_pause(self):
        self.paused = not self.paused
