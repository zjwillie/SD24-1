from .base_system import System

class PlayerSystem(System):
    ACTION_QUEUE_MAX_SIZE = 5

    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['player_system']

        self.keys_down = {}
        self.action_queue = []

        self.event_manager.subscribe(self.event_manager.KEYS_DOWN_UPDATE, self.handle_keys_down_update)

        self.event_manager.subscribe(self.event_manager.EVENT_UP, self.update_action_queue)
        self.event_manager.subscribe(self.event_manager.EVENT_DOWN, self.update_action_queue)
        self.event_manager.subscribe(self.event_manager.EVENT_LEFT, self.update_action_queue)
        self.event_manager.subscribe(self.event_manager.EVENT_RIGHT, self.update_action_queue)

    def update_action_queue(self, event):
        self.logger.info(f"Key Down Event Received: {event.type, event.data}")
        if event.data[0] == self.event_manager.KEY_DOWN:
            self.action_queue.append((event.type, event.data[1]))

    def handle_keys_down_update(self, event):
        #self.logger.info(f"Key Down Event Received: {event.data} -> {list(event.data.keys())}")
        self.keys_down = event.data

    def test_up(self, event):
        self.logger.info("Up Event Received")

    def update(self, delta_time):
        #self.logger.info(f"Keys that are down: {self.keys_down}")
        self.logger.info(f"Action Queue: {self.action_queue}")