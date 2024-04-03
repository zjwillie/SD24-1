from .base_system import System

class PlayerSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger
        self.logger.change_log_level('player_system', "INFO")

        self.event_manager.subscribe(self.event_manager.KEYS_DOWN_UPDATE, self.handle_key_down)

        self.keys_down = {}

    def handle_key_down(self, event):
        self.logger.loggers['player_system'].info(f"Key Down Event Received: {event.data} -> {list(event.data.keys())}")
        self.keys_down = event.data

    def test_up(self, event):
        self.logger.info("Up Event Received")

    def update(self, delta_time):
        self.logger.loggers['player_system'].info(f"Keys that are down: {self.keys_down}")