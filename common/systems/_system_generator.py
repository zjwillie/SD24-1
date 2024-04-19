import os

def create_new_system(system_name):
    # Convert system_name to CamelCase for the class name
    class_name = ''.join(word.title() for word in system_name.split('_'))

    # Define the relative path to the systems directory
    systems_dir = os.path.join("common", "systems")

    # Create the new system file in the systems directory
    with open(os.path.join(systems_dir, f"{system_name}_system.py"), "w") as file:
        file.write(f"""
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: {system_name}_system.py
# First Edit: 2020-06-30
# Last Change: 30-Jun-2020.
\"\"\"
This content is property of SomebodysDream.
Author: Zac Shepherd (SomebodysDream)
\"\"\"
# {class_name} System
from .base_system import System

from common.managers.event_manager import Event

class {class_name}System(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger.loggers['{system_name}_system']

    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)
    

    def update(self, delta_time):
        pass
""")

    # Add the new system to the __init__.py file
    with open(os.path.join(systems_dir, "__init__.py"), "a") as file:
        file.write(f"from .{system_name}_system import {class_name}System\n")

# Usage
create_new_system("grid")