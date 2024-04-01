from .base_system import System

from common.event_manager import Event
from common.components.menubutton_component import MenuButtonComponent
from common.components.menuselector_component import MenuSelectorComponent
from common.components.position_component import PositionComponent


class MenuSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger
        self.logger.change_log_level('menu_system', "OFF")

        self.menu_entities = []
        self.event_queue = []

        self.event_manager.subscribe("down", self.handle_menu_event)
        self.event_manager.subscribe("right", self.handle_menu_event)
        self.event_manager.subscribe("up", self.handle_menu_event)
        self.event_manager.subscribe("left", self.handle_menu_event)

        self.event_manager.subscribe("return", self.handle_menu_event)

        #TODO enter, joystick...., and mouse pressed for menu selector

    def update(self, delta_time):
        for entity in self.entity_manager.menu_entities:
            if self.entity_manager.has_component(entity, MenuSelectorComponent):
                selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                position_component = self.entity_manager.get_component(entity, PositionComponent)
                position_component.position = selector_component.options[selector_component.current_selection]['position']


    def handle_menu_event(self, event, troubleshooting=False):
        print(f"Event received in menu system - Type '{event.type}', Data '{event.data}'") if troubleshooting else None

        if (event.type == "down" or event.type == "right") and event.data[0] == "key_down":
            print(f"Down event received in menu system: {event.data}") if troubleshooting else None
            # TODO Coming back after updating "Update Key Maps" in input system to handle one at a time
            
            # TODO This is only to change the current selector
            for entity in self.entity_manager.menu_entities:
                if self.entity_manager.has_component(entity, MenuSelectorComponent):
                    selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                    selector_component.current_selection += 1
                    if selector_component.current_selection >= len(selector_component.options):
                        selector_component.current_selection = 0

        elif (event.type == "up" or event.type == "left") and event.data[0] == "key_down":
            print(f"Up event received in menu system: {event.data}") if troubleshooting else None
            # TODO Coming back after updating "Update Key Maps" in input system to handle one at a time
            
            # TODO This is only to change the current selector
            for entity in self.entity_manager.menu_entities:
                if self.entity_manager.has_component(entity, MenuSelectorComponent):
                    selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                    selector_component.current_selection -= 1
                    if selector_component.current_selection < 0:
                        selector_component.current_selection = len(selector_component.options) - 1

        elif event.type == "return" and event.data[0] == "key_down":
            print(f"Return event received in menu system: {event.data}") if troubleshooting else None
            for entity in self.entity_manager.menu_entities:
                if self.entity_manager.has_component(entity, MenuSelectorComponent):
                    selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                    print(f"Posting option: 'change_state', {selector_component.options[selector_component.current_selection]['name']}") if troubleshooting else None
                    self.event_manager.post(Event("change_state", selector_component.options[selector_component.current_selection]["name"]))
                    
        #TODO Not updated from SD
        if event.type == "mouse":
            print(f"Mouse event received in menu system: ({event.data})") if troubleshooting else None
            if event.data.action == "down":
                for entity, (position, menu_selector, image_component) in self.entity_manager.get_entities_with_components(PositionComponent, MenuSelectorComponent, ImageComponent):
                    menu_width = image_component.images[0].get_width()
                    menu_height = image_component.images[0].get_height()
                    print(menu_selector.menu_options) if troubleshooting else None
                    for i in range(len(menu_selector.menu_options)):
                        menu_option, position = menu_selector.menu_options[i]
                        print(f"Checking position: {position}") if troubleshooting else None
                        print(image_component.images[0], image_component.images[0]) if troubleshooting else None
                        if (position[0] < event.data.position[0] < position[0] + menu_width) and (position[1] < event.data.position[1] < position[1] + menu_height):
                            print(f"Mouse clicked on {menu_option}") if troubleshooting else None
                            self.event_manager.post(Event("change_state", menu_selector.menu_options[menu_selector.current_selection][0]))
        
