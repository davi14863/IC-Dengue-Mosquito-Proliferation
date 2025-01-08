import pygame
import numpy
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20

# Calculate grid size
cols = WIDTH // CELL_SIZE
rows = HEIGHT // CELL_SIZE

# Initialize grids
grid_mosquitos = [[0 for _ in range(cols)] for _ in range(rows)]
grid_values = [[random.choice([0, 1, 0.5, 0.5, 0, 0, 0.2]) for _ in range(cols)] for _ in range(rows)]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test IC1")

# Mosquito iteration parameters
moviment_factor = 0.40
moviment_dev = 0.10
direction_dev = 0.10
death_factor = 20
reproduction_factor = 50
eggs_Quantity = 100
max_mosquito_count = 1000

# Function to validate grids
def validate_grid(grid):
    for row in grid:
        for cell in row:
            if not (0 <= cell <= max_mosquito_count):
                print(f"Invalid cell value detected: {cell}")
                return False
    return True

# Function to draw the grid
def draw_grid_mosquitos():
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            green = 255
            if grid_mosquitos[y][x] > 127:
                green = max(0, green - ((grid_mosquitos[y][x] - 127) * 2))
            blue = 0
            if grid_mosquitos[y][x] < 127:
                blue = min(255, (127 - grid_mosquitos[y][x]) * 2)
            pygame.draw.rect(screen, (255, green, blue), rect)

            if grid_values[y][x] > 0:
                pygame.draw.line(screen, (255 - grid_values[y][x] * 255,255 - grid_values[y][x] * 255,255),(x * CELL_SIZE,y * CELL_SIZE),((x + 1) * CELL_SIZE,(y + 1) * CELL_SIZE),2)
                pygame.draw.line(screen, (255 - grid_values[y][x] * 255,255 - grid_values[y][x] * 255,255),((x + 1) * CELL_SIZE,y * CELL_SIZE),(x * CELL_SIZE,(y + 1) * CELL_SIZE),2)

# Function to move the mosquitos
def move_grid_mosquitos():
    global grid_mosquitos

    new_grid_mosquitos = [[0 for _ in range(cols)] for _ in range(rows)]

    for y in range(rows):
        for x in range(cols):
            move_percentage = numpy.clip(numpy.random.normal(moviment_factor, moviment_dev), 0, 1)
            percentages = numpy.random.normal([0.25, 0.25, 0.25, 0.25], direction_dev, 4)

            # Ensure percentages are valid
            percentages = numpy.maximum(percentages, 0)
            total_percentages = numpy.sum(percentages)
            if total_percentages == 0:
                percentages = [0.25, 0.25, 0.25, 0.25]
            else:
                percentages /= total_percentages

            value = max(0, math.floor(grid_mosquitos[y][x] * (1 - move_percentage)))
            moving_value = grid_mosquitos[y][x] - value

            if x > 0:
                new_grid_mosquitos[y][x - 1] += math.floor(moving_value * percentages[0])
            if x < cols - 1:
                new_grid_mosquitos[y][x + 1] += math.floor(moving_value * percentages[1])
            if y > 0:
                new_grid_mosquitos[y - 1][x] += math.floor(moving_value * percentages[2])
            if y < rows - 1:
                new_grid_mosquitos[y + 1][x] += math.floor(moving_value * percentages[3])

            # Remaining value stays in the same cell
            new_grid_mosquitos[y][x] += value

    grid_mosquitos = new_grid_mosquitos

# Function to reproduce mosquitos
def reproduce_grid_mosquitos():
    global grid_mosquitos, grid_values

    for y in range(rows):
        for x in range(cols):
            if grid_values[y][x] == 1:
                new_mosquitos = math.floor(
                    eggs_Quantity * grid_mosquitos[y][x] * (reproduction_factor / 100) * (1 - (grid_mosquitos[y][x] / max_mosquito_count))
                )
                grid_mosquitos[y][x] += max(0, new_mosquitos)
                grid_mosquitos[y][x] = min(max_mosquito_count, grid_mosquitos[y][x])

# Function to kill mosquitos
def kill_grid_mosquitos():
    global grid_mosquitos

    for y in range(rows):
        for x in range(cols):
            grid_mosquitos[y][x] *= (1 - (death_factor / 100))
            grid_mosquitos[y][x] = max(0, grid_mosquitos[y][x])

# Main loop
running = True
clock = pygame.time.Clock()

# Initialize some starting values
grid_mosquitos[20][20] = 500
grid_values[20][20] = 1

while running:
    try:
        screen.fill((0, 0, 0))
        draw_grid_mosquitos()
        move_grid_mosquitos()
        reproduce_grid_mosquitos()
        kill_grid_mosquitos()

        # Validate the grid
        if not validate_grid(grid_mosquitos):
            raise ValueError("Invalid values detected in grid!")

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    except Exception as e:
        print(f"Error encountered: {e}")
        running = False

pygame.quit()
