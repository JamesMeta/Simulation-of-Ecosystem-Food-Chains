import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Dimensional Random Walk")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Constants
STEP_SIZE = 10
INITIAL_POSITION = [WIDTH // 2, HEIGHT // 2]
MAX_STEPS = 1000

# Function to perform a random step
def random_step():
    return random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)]) * STEP_SIZE

# Main function
def main():
    position = list(INITIAL_POSITION)
    steps = 0

    # Main loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Perform a random step
        step = random_step()
        position[0] += step[0]
        position[1] += step[1]

        # Draw
        screen.fill(WHITE)
        pygame.draw.circle(screen, BLACK, position, 5)
        pygame.display.flip()

        # Limit to 60 frames per second
        pygame.time.Clock().tick(60)

        # Check if maximum steps reached
        steps += 1
        if steps >= MAX_STEPS:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
