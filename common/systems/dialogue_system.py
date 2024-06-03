import copy
import json
import pygame

# Dialogue System
from .base_system import System

from common.managers.event_manager import Event

from common.components.border_component import BorderComponent
from common.components.dialogue_component import DialogueComponent
from common.components.font_component import FontComponent
from common.components.image_component import ImageComponent
from common.components.textbox_component import TextBoxComponent

# TODO can remove after testing
from common.components.name_component import NameComponent
class DialogueSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.dialogue_source_entity = None
        self.is_active = False

        # Only needed when activating?
        #self.textbox_dialogue_entity = self.entity_manager.get_entity_by_ID("textbox_dialogue_entity")
        #print(f"Textbox Dialogue Entity: {self.get_component(self.textbox_dialogue_entity, DialogueComponent).dialogue_id}")

        self.current_dialogue = None
        self.text_surfaces = []
        self.response_surfaces = []

        self.active_font = None
        self.active_border = None

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
            #TODO duh
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

        self.textbox_dialogue_entity = self.entity_manager.get_entity_by_ID("textbox_dialogue_entity")

        # Get the dialogue source entity
        self.dialogue_source_entity = event.data['entity']
        print(f"Dialogue Source Entity: {self.dialogue_source_entity}")

        enity_name = self.get_component(self.dialogue_source_entity, NameComponent).name
        print(f"Entity Name: {enity_name}")

        dialogue_component = self.get_component(self.dialogue_source_entity, DialogueComponent)
        new_dialogue = copy.deepcopy(dialogue_component)
        # Remove the existing DialogueComponent from textbox_dialogue_entity then add it
        self.entity_manager.remove_component(self.textbox_dialogue_entity, DialogueComponent)
        self.entity_manager.add_component(self.textbox_dialogue_entity, new_dialogue)

        # Set the control component
        self.entity_manager.add_component(self.dialogue_source_entity, "ControlComponent")
        
        # Grab the start of the dialogue
        self.current_dialogue = self.get_component(self.textbox_dialogue_entity, DialogueComponent).dialogues['start']

        # Get the parts for the textbox_component
        # Font
        new_font = FontComponent(self.get_component(self.dialogue_source_entity, TextBoxComponent).font)
        new_border = BorderComponent(self.get_component(self.dialogue_source_entity, TextBoxComponent).border)
        width = self.get_component(self.dialogue_source_entity, TextBoxComponent).width
        height = self.get_component(self.dialogue_source_entity, TextBoxComponent).height
        location = self.get_component(self.dialogue_source_entity, TextBoxComponent).location

        # Remove old and add new textbox component with the new parts
        self.entity_manager.remove_component(self.textbox_dialogue_entity, TextBoxComponent)
        self.entity_manager.add_component(self.textbox_dialogue_entity, TextBoxComponent(new_font, new_border, width, height, location.x, location.y))

        # Create the surfaces for the text and responses
        self.text_surfaces = self.convert_text_to_surfaces(new_font, self.get_next_text().content, width, height)
        self.response_surfaces = self.convert_text_to_surfaces(new_font, self.get_next_responses()[0].content, width, height, single_surface=False)

        # TODO HERE
        # Add surgaces to textbot_dialogue_entity images and set current text and response index to 0
        self.get_component(self.textbox_dialogue_entity, ImageComponent).images = self.text_surfaces
        self.get_component(self.textbox_dialogue_entity, ImageComponent).current_index = 0
        self.get_component(self.textbox_dialogue_entity, ImageComponent).render = True

        # Queue all events associated with starting the dialogue
        self.event_queue.extend(self.current_dialogue.events)


    def deactivate_dialogue(self, event):
        self.is_active = False
        self.entity_manager.remove_component(self.dialogue_source_entity, "ControlComponent")
        self.textbox_dialogue_entity = None
        self.dialogue_source_entity = None
        self.activate_stored_dialogue_events()

    def activate_stored_dialogue_events(self):
        # TODO, event likely not storing correctly
        for event in self.event_queue:
            self.logger.info(f"Event Triggered: {event}")
            self.post_event(event.type, event.data)
        self.event_queue = []

    def split_text_into_lines(self, font, text, width):
        words = text.split(" ")
        lines = []
        current_line = ""
        current_line_width = 0

        for word in words:
            current_word_width = 0
            for letter in word:
                if letter in font.character_list:
                    current_word_width += font.characters[letter].width + font.spacing
                else:
                    print(f"Character {letter} not found in font character list")
                    continue

            if (current_line_width + current_word_width + font.space_width) <= width:
                current_line += word
                current_line_width += current_word_width
                if word != words[-1]:
                    current_line += " "
                    current_line_width += font.space_width
            else:
                lines.append(current_line.strip())
                current_line = word
                current_line_width = current_word_width
                if word != words[-1]:
                    current_line += " "
                    current_line_width += font.space_width

        lines.append(current_line.strip())
        return lines

    def convert_text_to_surfaces(self, font, text, width, height, single_surface=False):
        lines = self.split_text_into_lines(font, text, width)

        surfaces = []
        for i in range(0, len(lines), height // font.line_height):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))

            x_offset = 0
            y_offset = 0
            for line in lines[i:i + height // font.line_height]:
                for letter in line:
                    if letter in font.character_list:
                        char = font.characters[letter]
                        surface.blit(char.sprite, (x_offset, y_offset))
                        x_offset += char.width + font.spacing
                    elif letter == " ":
                        x_offset += font.space_width
                    elif letter == "\n":
                        x_offset = 0
                        y_offset += font.line_height
                y_offset += font.line_height
                x_offset = 0

            bounding_rect = surface.get_bounding_rect()
            trimmed_surface = surface.subsurface(bounding_rect)
            surfaces.append(trimmed_surface)

        return surfaces[0] if single_surface else surfaces
    
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