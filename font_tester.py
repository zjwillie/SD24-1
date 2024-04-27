import pygame
from common.components.font_component import FontComponent

def convert_text_to_surfaces(screen, font, text, width, height):
    # split the words into a list list of words
    words = text.split(" ")
    lines = []
    current_line = ""
    current_line_width = 0
    current_lines_height = 0
    # add words until adding one would make its width is longer than the width of the box
    # so we need to get a word, then check if the current length plus the new word length fits, if it does, add it
    # if it does not finish the line
    # if there are still more words, start a new current line if the sum of all the heights of the lines in lines is
    # less than the height of the box

    for word in words:
        current_word_width = 0
        for letter in word:
            if letter in font.character_list:
                current_word_width += font.characters[letter].width
            else:
                print(f"Character {letter} not found in font character list")
                continue  # Skip the letter if it's not in the character list
    
        # Check if adding the word would fit in the current box
        if (current_line_width + current_word_width + font.space_width) <= width:
            current_line += word + " "
            current_line_width += current_word_width + font.space_width
        # If not append the line, add the word to the new current_line
        else:
            lines.append(current_line.strip())  # Remove trailing space from the line
            current_line = word + " "
            current_line_width = current_word_width + font.space_width
    
    lines.append(current_line.strip())  # Remove trailing space from the last line

    surfaces = []
    for i in range(0, len(lines), height // font.line_height):
        surface = pygame.Surface((width, height))

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


def main():
    # Initialize Pygame
    pygame.init()

    # Set up some constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SAMPLE_TEXT = """
one two three four five six seven eight nine ten
eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty
twenty-one twenty-two twenty-three twenty-four twenty-five twenty-six twenty-seven twenty-eight twenty-nine thirty
thirty-one thirty-two thirty-three thirty-four thirty-five thirty-six thirty-seven thirty-eight thirty-nine forty
forty-one forty-two forty-three forty-four forty-five forty-six forty-seven forty-eight forty-nine fifty
fifty-one fifty-two fifty-three fifty-four fifty-five fifty-six fifty-seven fifty-eight fifty-nine sixty
sixty-one sixty-two sixty-three sixty-four sixty-five sixty-six sixty-seven sixty-eight sixty-nine seventy
seventy-one seventy-two seventy-three seventy-four seventy-five seventy-six seventy-seven seventy-eight seventy-nine eighty
eighty-one eighty-two eighty-three eighty-four eighty-five eighty-six eighty-seven eighty-eight eighty-nine ninety
ninety-one ninety-two ninety-three ninety-four ninety-five ninety-six ninety-seven ninety-eight ninety-nine one hundred
"""

    # strip the text of leading and trailing whitespace
    SAMPLE_TEXT = '\n'.join(line.strip() for line in SAMPLE_TEXT.split('\n'))
    SAMPLE_TEXT = SAMPLE_TEXT.replace("\n", " ")  

    # Create a screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a FontComponent
    font = FontComponent("entities/textbox/test_font.json")

    #test_font(screen, font, SAMPLE_TEXT, SCREEN_WIDTH)

    x = 100
    y = 100
    surfaces = convert_text_to_surfaces(screen, font, SAMPLE_TEXT, 600, 200)
    current_surface_index = 0

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
        screen.blit(surfaces[current_surface_index], (x, y))  # Draw the current surface
        pygame.display.flip()  # Update the display

if __name__ == "__main__":
    main()