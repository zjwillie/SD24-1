import pygame
import sys
import json

# Initialize Pygame
pygame.init()

JSON_to_load = "entities/buildings/home.json"

# Set up the scale factor
SCALE_FACTOR = 4

# Load the JSON file
with open(JSON_to_load, 'r') as f:
    data = json.load(f)

# Load and scale the background image
background = pygame.image.load(data['ImageComponent']['image_data']['path'])
background = pygame.transform.scale(background, (background.get_width() * SCALE_FACTOR, background.get_height() * SCALE_FACTOR))

# Set up some constants
WIDTH, HEIGHT = background.get_size()  # Window size

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# List to store the points
points = []

def draw_points():
    for point in points:
        pygame.draw.circle(window, (255, 255, 255), (point["x"]*SCALE_FACTOR + SCALE_FACTOR//2, point["y"]*SCALE_FACTOR + SCALE_FACTOR//2), 3)

def add_point(x, y):
    grid_x = x // SCALE_FACTOR
    grid_y = y // SCALE_FACTOR
    points.append({"x": grid_x, "y": grid_y})

def orientation(p, q, r):
    val = (q['y'] - p['y']) * (r['x'] - q['x']) - (q['x'] - p['x']) * (r['y'] - q['y'])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def convex_hull(points):
    n = len(points)
    if n < 3:
        return
    l = min(range(n), key = lambda i: (points[i]['y'], points[i]['x']))
    p = l
    q = None
    hull = []
    while True:
        hull.append(points[p])
        q = (p + 1) % n
        for r in range(n):
            if orientation(points[p], points[q], points[r]) == 2:
                q = r
        p = q
        if p == l:
            break
    return hull

def print_points():
    new_polygon = convex_hull(points)
    if new_polygon:
        data['CollisionComponent']['polygons'].append(new_polygon)
        with open(JSON_to_load, 'w') as f:
            json.dump(data, f, indent=4)
    points.clear()

# Draw the existing polygons
def draw_polygons():
    for polygon in data['CollisionComponent']['polygons']:
        pygame.draw.polygon(window, (255, 0, 0), [(point["x"]*SCALE_FACTOR + SCALE_FACTOR//2, point["y"]*SCALE_FACTOR + SCALE_FACTOR//2) for point in polygon], 1)

# Draw a grid
def draw_grid():
    for x in range(0, WIDTH, SCALE_FACTOR):
        pygame.draw.line(window, (211, 211, 211), (x, 0), (x, HEIGHT))  # Light gray color
    for y in range(0, HEIGHT, SCALE_FACTOR):
        pygame.draw.line(window, (211, 211, 211), (0, y), (WIDTH, y))  # Light gray color

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            add_point(x, y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print_points()
            elif event.key == pygame.K_ESCAPE:  # Clear points when escape key is pressed
                points.clear()

    window.blit(background, (0, 0))
    draw_grid()  # Draw the grid
    draw_points()
    draw_polygons()
    pygame.display.flip()