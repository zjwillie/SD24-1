import pygame
import json

class Letter:
    def __init__(self, sprite, width):
        self.sprite = sprite
        self.width = width

class FontComponent:
    def __init__(self, font_dict):
        self.width = font_dict["width"]
        self.height = font_dict["height"]
        self.character_map = font_dict["character_map"]
        font_sheet = pygame.image.load(font_dict["font_sheet_location"]).convert_alpha()
        self.characters = {}
        for i, map in enumerate(self.character_map):
            for j, char in enumerate(map):
                x = j * self.width
                y = i * self.height
                sprite = font_sheet.subsurface((x, y, self.width, self.height))
                new_sprite, new_width = self.trim_sprite(sprite)
                self.characters[char] = Letter(new_sprite, new_width)

    def trim_sprite(self, sprite):
        bounding_rect = sprite.get_bounding_rect()
        trimmed_sprite = pygame.Surface((bounding_rect.width, self.height), pygame.SRCALPHA)
        trimmed_sprite.blit(sprite, (0, 0), pygame.Rect(bounding_rect.left, 0, bounding_rect.width, self.height))
        return trimmed_sprite, bounding_rect.width

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    with open('entities/text/test_font.json') as f:
        font_dict = json.load(f)

    font_component = FontComponent(font_dict)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        x = 0
        y = 0
        for i, (char, letter) in enumerate(font_component.characters.items()):
            screen.blit(letter.sprite, (x, y))
            x += letter.width + 5
            if (i + 1) % 10 == 0:
                x = 0
                y += font_component.height + 5
            if y + font_component.height > screen.get_height():
                break

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()