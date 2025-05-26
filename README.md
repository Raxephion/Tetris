# Pygame Tetris

A simple, work-in-progress implementation of the classic Tetris game, built using Python and the Pygame library. This project was created by **raxephion** as a fun exercise and is currently under development.

## Features

*   Classic Tetris gameplay: falling tetrominoes that can be moved and rotated.
*   Line clearing: complete horizontal lines to score points and make space.
*   Increasing difficulty: (Currently, the speed is constant, but pressing 'down' accelerates the current piece).
*   Basic scoring: gain 1 point for each line cleared.
*   Game Over detection: when blocks pile up to the top.
*   Random piece generation.
*   Piece rotation.

## Screenshot

*(It would be great to add a screenshot of the game in action here!)*
![Tetris Gameplay](placeholder_screenshot.png)
*(Replace `placeholder_screenshot.png` with an actual image file in your repository)*

## Requirements

*   Python 3.x
*   Pygame library

The `random` module is part of the Python standard library, so no separate installation is needed for it.

## Installation

1.  **Clone the repository (or download the script):**
    If you're using Git:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```
    Otherwise, just download the Python script (`.py` file).

2.  **Ensure Python 3 is installed.**
    You can download it from [python.org](https://www.python.org/downloads/).

3.  **Install Pygame:**
    Open your terminal or command prompt and run:
    ```bash
    pip install pygame
    ```

## How to Play

1.  Navigate to the directory where you saved the `tetris_game.py` file (or the cloned repository).
2.  Run the game using Python:
    ```bash
    python tetris_game.py
    ```
    *(Assuming your Python file is named `tetris_game.py`. If not, replace it with the actual filename.)*

## Controls

*   **Left Arrow Key:** Move the current piece left.
*   **Right Arrow Key:** Move the current piece right.
*   **Down Arrow Key:** Move the current piece down faster (soft drop).
*   **Up Arrow Key:** Rotate the current piece clockwise.

## Game Logic Overview

*   The game board is a grid.
*   Tetrominoes (shapes) fall from the top of the screen.
*   Players can move pieces left, right, accelerate their fall, or rotate them.
*   When a piece can no longer move down, it locks into place.
*   If a horizontal line is completely filled with blocks, it is cleared, and the blocks above it move down.
*   The game ends when a newly spawned piece cannot fit on the board (i.e., it collides immediately).

## Future Enhancements (To-Do / Ideas)

Since this is a work-in-progress, here are some ideas for future development:

*   **Next Piece Preview:** Show the player which piece is coming next.
*   **Hold Piece Functionality:** Allow the player to "hold" a piece and swap it out later.
*   **Hard Drop:** Instantly drop the piece to the bottom (e.g., with Spacebar).
*   **Wall Kicks/Rotation System:** Implement a more sophisticated rotation system (like SRS) to allow pieces to "kick" off walls or other blocks when rotated near them.
*   **Ghost Piece:** Show a faint outline of where the current piece will land.
*   **Levels & Increasing Speed:** Increase game speed as the player scores more points or clears more lines.
*   **Improved UI:**
    *   Display score, lines cleared, and current level more prominently.
    *   A proper "Game Over" screen with options to restart.
*   **Sound Effects & Music:** Add audio cues for piece movement, line clears, and game over.
*   **High Score System:** Save and display high scores.
*   **Pause Functionality.**

## Author

*   **raxephion**

---

Feel free to contribute, modify, or use this code as a learning resource!
