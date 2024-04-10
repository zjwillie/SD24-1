import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800  # Window size
GRID_SIZE = 100  # Size of the grid (in squares)
SQUARE_SIZE = WIDTH // GRID_SIZE  # Size of a square (in pixels)

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# List to store the points
points = []

def draw_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(window, (255, 255, 255), rect, 1)

def draw_points():
    for point in points:
        rect = pygame.Rect(point["x"]*SQUARE_SIZE, point["y"]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(window, (255, 0, 0), rect)

def add_point(x, y):
    points.append({"x": x, "y": y})

def print_points():
    print("            [")
    for point in points:
        print(f"                {{\"x\": {point['x']}, \"y\": {point['y']}}},")
    print("            ],")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            add_point(x // SQUARE_SIZE, y // SQUARE_SIZE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print_points()

    window.fill((0, 0, 0))
    draw_grid()
    draw_points()
    pygame.display.flip()