# Animation System

from .base_system import System

from common.components import AnimationComponent

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

            if current_animation.time_since_last_frame >= current_animation.frame_duration:
                current_animation.time_since_last_frame = 0
                current_animation.current_frame += 1

                if current_animation.current_frame >= current_animation.num_frames:
                    if current_animation.loop:
                        current_animation.current_frame = 0
                    else:
                        current_animation.is_finished = True
                        continue

            current_animation.time_since_last_frame = 0

            animation_component.current_animation = current_animation

            self.entity_manager.add_component(entity, animation_component)