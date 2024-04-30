import os
import pygame

from common.components.border_component import BorderComponent
from common.components.font_component import FontComponent
        
def test_font(screen, font, SAMPLE_TEXT, SCREEN_WIDTH):
    # Display the entire sprite sheet
    screen.blit(font.font_sheet, (0, 0))
    pygame.display.flip()

    # Display each individual character
    x, y = 0, 100
    for char, letter in font.characters.items():
        screen.blit(letter.sprite, (x, y))
        x += letter.width
        if x > SCREEN_WIDTH:
            x = 0
            y += font.height
    pygame.display.flip()

    # Calculate the maximum height of all characters
    max_height = max(letter.height for letter in font.characters.values())

    # Display a sample text
    x, y = 0, 200
    for char in SAMPLE_TEXT:
        if char in font.characters:
            letter = font.characters[char]
            # Check if the character will fit on the current line
            if x + letter.width > SCREEN_WIDTH:
                x = 0
                y += font.height
            screen.blit(letter.sprite, (x, y))
            x += letter.width
        elif char == " ":
            x += font.width / 2
            # Check if the space will fit on the current line
            if x > SCREEN_WIDTH:
                x = 0
                y += font.height
        elif char == "\n":
            x = 0
            y += font.height
    pygame.display.flip()

def save_surfaces(surfaces, save_path):
    if isinstance(surfaces, pygame.Surface):
        # If a single surface is provided, save it
        pygame.image.save(surfaces, os.path.join(save_path, 'surface.png'))
    else:
        # If a list of surfaces is provided, save each one
        for i, surface in enumerate(surfaces):
            pygame.image.save(surface, os.path.join(save_path, f'surface_{i}.png'))

def split_text_into_lines(font, text, width):
    words = text.split(" ")
    lines = []
    current_line = ""
    current_line_width = 0

    for word in words:
        current_word_width = 0
        for letter in word:
            if letter in font.character_list:
                current_word_width += font.characters[letter].width + font.spacing
            else:
                print(f"Character {letter} not found in font character list")
                continue

        if (current_line_width + current_word_width + font.space_width) <= width:
            current_line += word
            current_line_width += current_word_width
            if word != words[-1]:
                current_line += " "
                current_line_width += font.space_width
        else:
            lines.append(current_line.strip())
            current_line = word
            current_line_width = current_word_width
            if word != words[-1]:
                current_line += " "
                current_line_width += font.space_width

    lines.append(current_line.strip())
    return lines

