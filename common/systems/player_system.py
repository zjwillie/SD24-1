from .base_system import System

class PlayerSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['player_system']

        self.keys_down = {}

        self.event_manager.subscribe(self.event_manager.KEYS_DOWN_UPDATE, self.handle_key_down)

        self.event_manager.subscribe(self.event_manager.KEY_DOWN, self.handle_key_down)

    def handle_key_down(self, event):
        self.logger.info(f"Key Down Event Received: {event.data} -> {list(event.data.keys())}")
        self.keys_down = event.data

    def test_up(self, event):
        self.logger.info("Up Event Received")

    def update(self, delta_time):
        #self.logger.info(f"Keys that are down: {self.keys_down}")
        pass