# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:59:46 2024

@author: raxephion

Simple TETRIS game in Python (Work-In_Progress)

Requirements:

bash
pip install pygame
pip install random


"""



import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 600
block_size = 30

# Define colors (RGB values)
colors = [
    (0, 0, 0),          # Black - Background color
    (255, 0, 0),        # Red
    (0, 255, 0),        # Green
    (0, 0, 255),        # Blue
    (255, 255, 0),      # Yellow
    (255, 0, 255),      # Magenta
    (0, 255, 255),      # Cyan
    (255, 165, 0)       # Orange
]

# Define shapes (Tetris pieces)
shapes = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1, 1], [1, 0, 0]],  # L shape
    [[1, 1, 1], [0, 0, 1]]   # J shape
]

class Tetris:
    def __init__(self, screen):
        self.screen = screen
        # Create a grid of empty cells
        self.grid = [[0 for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]
        self.shapes = shapes
        self.colors = colors
        self.current_shape = self.get_new_shape()
        self.shape_index = self.shapes.index(self.current_shape)  # Track the shape index
        # Initial position of the current shape
        self.shape_position = [0, screen_width // block_size // 2 - len(self.current_shape[0]) // 2]
        self.score = 0
        self.game_over = False
        self.last_move_down = pygame.time.get_ticks()

    # Randomly select a new shape
    def get_new_shape(self):
        shape = random.choice(self.shapes)
        self.shape_index = self.shapes.index(shape)  # Update index when getting a new shape
        return shape

    # Draw the grid
    def draw_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                pygame.draw.rect(self.screen, self.colors[self.grid[row][col]],
                                 (col * block_size, row * block_size, block_size, block_size), 0)

    # Draw the current shape on the screen
    def draw_shape(self, shape, offset, color_index):
        off_y, off_x = offset
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.colors[color_index],
                                     ((off_x + x) * block_size, (off_y + y) * block_size, block_size, block_size), 0)

    # Rotate the shape 90 degrees clockwise
    def rotate_shape(self, shape):
        return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

    # Check for collisions
    def check_collision(self, shape, offset):
        off_y, off_x = offset
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Check if the shape is out of bounds or colliding with another shape
                    if y + off_y >= len(self.grid) or x + off_x >= len(self.grid[0]) or x + off_x < 0 or self.grid[y + off_y][x + off_x]:
                        return True
        return False

    # Remove completed lines and update the score
    def remove_lines(self):
        new_grid = [[0 for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]
        index = len(new_grid) - 1
        for row in reversed(self.grid):
            if 0 in row:
                new_grid[index] = row
                index -= 1
            else:
                self.score += 1
        self.grid = new_grid

    # Move the current shape
    def move(self, direction):
        new_pos = self.shape_position[:]
        
        if direction == "left":
            new_pos = [self.shape_position[0], self.shape_position[1] - 1]
        elif direction == "right":
            new_pos = [self.shape_position[0], self.shape_position[1] + 1]
        elif direction == "down":
            new_pos = [self.shape_position[0] + 1, self.shape_position[1]]
            self.last_move_down = pygame.time.get_ticks()  # Accelerate the block's fall when the down key is pressed
        elif direction == "rotate":
            rotated_shape = self.rotate_shape(self.current_shape)
            if not self.check_collision(rotated_shape, self.shape_position):
                self.current_shape = rotated_shape
            return

        if not self.check_collision(self.current_shape, new_pos):
            self.shape_position = new_pos

    # Update the game state
    def update(self):
        current_time = pygame.time.get_ticks()
        # Move the shape down if enough time has passed
        if current_time - self.last_move_down >= 500:
            self.shape_position[0] += 1
            if self.check_collision(self.current_shape, self.shape_position):
                self.shape_position[0] -= 1
                self.lock_shape()
            self.last_move_down = current_time

        self.draw_grid()
        self.draw_shape(self.current_shape, self.shape_position, self.shape_index + 1)

    # Lock the shape in place when it cannot move further down
    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.shape_position[0]][x + self.shape_position[1]] = self.shape_index + 1
        self.current_shape = self.get_new_shape()
        self.shape_position = [0, screen_width // block_size // 2 - len(self.current_shape[0]) // 2]
        if self.check_collision(self.current_shape, self.shape_position):
            self.game_over = True
        self.remove_lines()

# Main game loop
def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    tetris = Tetris(screen)

    while not tetris.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move("left")
                elif event.key == pygame.K_RIGHT:
                    tetris.move("right")
                elif event.key == pygame.K_DOWN:
                    tetris.move("down")
                elif event.key == pygame.K_UP:
                    tetris.move("rotate")

        screen.fill((0, 0, 0))  # Clear the screen
        tetris.update()  # Update the game state
        pygame.display.update()  # Update the display
        clock.tick(30)  # Limit the frame rate to 30 FPS

    print("Game Over! Final Score:", tetris.score)
    pygame.quit()

if __name__ == "__main__":
    main()
