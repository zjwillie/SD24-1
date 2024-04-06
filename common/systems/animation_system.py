# Animation System

from .base_system import System

from common.components import AnimationComponent
from common.components import ImagesComponent

class AnimationSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['animation_system']

    def update(self, delta_time):
        for entity in self.entity_manager.entities_with_animation:
            animation_component = self.entity_manager.get_component(entity, AnimationComponent)
            current_animation = animation_component.current_animation

            if current_animation is None:
                continue

            current_animation.time_since_last_frame += delta_time

            self.logger.info(f"Current frame: {current_animation.current_frame}, Time since last frame: {current_animation.time_since_last_frame}, Frame duration: {current_animation.frame_duration[current_animation.current_frame]}")

            if current_animation.time_since_last_frame >= current_animation.frame_duration[current_animation.current_frame]:
                current_animation.time_since_last_frame -= current_animation.frame_duration[current_animation.current_frame]
                current_animation.current_frame += 1

                if current_animation.current_frame >= current_animation.num_frames:
                    if current_animation.loop:
                        current_animation.current_frame = 0
                    else:
                        current_animation.is_finished = True
                        current_animation.current_frame = current_animation.num_frames - 1
                        continue

            self.logger.info(f"Current frame: {current_animation.current_frame}, Time since last frame: {current_animation.time_since_last_frame}, Frame duration: {current_animation.frame_duration[current_animation.current_frame]}")
            current_image = current_animation.sprites[current_animation.current_frame]
            self.entity_manager.get_component(entity, ImagesComponent).images = [current_image]