
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File name: grid_system.py
# First Edit: 2020-06-30
# Last Change: 30-Jun-2020.
"""
This content is property of SomebodysDream.
Author: Zac Shepherd (SomebodysDream)
"""
# Grid System
from .base_system import System

from common.managers.event_manager import Event

class GridSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger.loggers['grid_system']

    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)
    

    def update(self, delta_time):
        print("grid_system update called")
