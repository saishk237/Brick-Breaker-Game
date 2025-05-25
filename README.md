# Brick Breaker - Multiplayer Edition

A modern implementation of the classic Brick Breaker game with local two-player split-screen multiplayer support, built using PyGame.

![Brick Breaker Multiplayer](https://github.com/saishk237/Brick-Breaker-Game/blob/main/screenshots/gamestart.png)

## Features

- **Local Two-Player Split Screen**: Compete against a friend on the same screen
- **Power-ups**:
  - **Multiball**: Adds two additional balls
  - **Sticky Paddle**: Makes balls stick to your paddle
  - **Laser**: Allows your paddle to shoot lasers
  - **Shrink**: Shrinks your opponent's paddle
  - **Expand**: Expands your paddle
- **5 Unique Brick Layouts**: Different patterns and challenges
  - Grid layout
  - Pyramid layout
  - Circular layout
  - Checkerboard pattern
  - Fortress layout with stronger bricks
- **Sound Effects and Music**: Immersive audio experience
- **Pause/Resume**: Take a break when needed
- **High Score Leaderboard**: Track the best performances

## Screenshots

![Main Menu](https://github.com/saishk237/Brick-Breaker-Game/raw/main/screenshots/menu.png)
![Gameplay](https://github.com/saishk237/Brick-Breaker-Game/raw/main/screenshots/gameplay.png)
![Game Over](https://github.com/saishk237/Brick-Breaker-Game/raw/main/screenshots/gameover.png)

## Controls

### Player 1 (Left Side)
- **A/D**: Move paddle left/right
- **W**: Launch ball / Fire laser

### Player 2 (Right Side)
- **Left/Right Arrows**: Move paddle left/right
- **Up Arrow**: Launch ball / Fire laser

### General
- **ESC**: Pause game / Return to menu

## Requirements

- Python 3.x
- PyGame library

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/brick-breaker.git
   cd brick-breaker
   ```

2. Install PyGame:
   ```
   pip install pygame
   ```

3. Run the game:
   ```
   python main.py
   ```

## Project Structure

```
brick_breaker/
├── main.py              # Main game entry point
├── game_objects.py      # Core game classes (Ball, Paddle, Brick, etc.)
├── game_manager.py      # Game state and logic management
├── layouts.py           # Brick layout patterns
├── ui.py                # User interface components
├── sound_manager.py     # Audio handling
├── README.md            # Documentation
├── assets/              # Game assets
│   ├── images/          # For future image assets
│   ├── sounds/          # Sound effects
│   └── music/           # Background music
└── data/                # For storing high scores
```

## Game Design

The game is structured using object-oriented programming principles with the following main classes:

- **Player**: Manages player state, score, and lives
- **Ball**: Handles ball physics and collisions
- **Paddle**: Controls paddle movement and special abilities
- **Brick**: Manages brick properties and destruction
- **PowerUp**: Implements different power-up effects
- **Game**: Main game loop and state management

## Customization

### Adding Custom Sounds
Replace the placeholder sound files in the `assets/sounds` and `assets/music` directories with your own WAV files.

### Creating New Layouts
Add new brick layouts by modifying the `create_layout` function in `layouts.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the classic Breakout and Arkanoid games
- Built with PyGame, a set of Python modules designed for writing video games
- Special thanks to the open-source community for their invaluable resources

## Future Improvements

- Add more power-ups
- Implement online multiplayer
- Create additional brick layouts
- Add boss levels
- Improve graphics with sprite animations
