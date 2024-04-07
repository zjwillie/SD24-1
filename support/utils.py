import json
import math
import os
import pygame
import sys

from PIL import Image

def get_JSON_data(JSON = None):
    if JSON:
        data = None
        with open(JSON, 'r') as file:
            data = json.load(file)
        return data
    else:
        return None

def scale_surface(surface, scale):
    new_size = (int(surface.get_width() * scale), int(surface.get_height() * scale))
    return pygame.transform.scale(surface, new_size)

def check_game_loop_speed(delta_time):
    frame_rate = delta_time * 1000
    print(f"Frame rate: {frame_rate}")

def crop_sprite_sides(surface):
    rect = surface.get_rect()
    pixels = pygame.PixelArray(surface)

    left = 0
    right = rect.width

    for x in range(rect.width):
        column = pixels[x, :]
        if any(column):
            left = x
            break

    for x in range(rect.width - 1, -1, -1):
        column = pixels[x, :]
        if any(column):
            right = x + 1
            break

    new_width = right - left

    cropped_surface = surface.subsurface(pygame.Rect(left, 0, new_width, rect.height))

    return cropped_surface

def create_semi_circular_hitbox(center_x, center_y, base_radius, facing_direction, segment_count=40):
    hit_points = []

    # Define radius values for the smaller, base, and larger semi-circles
    radii = [base_radius * 0.2, base_radius * 0.4, base_radius * 0.6, base_radius * 0.7, base_radius * 0.8, base_radius * 0.9, base_radius]

    # Define the angle range based on the facing direction
    if facing_direction == "right":
        start_angle, end_angle = -90, 90
    elif facing_direction == "left":
        start_angle, end_angle = 90, 270
    elif facing_direction == "down":
        start_angle, end_angle = 0, 180
    elif facing_direction == "up":
        start_angle, end_angle = 180, 360

    # Generate points for each radius
    for radius in radii:
        for i in range(segment_count):
            angle = start_angle + (end_angle - start_angle) * i / (segment_count - 1)
            rad = math.radians(angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            hit_points.append((x, y))

    return hit_points

def crop_image(input_file_path, output_file_path, area):
    # Open the input image
    with Image.open(input_file_path) as img:
        # Crop the image using the specified area
        cropped_img = img.crop(area)
        # Save the cropped image to the output file path
        cropped_img.save(output_file_path, "PNG")

def convert_and_crop_aseprite(input_json_path):
    # Read the input JSON from the specified file path
    with open(input_json_path, 'r') as file:
        data = json.load(file)

    # Determine the directory and the base image path
    dir_path = os.path.dirname(input_json_path)
    base_image_path = os.path.join(dir_path, data['meta']['image'])

    # Extract frames from the input data
    frames = data['frames']

    # Iterate over frames (which are now dynamic, no fixed naming convention)
    for frame_key, frame_data in frames.items():
        frame = frame_data['frame']
        # The name is now derived from the frame_key to ensure uniqueness
        name = frame_key.split()[0]  # Assuming the first word in the frame key is the layer name
        safe_name = name.replace(" ", "_")  # Create a filesystem-safe name

        # Define the cropped image path
        cropped_image_path = os.path.join(dir_path, f"{safe_name}.png")

        # Crop and save the image based on the frame data
        crop_image(base_image_path, cropped_image_path, (frame['x'], frame['y'], frame['x'] + frame['w'], frame['y'] + frame['h']))

        # Create a new JSON object for this layer
        new_json = {
            "NameComponent": {
                "name": name
            },
            "IDComponent": {
                "id": safe_name.lower()
            },
            "UUIDComponent": {},
            "PositionComponent": {
                "x": 0,
                "y": 0
            },
            "SizeComponent": {
                "width": frame['w'],
                "height": frame['h']
            },
            "HUDComponent": {},
            "ImageComponent": {
                "images": [cropped_image_path]
            },
            "RenderComponent": {
                "layer": 5  # Assuming layer 5 for all, adjust as needed
            }
        }

        # Define the output JSON file path
        output_json_path = os.path.join(dir_path, f"{safe_name}_component.json")

        # Write the new JSON object to a file with the name of the component
        with open(output_json_path, 'w') as outfile:
            json.dump(new_json, outfile, indent=4)

        print(f"Output JSON for {name} written to {output_json_path}")
        print(f"Cropped image for {name} saved as {cropped_image_path}")


def main():

    """
    # Initialize Pygame
    pygame.init()

    # Window settings
    width, height = 400, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Semi-Circular Hitbox Visualization")
    clock = pygame.time.Clock()

    running = True
    facing_direction = "right"  # Can be changed to "up", "down", "left", "right"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill screen with white background
        screen.fill((255, 255, 255))

        # Draw the simplified semi-circular hitbox
        center_x, center_y, radius = 200, 200, 31  # Center of the screen
        hitbox_points = create_semi_circular_hitbox(center_x, center_y, radius, facing_direction)
        for point in hitbox_points:
            pygame.draw.circle(screen, (255, 0, 0), (int(point[0]), int(point[1])), 2)  # Red points

        # Update the display
        pygame.display.flip()
        clock.tick(60)
    """

    convert_and_crop_aseprite("images/sprites/creatures/cats/cat_tuxedo_animation.json")

if __name__ == "__main__":
    main()