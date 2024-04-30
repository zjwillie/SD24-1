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

def convert_text_to_surface(font, text, width, height):
    """
    Convert a text string into a surface with the text rendered in the font
    :param font: The font component to use for rendering the text
    :param text: The text string to render
    :param width: The width of the surface to render the text on
    :param height: The height of the surface to render the text on
    :return: A surface with the text rendered in the font
    """

    # split the words into a list list of words
    words = text.split(" ")
    lines = []
    current_line = ""
    current_line_width = 0

    # add words until adding one would make its width is longer than the width of the box
    # so we need to get a word, then check if the current length plus the new word length fits, if it does, add it
    # if it does not finish the line
    # if there are still more words, start a new current line if the sum of all the heights of the lines in lines is
    # less than the height of the box

    for word in words:
        current_word_width = 0  # Start with the width of 0
        for letter in word:
            if letter in font.character_list:
                current_word_width += font.characters[letter].width + font.spacing  # Add the width of the letter and the spacing
            else:
                print(f"Character {letter} not found in font character list")
                continue  # Skip the letter if it's not in the character list
    
        # Check if adding the word would fit in the current box
        if (current_line_width + current_word_width + font.space_width) <= width:
            current_line += word
            current_line_width += current_word_width
            if word != words[-1]:  # If the word is not the last one in the line
                current_line += " "
                current_line_width += font.space_width  # Add the width of the space character here
        # If not append the line, add the word to the new current_line
        else:
            lines.append(current_line.strip())  # Remove trailing space from the line
            current_line = word
            current_line_width = current_word_width
            if word != words[-1]:  # If the word is not the last one in the line
                current_line += " "
                current_line_width += font.space_width  # Add the width of the space character here
    
    lines.append(current_line.strip())  # Remove trailing space from the last line

    for i in range(0, len(lines), height // font.line_height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
        surface.fill((0, 0, 0, 0))  # Fill the surface with a transparent color

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
                    
    # Get the bounding rectangle of the non-transparent area
    bounding_rect = surface.get_bounding_rect()

    # Create a new surface that represents the non-transparent area of the original surface
    trimmed_surface = surface.subsurface(bounding_rect)

    return trimmed_surface

def convert_text_to_surfaces(font, text, width, height):
    # split the words into a list list of words
    words = text.split(" ")
    lines = []
    current_line = ""
    current_line_width = 0

    # add words until adding one would make its width is longer than the width of the box
    # so we need to get a word, then check if the current length plus the new word length fits, if it does, add it
    # if it does not finish the line
    # if there are still more words, start a new current line if the sum of all the heights of the lines in lines is
    # less than the height of the box

    for word in words:
        current_word_width = 0  # Start with the width of 0
        for letter in word:
            if letter in font.character_list:
                current_word_width += font.characters[letter].width + font.spacing  # Add the width of the letter and the spacing
            else:
                print(f"Character {letter} not found in font character list")
                continue  # Skip the letter if it's not in the character list
    
        # Check if adding the word would fit in the current box
        if (current_line_width + current_word_width + font.space_width) <= width:
            current_line += word
            current_line_width += current_word_width
            if word != words[-1]:  # If the word is not the last one in the line
                current_line += " "
                current_line_width += font.space_width  # Add the width of the space character here
        # If not append the line, add the word to the new current_line
        else:
            lines.append(current_line.strip())  # Remove trailing space from the line
            current_line = word
            current_line_width = current_word_width
            if word != words[-1]:  # If the word is not the last one in the line
                current_line += " "
                current_line_width += font.space_width  # Add the width of the space character here
    
    lines.append(current_line.strip())  # Remove trailing space from the last line

    surfaces = []
    for i in range(0, len(lines), height // font.line_height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
        surface.fill((0, 0, 0, 0))  # Fill the surface with a transparent color

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

def create_text_box_surface(border, width, height):
    # Create a new surface
    surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
    surface.fill((0, 0, 0, 0))  # Fill the surface with a transparent color

    # Calculate the number of full tiles and the remainder for width and height
    full_tiles_width = (width - 2 * border.width) // border.width
    remainder_width = (width - 2 * border.width) % border.width
    full_tiles_height = (height - 2 * border.height) // border.height
    remainder_height = (height - 2 * border.height) % border.height

    # Draw the top-left corner
    surface.blit(border.border[0], (0, 0))
    # Draw the top border
    for i in range(full_tiles_width):
        surface.blit(border.border[1], (border.width + i * border.width, 0))
    # Draw the remainder of the top border
    if remainder_width > 0:
        subsurface = border.border[1].subsurface(pygame.Rect(0, 0, remainder_width, border.height))
        surface.blit(subsurface, (border.width + full_tiles_width * border.width, 0))
    # Draw the top-right corner
    surface.blit(border.border[2], (width - border.width, 0))

    # Draw the middle part of the border
    for i in range(full_tiles_height):
        # Draw the left border
        surface.blit(border.border[3], (0, border.height + i * border.height))
        # Draw the middle tiles
        for j in range(full_tiles_width):
            surface.blit(border.border[4], (border.width + j * border.width, border.height + i * border.height))
        # Draw the right border
        surface.blit(border.border[5], (width - border.width, border.height + i * border.height))
    # Draw the remainder of the middle part
    if remainder_width > 0:
        for i in range(full_tiles_height):
            subsurface = border.border[4].subsurface(pygame.Rect(0, 0, remainder_width, border.height))
            surface.blit(subsurface, (border.width + full_tiles_width * border.width, border.height + i * border.height))
    if remainder_height > 0:
        subsurface_left = border.border[3].subsurface(pygame.Rect(0, 0, border.width, remainder_height))
        surface.blit(subsurface_left, (0, border.height + full_tiles_height * border.height))
        for i in range(full_tiles_width):
            subsurface_middle = border.border[4].subsurface(pygame.Rect(0, 0, border.width, remainder_height))
            surface.blit(subsurface_middle, (border.width + i * border.width, border.height + full_tiles_height * border.height))
        subsurface_right = border.border[5].subsurface(pygame.Rect(0, 0, border.width, remainder_height))
        surface.blit(subsurface_right, (width - border.width, border.height + full_tiles_height * border.height))
    if remainder_width > 0 and remainder_height > 0:
        subsurface = border.border[4].subsurface(pygame.Rect(0, 0, remainder_width, remainder_height))
        surface.blit(subsurface, (border.width + full_tiles_width * border.width, border.height + full_tiles_height * border.height))

    # Draw the bottom-left corner
    surface.blit(border.border[6], (0, height - border.height))
    # Draw the bottom border
    for i in range(full_tiles_width):
        surface.blit(border.border[7], (border.width + i * border.width, height - border.height))
    # Draw the remainder of the bottom border
    if remainder_width > 0:
        subsurface = border.border[7].subsurface(pygame.Rect(0, 0, remainder_width, border.height))
        surface.blit(subsurface, (border.width + full_tiles_width * border.width, height - border.height))
    # Draw the bottom-right corner
    surface.blit(border.border[8], (width - border.width, height - border.height))

    # Return the new surface with the border
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
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    BACKGROUND_IMAGE = create_surface("images/unsorted/scene_meeting_ancient_advisor.png")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a FontComponent
    #font = FontComponent("entities/textbox/test_font.json")
    #font = FontComponent("entities/textbox/test_font_16x16.json")
    font = FontComponent("entities/textbox/test_font_16x16_outline.json")
    border = BorderComponent("entities/textbox/test_border.json")

    #test_font(screen, font, SAMPLE_TEXT, SCREEN_WIDTH)

    x = 100
    y = 100
    surface_width = 600
    surface_height = 200

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