import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.systems.system_factory import SystemFactory

class SystemManager:
    def __init__(self, game_state, entity_manager, event_manager, logger):
        self.game_state = game_state
        self.entity_manager = entity_manager
        self.event_manager = event_manager

        self.systems = {}
        self.factory = SystemFactory()

        # Must pass in logger to be able to log, can't change to .loggers["system"]
        self.logger = logger
        
    def add_system(self, system_name):
        self.logger.loggers["system"].info(f"Adding system: {system_name}")
        system = self.factory.create_system(system_name, self.game_state, self.entity_manager, self.event_manager, self.logger)
        self.systems[system_name] = system
    
    def add_systems(self, world_data):
        self.logger.loggers["system"].info(f"Adding world systems: {world_data}")
        for system_name in world_data:
            self.add_system(system_name)

    def remove_system(self, system_name):
        self.logger.loggers["system"].info(f"Removing system: {system_name}")
        del self.systems[system_name]

    def get_system(self, system_name):
        return self.systems.get(system_name, None)

    def update(self, delta_time):
        for system in self.systems.values():
            system.update(delta_time)