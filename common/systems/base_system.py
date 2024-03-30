class System:
    def __init__(self, game_state, entity_manager, event_manager, logger):
        self.game_state = game_state
        self.entity_manager = entity_manager
        self.event_manager = event_manager
        self.logger = logger