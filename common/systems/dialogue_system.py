# Dialogue System
from .base_system import System

from common.managers.event_manager import Event

from common.components.dialogue_component import DialogueComponent

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

    def get_current_dialogue(self, entity):
        return self.get_component(entity, DialogueComponent).current_dialogue


    def update(self, delta_time):
        #TODO Working here
        for entity in self.entity_manager.component_sets[DialogueComponent]:

            dialogue_component = self.get_component(entity, DialogueComponent)

            if dialogue_component.dialogue_name:
                self.logger.debug(f"Entity {entity} has dialogue {dialogue_component.dialogue_name}")
                self.logger.debug(f"Current dialogue: {dialogue_component.current_dialogue.texts[0].content}")