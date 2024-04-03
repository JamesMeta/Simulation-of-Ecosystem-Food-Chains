import pygame
import random

# Constants
GRID_SIZE = 20  # Size of each grid cell
GRID_WIDTH = 30  # Number of grid cells in width
GRID_HEIGHT = 20  # Number of grid cells in height
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Function to draw a grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

# Main function for the self-avoiding random walk
def self_avoiding_random_walk():
    # Start position of the particle
    x, y = GRID_WIDTH // 2, GRID_HEIGHT // 2
    visited = set()  # Set to store visited positions
    visited.add((x, y))
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get available directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        # Move the particle
        moved = False
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT
                    and (new_x, new_y) not in visited):
                x, y = new_x, new_y
                visited.add((x, y))
                moved = True
                break

        # Draw the particle
        screen.fill(BLACK)
        draw_grid()
        pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()
        clock.tick(10)  # Adjust speed

        # Check if stuck (no available moves)
        if not moved: 
            print("Stuck!")
            visited = set()  # Reset visited set

    pygame.quit()

# Run the self-avoiding random walk
self_avoiding_random_walk()
