import pygame
import sys
import json

# Initialize Pygame
pygame.init()

JSON_to_load = "entities/buildings/home.json"

# Load the JSON file
with open(JSON_to_load, 'r') as f:
    data = json.load(f)

# Load and scale the background image
background = pygame.image.load(data['ImageComponent']['image_data']['path'])
background = pygame.transform.scale(background, (background.get_width() * 10, background.get_height() * 10))

# Set up some constants
WIDTH, HEIGHT = background.get_size()  # Window size

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# List to store the points
points = []

def draw_points():
    for point in points:
        pygame.draw.circle(window, (255, 255, 255), (point["x"]*10 + 5, point["y"]*10 + 5), 3)

def add_point(x, y):
    points.append({"x": x//10, "y": y//10})

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
        pygame.draw.polygon(window, (255, 0, 0), [(point["x"]*10 + 5, point["y"]*10 + 5) for point in polygon], 1)

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

    window.blit(background, (0, 0))
    draw_points()
    draw_polygons()
    pygame.display.flip()