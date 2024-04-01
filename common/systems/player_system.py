from .base_system import System

class PlayerSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['player_system']

    def test_up(self, event):
        self.logger.info("Up Event Received")

    def update(self, delta_time):
        pass