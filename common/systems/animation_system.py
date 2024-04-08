# Animation System

from .base_system import System

from common.managers.event_manager import Event

from common.components import AnimationComponent
from common.components import ImagesComponent
from common.components import PlayerComponent

class AnimationSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['animation_system']

    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def update(self, delta_time):
        for entity in self.entity_manager.entities_with_animation:
            animation_component = self.entity_manager.get_component(entity, AnimationComponent)
            current_animation = animation_component.current_animation

            if current_animation is None:
                continue

            current_animation.time_since_last_frame += delta_time

            #self.logger.info(f"Current frame: {current_animation.current_frame}, Time since last frame: {current_animation.time_since_last_frame}, Frame duration: {current_animation.frame_duration[current_animation.current_frame]}")

            if current_animation.time_since_last_frame >= current_animation.frame_duration[current_animation.current_frame]:
                current_animation.time_since_last_frame -= current_animation.frame_duration[current_animation.current_frame]
                current_animation.current_frame += 1

                if current_animation.current_frame >= current_animation.num_frames:
                    if current_animation.loop:
                        current_animation.current_frame = 0
                    else:
                        current_animation.is_finished = True
                        self.reset_animation(entity)
                        self.post_event(self.event_manager.PLAYER_ANIMATION_FINISHED, (entity, current_animation))
                        continue

            current_image = current_animation.sprites[current_animation.current_frame]
            self.entity_manager.get_component(entity, ImagesComponent).images = [current_image]

    def reset_animation(self, entity):
        animation_component = self.entity_manager.get_component(entity, AnimationComponent)
        if animation_component.current_animation is not None:
            animation_component.current_animation.current_frame = 0
        animation_component.current_frame = 0
        animation_component.time_since_last_frame = 0
        animation_component.is_finished = False
        animation_component.current_animation = None