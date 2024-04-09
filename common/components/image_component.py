# ImageComponent.py
import pygame

from .base_component import Component

class ImageComponent(Component):
    def __init__(self, image_data: list[str] = None):
        super().__init__()
       
        self.images = []
        self.current_index = 0
        self.current_image = None

        if image_data:
            self.path = image_data["path"]
            self.locations = image_data["locations"]
            self.initialize_images()
            # TODO for now
            self.current_image = self.images[self.current_index]

    def initialize_images(self):
        for location in self.locations:
            # Get subsurface of the image based on location (x, y, width, height)
            rect = pygame.Rect(location)
            image = pygame.image.load(self.path).subsurface(rect)
            self.images.append(image)