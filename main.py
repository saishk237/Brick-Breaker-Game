import pygame
import sys
import os
from pygame.locals import *
from game_objects import Player, Paddle, Ball, Brick, PowerUp, Laser
from layouts import create_layout
from ui import Menu, Button
from sound_manager import SoundManager
from game_manager import GameManager

# Initialize pygame
pygame.init()
pygame.mixer.init()

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

# Game states
MENU = 0
GAME = 1
SETTINGS = 2
GAME_OVER = 3

# Main game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brick Breaker - Multiplayer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MENU
        self.font = pygame.font.SysFont('Arial', 24)
        self.large_font = pygame.font.SysFont('Arial', 36)
        
        # Initialize UI and sound
        self.menu = Menu(self.screen, self.font, self.large_font)
        self.sound_manager = SoundManager()
        
        # Initialize game manager
        self.game_manager = GameManager(self.screen)
        
        # Settings
        self.sound_on = True
        self.music_on = True
        
        # Play menu music
        self.sound_manager.play_music('menu')
        
    def run(self):
        while self.running:
            if self.state == MENU:
                self.menu_loop()
            elif self.state == GAME:
                self.game_loop()
            elif self.state == SETTINGS:
                self.settings_loop()
            elif self.state == GAME_OVER:
                self.game_over_loop()
                
    def menu_loop(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_clicked = True
                
        # Draw menu and get buttons
        start_button, settings_button, quit_button = self.menu.draw_main_menu(mouse_pos)
        
        # Check button clicks
        if start_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.play_sound('menu_select')
            self.state = GAME
            self.game_manager = GameManager(self.screen)  # Reset game
            self.sound_manager.play_music('gameplay')
            
        elif settings_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.play_sound('menu_select')
            self.state = SETTINGS
            
        elif quit_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.play_sound('menu_select')
            self.running = False
            
        # Draw high scores
        if hasattr(self.menu, 'draw_high_scores'):
            self.menu.draw_high_scores(self.game_manager.high_scores)
        
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def game_loop(self):
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game_manager.toggle_pause()
                elif event.key == K_w:
                    self.game_manager.handle_action_key(1)
                elif event.key == K_UP:
                    self.game_manager.handle_action_key(2)
                    
        # Handle input
        self.game_manager.handle_input(keys)
        
        # Update game state
        self.game_manager.update()
        
        # Draw game
        self.game_manager.draw()
        
        # Check for game over
        if self.game_manager.game_over:
            self.state = GAME_OVER
            self.sound_manager.play_music('menu')
            
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def settings_loop(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = MENU
                    
        # Draw settings menu and get buttons
        sound_button, music_button, back_button = self.menu.draw_settings_menu(
            mouse_pos, self.sound_manager.sound_on, self.sound_manager.music_on
        )
        
        # Check button clicks
        if sound_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.toggle_sound()
            self.sound_manager.play_sound('menu_select')
            
        elif music_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.toggle_music()
            self.sound_manager.play_sound('menu_select')
            
        elif back_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.play_sound('menu_select')
            self.state = MENU
            
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def game_over_loop(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_clicked = True
                
        # Get player scores
        scores = [self.game_manager.players[0].score, self.game_manager.players[1].score]
        
        # Draw game over screen and get buttons
        play_again_button, main_menu_button, quit_button = self.menu.draw_game_over(
            mouse_pos, self.game_manager.winner, scores
        )
        
        # Check button clicks
        if play_again_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.play_sound('menu_select')
            self.state = GAME
            self.game_manager = GameManager(self.screen)  # Reset game
            self.sound_manager.play_music('gameplay')
            
        elif main_menu_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.play_sound('menu_select')
            self.state = MENU
            
        elif quit_button.is_clicked(mouse_pos, mouse_clicked):
            self.sound_manager.play_sound('menu_select')
            self.running = False
            
        pygame.display.flip()
        self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
