# FontComponent.py
import json
import pygame

from .base_component import Component

class Letter:
    def __init__(self, sprite, width, height):
        self.sprite = sprite
        self.width = width
        self.height = height

class FontComponent(Component):
    def __init__(self, font_json_path):
        super().__init__()
        # Component initialization
        self.characters = {}
        self.width = 0
        self.height = 0
        self.space_width = 0
        self.line_height = 0
        self.font_sheet = None

        # Load dict from json
        with open(font_json_path, "r") as font_file:
            font_dict = json.load(font_file)
        
        self.load_font(font_dict)

    def load_font(self, font_dict):
        # Load font from JSON file
        self.width = font_dict["width"]
        self.height = font_dict["height"]
        self.space_width = font_dict["space_width"]
        self.spacing = font_dict["spacing"]
        self.line_height = font_dict["line_height"]

        self.character_map = font_dict["character_map"]
        self.character_list = ""
        self.characters = {}

        self.font_sheet = pygame.image.load(font_dict["font_sheet_location"]).convert_alpha()
    
        for character_lines in self.character_map:
            self.character_list += character_lines

        for i, map in enumerate(self.character_map):
            for j, char in enumerate(map):
                x = j * self.width
                y = i * self.height
                sprite = self.font_sheet.subsurface((x, y, self.width, self.height))
                new_sprite, new_width = self.trim_sprite(sprite)
                self.characters[char] = Letter(new_sprite, new_width, self.height)

    def trim_sprite(self, sprite):
        # Get the bounding box of the non-transparent area of the sprite
        bounding_rect = sprite.get_bounding_rect()
    
        # Create a new surface with the width of the bounding box and the original height
        trimmed_sprite = pygame.Surface((bounding_rect.width, self.height), pygame.SRCALPHA)
    
        # Blit the non-transparent area of the original sprite onto the new surface
        trimmed_sprite.blit(sprite, (0, 0), pygame.Rect(bounding_rect.left, 0, bounding_rect.width, self.height))
    
        # Return the trimmed sprite and its dimensions
        return trimmed_sprite, bounding_rect.width