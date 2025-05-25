import pygame
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

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=GREEN, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border
        
        # Draw text
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click
        
class Menu:
    def __init__(self, screen, font, large_font):
        self.screen = screen
        self.font = font
        self.large_font = large_font
        
    def draw_main_menu(self, mouse_pos):
        self.screen.fill(BLACK)
        
        # Title
        title = self.large_font.render("BRICK BREAKER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font.render("Multiplayer Edition", True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Buttons
        start_button = Button(SCREEN_WIDTH//2 - 100, 250, 200, 50, "Start Game")
        settings_button = Button(SCREEN_WIDTH//2 - 100, 320, 200, 50, "Settings")
        quit_button = Button(SCREEN_WIDTH//2 - 100, 390, 200, 50, "Quit")
        
        # Check hover states
        start_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        # Draw buttons
        start_button.draw(self.screen, self.font)
        settings_button.draw(self.screen, self.font)
        quit_button.draw(self.screen, self.font)
        
        # Instructions
        instructions = [
            "Player 1: A/D to move, W to launch ball/fire laser",
            "Player 2: Left/Right arrows to move, Up to launch ball/fire laser",
            "Collect power-ups to gain advantages!"
        ]
        
        for i, line in enumerate(instructions):
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 480 + i*30))
            
        return start_button, settings_button, quit_button
        
    def draw_settings_menu(self, mouse_pos, sound_on, music_on):
        self.screen.fill(BLACK)
        
        # Title
        title = self.large_font.render("SETTINGS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Sound toggle button
        sound_text = "Sound: ON" if sound_on else "Sound: OFF"
        sound_button = Button(SCREEN_WIDTH//2 - 100, 200, 200, 50, sound_text)
        
        # Music toggle button
        music_text = "Music: ON" if music_on else "Music: OFF"
        music_button = Button(SCREEN_WIDTH//2 - 100, 270, 200, 50, music_text)
        
        # Back button
        back_button = Button(SCREEN_WIDTH//2 - 100, 400, 200, 50, "Back")
        
        # Check hover states
        sound_button.check_hover(mouse_pos)
        music_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        # Draw buttons
        sound_button.draw(self.screen, self.font)
        music_button.draw(self.screen, self.font)
        back_button.draw(self.screen, self.font)
        
        return sound_button, music_button, back_button
        
    def draw_game_over(self, mouse_pos, winner, scores):
        self.screen.fill(BLACK)
        
        # Title
        title = self.large_font.render("GAME OVER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Winner
        winner_text = self.font.render(f"Player {winner} Wins!", True, YELLOW)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH//2, 170))
        self.screen.blit(winner_text, winner_rect)
        
        # Scores
        score_text = self.font.render(f"Player 1: {scores[0]}  |  Player 2: {scores[1]}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 220))
        self.screen.blit(score_text, score_rect)
        
        # Buttons
        play_again_button = Button(SCREEN_WIDTH//2 - 100, 300, 200, 50, "Play Again")
        main_menu_button = Button(SCREEN_WIDTH//2 - 100, 370, 200, 50, "Main Menu")
        quit_button = Button(SCREEN_WIDTH//2 - 100, 440, 200, 50, "Quit")
        
        # Check hover states
        play_again_button.check_hover(mouse_pos)
        main_menu_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        # Draw buttons
        play_again_button.draw(self.screen, self.font)
        main_menu_button.draw(self.screen, self.font)
        quit_button.draw(self.screen, self.font)
        
        return play_again_button, main_menu_button, quit_button
        
    def draw_pause_menu(self, mouse_pos):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.large_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(pause_text, pause_rect)
        
        # Buttons
        resume_button = Button(SCREEN_WIDTH//2 - 100, 300, 200, 50, "Resume")
        main_menu_button = Button(SCREEN_WIDTH//2 - 100, 370, 200, 50, "Main Menu")
        
        # Check hover states
        resume_button.check_hover(mouse_pos)
        main_menu_button.check_hover(mouse_pos)
        
        # Draw buttons
        resume_button.draw(self.screen, self.font)
        main_menu_button.draw(self.screen, self.font)
        
        return resume_button, main_menu_button
        
    def draw_game_ui(self, players, split_screen=True):
        # Draw divider for split screen
        if split_screen:
            pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 2)
            
        # Player 1 info
        p1_text = self.font.render(f"P1: {players[0].score}", True, WHITE)
        self.screen.blit(p1_text, (20, 10))
        
        # Player 1 lives
        for i in range(players[0].lives):
            pygame.draw.circle(self.screen, WHITE, (20 + i*20, 40), 8)
            
        # Player 2 info
        p2_text = self.font.render(f"P2: {players[1].score}", True, WHITE)
        self.screen.blit(p2_text, (SCREEN_WIDTH - 120, 10))
        
        # Player 2 lives
        for i in range(players[1].lives):
            pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH - 20 - i*20, 40), 8)
            
    def draw_high_scores(self, high_scores):
        """Draw high scores section on the screen"""
        # Draw high scores section
        title = self.font.render("HIGH SCORES", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH - 200, 50))
        
        for i, score in enumerate(high_scores):
            score_text = self.font.render(f"{i+1}. {score}", True, WHITE)
            self.screen.blit(score_text, (SCREEN_WIDTH - 200, 90 + i*30))
