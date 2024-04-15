# Dialogue System
from .base_system import System

from common.managers.event_manager import Event

from common.components.control_component import ControlComponent
from common.components.font_component import FontComponent
from common.components.text_component import TextComponent

class DialogueSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['dialogue_system']

    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)

    def update(self, delta_time):
        #TODO Working here
        for entity in self.entity_manager.entities_with_font:
            if self.get_component(entity, ControlComponent).enabled:
                self.draw_text(entity)


    def draw_text(self, entity):
        text_component = self.get_component(entity, TextComponent)
        print (text_component.text)

    def draw_text_box(self, entity):
        pass