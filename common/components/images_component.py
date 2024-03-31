# ImagesComponent.py
import pygame

from .base_component import Component

class ImagesComponent(Component):
    def __init__(self, images_locations: list[str]):
        super().__init__()
        self.images_locations = images_locations
        
        self.images = []
        self.current_image = 0

        self.initialize_images()

    def initialize_images(self):
        for location in self.images_locations:
            self.images.append(pygame.image.load(location))
