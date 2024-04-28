# BorderComponent.py
import json
import pygame

from .base_component import Component

class BorderComponent(Component):
    def __init__(self, border_json_path):
        super().__init__()
        # Component initialization
        self.height = 0
        self.width = 0
        self.top_thickness = 0
        self.bottom_thickness = 0
        self.left_thickness = 0
        self.right_thickness = 0
        self.border = []

        with open(border_json_path, "r") as border_file:
            border_dict = json.load(border_file)

        self.load_border(border_dict)

    def load_border(self, border_dict):
        self.height = border_dict["height"]
        self.width = border_dict["width"]
        self.top_thickness = border_dict["top_thickness"]
        self.bottom_thickness = border_dict["bottom_thickness"]
        self.left_thickness = border_dict["left_thickness"]
        self.right_thickness = border_dict["right_thickness"]

        self.borders = []

        self.border_sheet = pygame.image.load(border_dict["border_sheet_location"]).convert_alpha()

        for row in range(3):
            for col in range(3):
                sprite = self.border_sheet.subsurface((col * self.width, row * self.height, self.width, self.height))
                self.border.append(sprite)




