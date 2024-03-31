from .base_system import System

class RenderSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['render_system']

        self.screen = game_state.screen

    def update(self, delta_time):
        pass