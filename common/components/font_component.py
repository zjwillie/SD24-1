# FontComponent.py
import pygame

from .base_component import Component

class FontComponent(Component):
    def __init__(self, font_dict):
        super().__init__()
        # Component initialization
        self.characters = {}
        self.width = 0
        self.height = 0

        self.load_font(font_dict)

    def load_font(self, font_dict):
        # Load font from JSON file
        self.width = font_dict["width"]
        self.height = font_dict["height"]
        self.character_map = font_dict["character_map"]
        font_sheet = pygame.image.load(font_dict["font_sheet_location"]).convert_alpha()

        sprites = []
        for i, map in enumerate(self.character_map):
            for j, char in enumerate(map):
                x = j * self.width
                y = i * self.height
                sprite = font_sheet.subsurface((x, y, self.width, self.height))
                new_sprite = self.trim_sprite(sprite)
                self.characters[char] = new_sprite

    def trim_sprite(self, sprite):
        # Trim sides of sprite to remove any whitespace
        

