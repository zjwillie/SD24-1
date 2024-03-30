from .base_system import System

class PlayerSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

    def update(self, delta_time):
        pass