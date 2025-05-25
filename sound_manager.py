import pygame
import os

class SoundManager:
    def __init__(self):
        # Initialize sound dictionaries
        self.sounds = {}
        self.music = {}
        
        # Sound state
        self.sound_on = True
        self.music_on = True
        
        # Create placeholder sounds and music
        self.create_placeholder_sounds()
        self.load_sounds()
        self.load_music()
        
    def create_placeholder_sounds(self):
        """Create placeholder sound files if they don't exist"""
        # Create directories if they don't exist
        os.makedirs('assets/sounds', exist_ok=True)
        os.makedirs('assets/music', exist_ok=True)
        
        # Define sound files to create
        sound_files = {
            'paddle_hit': 'beep.wav',
            'brick_hit': 'pop.wav',
            'powerup': 'powerup.wav',
            'laser': 'laser.wav',
            'game_over': 'game_over.wav',
            'menu_select': 'select.wav'
        }
        
        music_files = {
            'menu': 'menu_music.wav',
            'gameplay': 'gameplay_music.wav'
        }
        
        # Create placeholder sound files if they don't exist
        for sound_name, filename in sound_files.items():
            path = os.path.join('assets/sounds', filename)
            if not os.path.exists(path):
                self.create_empty_sound_file(path)
                
        # Create placeholder music files if they don't exist
        for music_name, filename in music_files.items():
            path = os.path.join('assets/music', filename)
            if not os.path.exists(path):
                self.create_empty_sound_file(path)
                
    def create_empty_sound_file(self, path):
        """Create an empty sound file that won't cause errors"""
        # Create a minimal valid WAV file
        with open(path, 'wb') as f:
            # RIFF header
            f.write(b'RIFF')
            f.write((36).to_bytes(4, byteorder='little'))  # File size - 8
            f.write(b'WAVE')
            
            # Format chunk
            f.write(b'fmt ')
            f.write((16).to_bytes(4, byteorder='little'))  # Chunk size
            f.write((1).to_bytes(2, byteorder='little'))   # PCM format
            f.write((2).to_bytes(2, byteorder='little'))   # Stereo
            f.write((44100).to_bytes(4, byteorder='little'))  # Sample rate
            f.write((176400).to_bytes(4, byteorder='little'))  # Byte rate
            f.write((4).to_bytes(2, byteorder='little'))   # Block align
            f.write((16).to_bytes(2, byteorder='little'))  # Bits per sample
            
            # Data chunk
            f.write(b'data')
            f.write((0).to_bytes(4, byteorder='little'))  # Data size
                
    def load_sounds(self):
        """Load all sound effects"""
        sound_files = {
            'paddle_hit': 'assets/sounds/beep.wav',
            'brick_hit': 'assets/sounds/pop.wav',
            'powerup': 'assets/sounds/powerup.wav',
            'laser': 'assets/sounds/laser.wav',
            'game_over': 'assets/sounds/game_over.wav',
            'menu_select': 'assets/sounds/select.wav'
        }
        
        for sound_name, path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(path)
            except:
                print(f"Could not load sound: {path}")
                
    def load_music(self):
        """Load all music tracks"""
        music_files = {
            'menu': 'assets/music/menu_music.wav',
            'gameplay': 'assets/music/gameplay_music.wav'
        }
        
        for music_name, path in music_files.items():
            self.music[music_name] = path
            
    def play_sound(self, sound_name):
        """Play a sound effect if sound is enabled"""
        if self.sound_on and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
            
    def play_music(self, music_name):
        """Play a music track if music is enabled"""
        if self.music_on and music_name in self.music:
            try:
                pygame.mixer.music.load(self.music[music_name])
                pygame.mixer.music.play(-1)  # Loop indefinitely
            except:
                print(f"Could not play music: {self.music[music_name]}")
                
    def stop_music(self):
        """Stop currently playing music"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_on = not self.sound_on
        return self.sound_on
        
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_on = not self.music_on
        if self.music_on:
            try:
                pygame.mixer.music.unpause()
            except:
                pass
        else:
            try:
                pygame.mixer.music.pause()
            except:
                pass
        return self.music_on
