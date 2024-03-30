from common.systems.player_system import PlayerSystem
from common.systems.time_system import TimeSystem

class SystemFactory:
    def create_system(self, system_name, game_state, entity_manager, event_manager, logger):
        system_data = {
            'game_state': game_state,
            'entity_manager': entity_manager,
            'event_manager': event_manager,
            'logger': logger
        }
        factory_method = getattr(self, f"create_{system_name}", None)
        if factory_method:
            return factory_method(**system_data)
        raise ValueError(f"Factory method for {system_name} not found")

    def create_PlayerSystem(self, **kwargs):
        return PlayerSystem(**kwargs)
    
    def create_TimeSystem(self, **kwargs):
        return TimeSystem(**kwargs)