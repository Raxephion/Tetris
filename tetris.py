# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:59:46 2024 

@author: raxephion (Original)

Simple TETRIS game in Python (Work-In_Progress with improvements)

Requirements:

bash
pip install pygame
(random is a built-in module)

"""

import pygame
import random

# Initialize Pygame
pygame.init()
pygame.font.init() # Initialize font module

# --- Constants ---
BLOCK_SIZE = 30

# Playfield dimensions (in blocks)
PLAYFIELD_GRID_WIDTH = 10
PLAYFIELD_GRID_HEIGHT = 20

# Derived playfield dimensions (in pixels)
PLAYFIELD_WIDTH = PLAYFIELD_GRID_WIDTH * BLOCK_SIZE
PLAYFIELD_HEIGHT = PLAYFIELD_GRID_HEIGHT * BLOCK_SIZE

# Side Panel for Score and Next Piece
SIDE_PANEL_WIDTH = 6 * BLOCK_SIZE # Increased for better text/piece display

# Screen dimensions
SCREEN_WIDTH = PLAYFIELD_WIDTH + SIDE_PANEL_WIDTH
SCREEN_HEIGHT = PLAYFIELD_HEIGHT

# Colors (RGB values)
# colors[0] is used for background/empty cells
COLORS = [
    (25, 25, 25),       # Very Dark Grey - Background/Empty cell color
    (255, 0, 0),        # Red
    (0, 255, 0),        # Green
    (0, 0, 255),        # Blue
    (255, 255, 0),      # Yellow
    (255, 0, 255),      # Magenta
    (0, 255, 255),      # Cyan
    (255, 165, 0)       # Orange
]
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0,0,0) # For some UI elements if needed

# Tetromino Shapes (Tetris pieces)
# Each shape is a list of rows, where 1 indicates a block.
SHAPES = [
    [[1, 1, 1, 1]],         # I shape
    [[1, 1], [1, 1]],       # O shape
    [[0, 1, 1], [1, 1, 0]], # S shape (standard)
    [[1, 1, 0], [0, 1, 1]], # Z shape (standard)
    [[0, 1, 0], [1, 1, 1]], # T shape (standard)
    [[1, 0, 0], [1, 1, 1]], # L shape (standard)
    [[0, 0, 1], [1, 1, 1]]  # J shape (standard)
]

# Gameplay settings
INITIAL_FALL_SPEED = 500  # Milliseconds
FPS = 30 # Frames per second

class Tetris:
    def __init__(self, screen):
        self.screen = screen
        self.grid = [[0 for _ in range(PLAYFIELD_GRID_WIDTH)] for _ in range(PLAYFIELD_GRID_HEIGHT)]
        
        self.shapes_data = SHAPES # Use the constant
        self.colors_data = COLORS # Use the constant

        self.score = 0
        self.game_over = False
        self.last_move_down_time = pygame.time.get_ticks()
        self.fall_speed = INITIAL_FALL_SPEED

        # Fonts
        self.font_large = pygame.font.SysFont('Consolas', 30, bold=True)
        self.font_medium = pygame.font.SysFont('Consolas', 24)
        self.font_small = pygame.font.SysFont('Consolas', 18)

        # Current and Next Piece
        self.current_piece_coords = None
        self.current_piece_color_index = 0
        self.current_piece_position = [0, 0] # [row, col] on the grid

        self.next_piece_coords = None
        self.next_piece_color_index = 0
        
        self._generate_next_piece() # Generate the first "next"
        self._promote_next_to_current() # Promote it to "current" and generate another "next"

    def _generate_next_piece(self):
        """Generates a new random piece for the 'next' piece."""
        self.next_piece_coords = random.choice(self.shapes_data)
        self.next_piece_color_index = self.shapes_data.index(self.next_piece_coords) + 1
        # Ensure color index is within bounds of COLORS (excluding background)
        if self.next_piece_color_index >= len(self.colors_data):
            self.next_piece_color_index = 1 # Default to first color if something is wrong

    def _promote_next_to_current(self):
        """Moves the 'next' piece to 'current' and generates a new 'next' piece."""
        self.current_piece_coords = self.next_piece_coords
        self.current_piece_color_index = self.next_piece_color_index
        
        # Initial position for the new current piece (top-center)
        self.current_piece_position = [
            0, # Start at row 0
            PLAYFIELD_GRID_WIDTH // 2 - len(self.current_piece_coords[0]) // 2
        ]
        
        self._generate_next_piece() # Generate the new upcoming piece

        # Check for game over condition (immediate collision)
        if self.check_collision(self.current_piece_coords, self.current_piece_position):
            self.game_over = True

    def check_collision(self, piece_coords, piece_grid_offset):
        """
        Checks if the given piece at the given offset collides with
        playfield boundaries or existing locked blocks.
        piece_grid_offset is [row, col] on the grid.
        """
        offset_row, offset_col = piece_grid_offset
        for y, row_data in enumerate(piece_coords):
            for x, cell in enumerate(row_data):
                if cell: # If this part of the piece exists
                    grid_y = offset_row + y
                    grid_x = offset_col + x
                    
                    # Check boundaries
                    if not (0 <= grid_x < PLAYFIELD_GRID_WIDTH and 0 <= grid_y < PLAYFIELD_GRID_HEIGHT):
                        return True # Out of bounds
                    
                    # Check collision with existing blocks on the grid
                    if self.grid[grid_y][grid_x] != 0: # 0 is empty
                        return True # Collision with another block
        return False # No collision

    def rotate_piece(self):
        """Rotates the current piece clockwise if the rotation is valid."""
        if not self.current_piece_coords: return

        # Transpose and reverse rows for clockwise rotation
        rotated_coords = [[self.current_piece_coords[y][x] for y in range(len(self.current_piece_coords))] 
                          for x in range(len(self.current_piece_coords[0]) - 1, -1, -1)]
        
        if not self.check_collision(rotated_coords, self.current_piece_position):
            self.current_piece_coords = rotated_coords
        # Basic wall kick (try shifting left/right if collision) - simple version
        else:
            # Try shifting right
            temp_pos = [self.current_piece_position[0], self.current_piece_position[1] + 1]
            if not self.check_collision(rotated_coords, temp_pos):
                self.current_piece_coords = rotated_coords
                self.current_piece_position = temp_pos
                return
            # Try shifting left
            temp_pos = [self.current_piece_position[0], self.current_piece_position[1] - 1]
            if not self.check_collision(rotated_coords, temp_pos):
                self.current_piece_coords = rotated_coords
                self.current_piece_position = temp_pos
                return


    def move_piece(self, direction_col_change):
        """Moves the current piece horizontally if valid."""
        if not self.current_piece_coords or self.game_over: return

        new_pos = [
            self.current_piece_position[0],
            self.current_piece_position[1] + direction_col_change
        ]
        if not self.check_collision(self.current_piece_coords, new_pos):
            self.current_piece_position = new_pos

    def drop_piece(self, soft_drop=False):
        """Moves the current piece down by one step. If soft_drop, resets fall timer."""
        if not self.current_piece_coords or self.game_over: return

        new_pos = [
            self.current_piece_position[0] + 1,
            self.current_piece_position[1]
        ]
        if not self.check_collision(self.current_piece_coords, new_pos):
            self.current_piece_position = new_pos
            if soft_drop:
                 # Accelerate score or piece for soft drop if desired, here just resets timer
                self.last_move_down_time = pygame.time.get_ticks()
        else:
            self.lock_piece() # Can't move down further, so lock it

    def hard_drop_piece(self):
        """Instantly drops the piece to the lowest possible position and locks it."""
        if not self.current_piece_coords or self.game_over: return
        
        while True:
            test_pos = [self.current_piece_position[0] + 1, self.current_piece_position[1]]
            if not self.check_collision(self.current_piece_coords, test_pos):
                self.current_piece_position = test_pos
            else:
                break # Found the lowest position
        self.lock_piece()


    def lock_piece(self):
        """Locks the current piece onto the grid."""
        if not self.current_piece_coords: return

        offset_row, offset_col = self.current_piece_position
        for y, row_data in enumerate(self.current_piece_coords):
            for x, cell in enumerate(row_data):
                if cell:
                    grid_y, grid_x = offset_row + y, offset_col + x
                    # Ensure it's within bounds before locking (should be, due to checks)
                    if 0 <= grid_y < PLAYFIELD_GRID_HEIGHT and 0 <= grid_x < PLAYFIELD_GRID_WIDTH:
                        self.grid[grid_y][grid_x] = self.current_piece_color_index
        
        self.clear_lines()
        self._promote_next_to_current() # Get new piece, checks for game over

    def clear_lines(self):
        """Checks for and clears completed lines, updating the score."""
        lines_cleared = 0
        new_grid = [[0 for _ in range(PLAYFIELD_GRID_WIDTH)] for _ in range(PLAYFIELD_GRID_HEIGHT)]
        # Index for placing rows in new_grid, starting from bottom
        new_grid_row_idx = PLAYFIELD_GRID_HEIGHT - 1 

        for r in range(PLAYFIELD_GRID_HEIGHT - 1, -1, -1): # Iterate grid from bottom up
            if 0 in self.grid[r]: # If line is not full (contains an empty cell)
                new_grid[new_grid_row_idx] = self.grid[r][:] # Copy the line
                new_grid_row_idx -= 1
            else: # Line is full
                lines_cleared += 1
        
        self.grid = new_grid
        
        # Scoring (simple: 100 per line, bonus for multiple lines)
        if lines_cleared == 1: self.score += 100
        elif lines_cleared == 2: self.score += 300
        elif lines_cleared == 3: self.score += 500
        elif lines_cleared >= 4: self.score += 800 # Tetris!
        # Could also increase fall_speed here based on lines or score.

    def update_timed_fall(self):
        """Handles the automatic downward movement of the piece over time."""
        if self.game_over: return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_down_time >= self.fall_speed:
            self.drop_piece() # Not a soft drop, just a timed one
            self.last_move_down_time = current_time

    def draw_playfield(self):
        """Draws the grid and locked pieces."""
        for r in range(PLAYFIELD_GRID_HEIGHT):
            for c in range(PLAYFIELD_GRID_WIDTH):
                color_index = self.grid[r][c]
                pygame.draw.rect(self.screen, self.colors_data[color_index],
                                 (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                # Draw a border for blocks to make them more distinct
                if color_index != 0: # Don't draw border for empty cells
                    pygame.draw.rect(self.screen, GREY,
                                     (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


    def draw_current_piece(self):
        """Draws the actively falling piece."""
        if not self.current_piece_coords or self.game_over: return

        offset_row, offset_col = self.current_piece_position
        for y, row_data in enumerate(self.current_piece_coords):
            for x, cell in enumerate(row_data):
                if cell:
                    screen_x = (offset_col + x) * BLOCK_SIZE
                    screen_y = (offset_row + y) * BLOCK_SIZE
                    pygame.draw.rect(self.screen, self.colors_data[self.current_piece_color_index],
                                     (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(self.screen, GREY,
                                     (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1)


    def draw_side_panel(self):
        """Draws the score, next piece, and other info on the side panel."""
        panel_x_start = PLAYFIELD_WIDTH
        
        # Background for side panel (optional, if different from main screen fill)
        # pygame.draw.rect(self.screen, (30,30,30), (panel_x_start, 0, SIDE_PANEL_WIDTH, SCREEN_HEIGHT))

        # Score display
        score_text_render = self.font_medium.render("SCORE", True, WHITE)
        self.screen.blit(score_text_render, (panel_x_start + 20, 20))
        score_value_render = self.font_large.render(str(self.score), True, WHITE)
        self.screen.blit(score_value_render, (panel_x_start + 20, 50))

        # Next Piece display
        next_text_render = self.font_medium.render("NEXT", True, WHITE)
        self.screen.blit(next_text_render, (panel_x_start + 20, 120))

        if self.next_piece_coords:
            # Center the piece display in the side panel area for "NEXT"
            piece_width_blocks = len(self.next_piece_coords[0])
            piece_height_blocks = len(self.next_piece_coords)
            
            # Position to draw the next piece (top-left of its bounding box)
            # Try to center it horizontally in the panel area below "NEXT" text
            start_draw_x = panel_x_start + (SIDE_PANEL_WIDTH - piece_width_blocks * BLOCK_SIZE) // 2
            start_draw_y = 150 # Fixed Y position for the next piece preview

            for y, row_data in enumerate(self.next_piece_coords):
                for x, cell in enumerate(row_data):
                    if cell:
                        pygame.draw.rect(self.screen, self.colors_data[self.next_piece_color_index],
                                         (start_draw_x + x * BLOCK_SIZE, 
                                          start_draw_y + y * BLOCK_SIZE, 
                                          BLOCK_SIZE, BLOCK_SIZE), 0)
                        pygame.draw.rect(self.screen, GREY,
                                         (start_draw_x + x * BLOCK_SIZE, 
                                          start_draw_y + y * BLOCK_SIZE, 
                                          BLOCK_SIZE, BLOCK_SIZE), 1)
        
        # Controls Info
        controls_y_start = SCREEN_HEIGHT - 150
        controls = [
            "Controls:",
            "Left/Right: Move",
            "Up: Rotate",
            "Down: Soft Drop",
            "Space: Hard Drop"
        ]
        if self.game_over:
            controls = ["Game Over!", "R: Restart", "Q: Quit"]
        
        for i, line in enumerate(controls):
            text_render = self.font_small.render(line, True, WHITE)
            self.screen.blit(text_render, (panel_x_start + 10, controls_y_start + i * 20))


    def draw_game_over_screen(self):
        """Displays the 'Game Over' message on the playfield area."""
        # Semi-transparent overlay
        overlay = pygame.Surface((PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # Black with some transparency
        self.screen.blit(overlay, (0,0))

        game_over_text = self.font_large.render("GAME OVER", True, (255, 50, 50)) # Reddish
        text_rect = game_over_text.get_rect(center=(PLAYFIELD_WIDTH // 2, PLAYFIELD_HEIGHT // 2 - 30))
        self.screen.blit(game_over_text, text_rect)
        
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(PLAYFIELD_WIDTH // 2, PLAYFIELD_HEIGHT // 2 + 20))
        self.screen.blit(final_score_text, score_rect)

        # Restart/Quit instructions are now part of draw_side_panel
        # restart_text = self.font_small.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
        # restart_rect = restart_text.get_rect(center=(PLAYFIELD_WIDTH // 2, PLAYFIELD_HEIGHT // 2 + 60))
        # self.screen.blit(restart_text, restart_rect)

    def reset_game(self):
        """Resets the game state for a new game."""
        self.grid = [[0 for _ in range(PLAYFIELD_GRID_WIDTH)] for _ in range(PLAYFIELD_GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.last_move_down_time = pygame.time.get_ticks()
        self.fall_speed = INITIAL_FALL_SPEED
        
        self._generate_next_piece()
        self._promote_next_to_current()


# Main game loop
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Tetris")
    clock = pygame.time.Clock()
    
    tetris_game = Tetris(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if tetris_game.game_over:
                    if event.key == pygame.K_r:
                        tetris_game.reset_game()
                    elif event.key == pygame.K_q:
                        running = False
                else: # Game is active
                    if event.key == pygame.K_LEFT:
                        tetris_game.move_piece(-1) # Move left
                    elif event.key == pygame.K_RIGHT:
                        tetris_game.move_piece(1)  # Move right
                    elif event.key == pygame.K_DOWN:
                        tetris_game.drop_piece(soft_drop=True) # Soft drop
                    elif event.key == pygame.K_UP:
                        tetris_game.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        tetris_game.hard_drop_piece()

        # Game logic update
        if not tetris_game.game_over:
            tetris_game.update_timed_fall()

        # Drawing
        screen.fill(COLORS[0]) # Fill screen with background color

        tetris_game.draw_playfield()
        tetris_game.draw_current_piece()
        tetris_game.draw_side_panel() # Draws score, next piece, controls

        if tetris_game.game_over:
            tetris_game.draw_game_over_screen()

        pygame.display.flip() # Update the full display
        clock.tick(FPS)

    print("Game Over! Final Score:", tetris_game.score) # Keep console output
    pygame.quit()

if __name__ == "__main__":
    main()
