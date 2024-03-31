# ImagesComponent.py

from .base_component import Component

class ImagesComponent(Component):
    def __init__(self, images):
        super().__init__()
        self.images = images
        self.current_image = 0