def convert_text_to_surface(font, text, width, height):
    lines = split_text_into_lines(font, text, width)

    for i in range(0, len(lines), height // font.line_height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        x_offset = 0
        y_offset = 0
        for line in lines[i:i + height // font.line_height]:
            for letter in line:
                if letter in font.character_list:
                    char = font.characters[letter]
                    surface.blit(char.sprite, (x_offset, y_offset))
                    x_offset += char.width + font.spacing
                elif letter == " ":
                    x_offset += font.space_width
                elif letter == "\n":
                    x_offset = 0
                    y_offset += font.line_height
            y_offset += font.line_height
            x_offset = 0

    bounding_rect = surface.get_bounding_rect()
    trimmed_surface = surface.subsurface(bounding_rect)

    return trimmed_surface

def convert_text_to_surfaces(font, text, width, height):
    lines = split_text_into_lines(font, text, width)

    surfaces = []
    for i in range(0, len(lines), height // font.line_height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        x_offset = 0
        y_offset = 0
        for line in lines[i:i + height // font.line_height]:
            for letter in line:
                if letter in font.character_list:
                    char = font.characters[letter]
                    surface.blit(char.sprite, (x_offset, y_offset))
                    x_offset += char.width + font.spacing
                elif letter == " ":
                    x_offset += font.space_width
                elif letter == "\n":
                    x_offset = 0
                    y_offset += font.line_height
            y_offset += font.line_height
            x_offset = 0

        surfaces.append(surface)
    return surfaces

def blit_subsurface(surface, border, index, position, size=None):
    if size is not None:
        subsurface = border.border[index].subsurface(pygame.Rect(0, 0, *size))
        surface.blit(subsurface, position)
    else:
        surface.blit(border.border[index], position)

def create_text_box_surface(border, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    full_tiles_width = (width - 2 * border.width) // border.width
    remainder_width = (width - 2 * border.width) % border.width
    full_tiles_height = (height - 2 * border.height) // border.height
    remainder_height = (height - 2 * border.height) % border.height

    # Draw the corners
    blit_subsurface(surface, border, 0, (0, 0))
    blit_subsurface(surface, border, 2, (width - border.width, 0))
    blit_subsurface(surface, border, 6, (0, height - border.height))
    blit_subsurface(surface, border, 8, (width - border.width, height - border.height))

    # Draw the borders
    for i in range(full_tiles_width):
        blit_subsurface(surface, border, 1, (border.width + i * border.width, 0))
        blit_subsurface(surface, border, 7, (border.width + i * border.width, height - border.height))
    for i in range(full_tiles_height):
        blit_subsurface(surface, border, 3, (0, border.height + i * border.height))
        blit_subsurface(surface, border, 5, (width - border.width, border.height + i * border.height))

    # Draw the remainder of the borders
    if remainder_width > 0:
        blit_subsurface(surface, border, 1, (border.width + full_tiles_width * border.width, 0), (remainder_width, border.height))
        blit_subsurface(surface, border, 7, (border.width + full_tiles_width * border.width, height - border.height), (remainder_width, border.height))
    if remainder_height > 0:
        blit_subsurface(surface, border, 3, (0, border.height + full_tiles_height * border.height), (border.width, remainder_height))
        blit_subsurface(surface, border, 5, (width - border.width, border.height + full_tiles_height * border.height), (border.width, remainder_height))

    # Draw the middle part of the border
    for i in range(full_tiles_height):
        for j in range(full_tiles_width):
            blit_subsurface(surface, border, 4, (border.width + j * border.width, border.height + i * border.height))
    if remainder_width > 0:
        for i in range(full_tiles_height):
            blit_subsurface(surface, border, 4, (border.width + full_tiles_width * border.width, border.height + i * border.height), (remainder_width, border.height))
    if remainder_height > 0:
        for i in range(full_tiles_width):
            blit_subsurface(surface, border, 4, (border.width + i * border.width, border.height + full_tiles_height * border.height), (border.width, remainder_height))
    if remainder_width > 0 and remainder_height > 0:
        blit_subsurface(surface, border, 4, (border.width + full_tiles_width * border.width, border.height + full_tiles_height * border.height), (remainder_width, remainder_height))

    return surface

def create_arrow_surface(border):
    surface = pygame.Surface((border.arrow_width, border.arrow_height * 3), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
    surface.fill((0, 0, 0, 0))  # Fill the surface with a transparent color

    # Draw the arrow in the center of the surface
    up_arrow = border.arrows[0]
    down_arrow = border.arrows[1]

    x = 0 
    y = 0
    
    surface.blit(up_arrow, (x, y))

    y += border.arrow_height

    surface.blit(down_arrow, (x, border.arrow_height * 2))

    # Return the new surface with the arrow
    return surface

def create_surface(image_location):
    return pygame.image.load(image_location).convert_alpha()


def main():
    # Initialize Pygame
    pygame.init()

    # Set up some constants
    SAMPLE_TEXT = "Only through meditation do enternitie's creep not lead to madness. Long I have awaited your arrival, someone must come. Yes, yes. Enigma."
    SAMPLE_RESPONSES = ["1. Yes", "2. No", "3. Maybeazy dog. 1234567890 times! Isn't that amazing? Yes, it is. But, what's next? Well, let's see: []{}()", "4. Hi dog"]


    # strip the text of leading and trailing whitespace
    SAMPLE_TEXT = '\n'.join(line.strip() for line in SAMPLE_TEXT.split('\n'))
    SAMPLE_TEXT = SAMPLE_TEXT.replace("\n", " ")

    # strip the text of leading and trailing whitespace
    for test in SAMPLE_RESPONSES:
        test = '\n'.join(line.strip() for line in SAMPLE_TEXT.split('\n'))
        test = SAMPLE_TEXT.replace("\n", " ")  

    # Create a screen
    """
    infoObject = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h
    """
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)

    BACKGROUND_IMAGE = create_surface("images/unsorted/scene_meeting_ancient_advisor.png")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a FontComponent
    #font = FontComponent("entities/textbox/test_font.json")
    #font = FontComponent("entities/textbox/test_font_16x16.json")
    font = FontComponent("entities/textbox/test_font_16x16_outline.json")
    border = BorderComponent("entities/textbox/test_border.json")

    #test_font(screen, font, SAMPLE_TEXT, SCREEN_WIDTH)

    x = 160
    y = 350
    surface_width = 400
    surface_height = 80

    # Calculate the width and height of the text area based on the border
    text_area_width = surface_width - border.left_thickness - border.right_thickness
    text_area_height = surface_height - border.top_thickness - border.bottom_thickness

    # index to track the current text surface
    current_surface_index = 0

    border_image = create_text_box_surface(border, surface_width, surface_height)
    surfaces = convert_text_to_surfaces(font, SAMPLE_TEXT, text_area_width, text_area_height)
   
    save_path = "images/textbox/surfaces"
    save_surfaces(surfaces, save_path)

    # Create the response surfaces
    response_surface_width = 600
    response_surface_height = 100

    response_surfaces = []
    for response in SAMPLE_RESPONSES:
        response_surfaces.append(convert_text_to_surface(font, response, response_surface_width, response_surface_height))


    # Wait until the user closes the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_surface_index = (current_surface_index - 1) % len(surfaces)
                elif event.key == pygame.K_DOWN:
                    current_surface_index = (current_surface_index + 1) % len(surfaces)

        screen.fill((0, 0, 0))  # Clear the screen
        #pygame.draw.rect(screen, (0, 55, 55), (x-1, y-1, width+2, height+2), 0)  # Draw the box

        screen.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the background image

        screen.blit(border_image, (x - border.left_thickness, y - border.top_thickness))  # Draw the border)
        screen.blit(surfaces[current_surface_index], (x, y))  # Draw the current surface

        y_offset = 0
        for i in range(len(response_surfaces)):
            screen.blit(response_surfaces[i], (x, y + surface_height + y_offset))
            y_offset += response_surfaces[i].get_height()


        pygame.display.flip()  # Update the display

if __name__ == "__main__":
    main()