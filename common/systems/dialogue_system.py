import json

# Dialogue System
from .base_system import System

from common.managers.event_manager import Event

from common.components.dialogue_component import DialogueComponent

class DialogueSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.dialogue_entity = None
        self.is_active = False
        self.active_dialogue = DialogueComponent()
        self.current_dialogue = None

        self.event_queue = []

        self.logger = logger.loggers['dialogue_system']
        
        self.event_manager.subscribe(self.event_manager.EVENT_START_DIALOGUE, self.activate_dialogue)
        self.event_manager.subscribe(self.event_manager.EVENT_END_DIALOGUE, self.deactivate_dialogue)

    def post_event(self, event_type, data):                                         
        self.event_manager.post(Event(event_type, data))

    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)

    def get_current_dialogue(self, entity):
        return self.get_component(entity, DialogueComponent).current_dialogue

    def check_conditions(self, conditions):
        for condition in conditions:
            if condition.type == "world_flag":
                with open("common/data/world_flags.json", "r") as file:
                    world_flags = json.load(file)
                if condition.name in world_flags:
                    if condition.operator == "==":
                        if world_flags[condition.name] == condition.value:
                            return True
                    elif condition.operator == "!=":
                        if world_flags[condition.name] != condition.value:
                            return True
                
            elif condition.type == "entity_flag":
                pass
            elif condition.type == "player_flag":
                pass

        return False

    def get_next_text(self):
        # Get the first possible text
        # Check the conditions
        # Return the first text for which the conditions are met
        for text in self.current_dialogue.texts:
            # Check if there are conditions, if so check them, if not return the content
            if text.conditions:
                if self.check_conditions(text.conditions):
                    self.event_queue.extend(text.events)
                    return text
            else:
                return text

        raise ValueError("No valid text found.")

    def get_next_responses(self):
        # Get all responses that pass the conditions
        responses = []
        for response in self.current_dialogue.responses:
            if response.conditions:
                if self.check_conditions(response.conditions):
                    responses.append(response)
            else:
                responses.append(response)
        
        return responses

    def activate_dialogue(self, event):
        print(f"Activtaing dialogue: {event.data}")
        # Let the system know that the dialogue is active
        self.is_active = True

        # Get the dialogue entity
        self.dialogue_entity = event.data['entity']

        # Create a copy of the dialogue
        self.active_dialogue = DialogueComponent(self.get_component(self.dialogue_entity, DialogueComponent).dialogue_id)
        
        # Set the control component
        self.entity_manager.add_component(self.dialogue_entity, "ControlComponent")
        
        # Grab the start of the dialogue
        self.current_dialogue = self.active_dialogue.dialogues["start"]
        
        # Queue all events associated with starting the dialogue
        self.event_queue.extend(self.current_dialogue.events)

    def deactivate_dialogue(self, event):
        self.is_active = False
        self.entity_manager.remove_component(self.dialogue_entity, "ControlComponent")
        self.active_dialogue = None
        self.dialogue_entity = None
        self.trigger_events()

    def trigger_events(self):
        # TODO, event likely not storing correctly
        for event in self.event_queue:
            self.logger.info(f"Event Triggered: {event}")
            self.post_event(event.type, event.data)
        self.event_queue = []

    
#? *************************

    def update(self, delta_time):
        #TODO Working here

        if self.is_active:
            #self.logger.info(f"Active Dialogue: {self.active_dialogue.dialogue_id}")
            next_text = self.get_next_text()
            print(next_text.content)
            next_responses = self.get_next_responses()
            for next_response in next_responses:
                print(next_response.content)