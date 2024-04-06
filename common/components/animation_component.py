# AnimationComponent.py
import pygame

from .base_component import Component

class Animation:
    def __init__(self, width, height, animation_data, sprite_sheet):
        self.width = width
        self.height = height
        self.row = animation_data["row"]
        self.num_frames = animation_data["num_frames"]
        self.loop = animation_data["loop"]
        self.sprite_sheet = sprite_sheet
        self.frame_duration = animation_data["frame_duration"]

        self.sprites = self.load_sprites()

        self.is_finished = False
        self.current_frame = 0
        self.time_since_last_frame = 0

    def load_sprites(self):
        sprites = []
        for i in range(self.num_frames):
            x = i * self.width
            y = self.row * self.height
            sprite = self.sprite_sheet.subsurface((x, y, self.width, self.height))
            sprites.append(sprite)
        return sprites

class AnimationComponent(Component):
    def __init__(self, animation_data: dict):
        super().__init__()
        self.sprite_sheet_location = animation_data["sprite_sheet_location"]
        self.sprite_sheet = pygame.image.load(self.sprite_sheet_location).convert_alpha()
        self.current_animation = None

        self.width = animation_data["frame_width"]
        self.height = animation_data["frame_height"]
        
        self.animations = self.initialize_animations(animation_data)

    def initialize_animations(self, animation_data: dict):
        animations = {}
        for name, data in animation_data['animations'].items():
            animations[name] = Animation(self.width, self.height, data, self.sprite_sheet)
        return animations
