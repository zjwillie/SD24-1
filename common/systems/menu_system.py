from .base_system import System

from common.event_manager import Event
from common.components.menubutton_component import MenuButtonComponent
from common.components.menuselector_component import MenuSelectorComponent
from common.components.position_component import PositionComponent


class MenuSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger
        self.logger.change_log_level('menu_system', "INFO")

        self.menu_entities = []
        self.current_menu = None
        self.current_selector = None

        self.event_manager.subscribe("down", self.handle_menu_event)
        self.event_manager.subscribe("right", self.handle_menu_event)
        self.event_manager.subscribe("up", self.handle_menu_event)
        self.event_manager.subscribe("left", self.handle_menu_event)
        self.event_manager.subscribe("return", self.handle_menu_event)

        self.event_manager.subscribe("set_menu", self.set_menu)

    def set_menu(self, event):
        self.logger.loggers['menu_system'].info(f'Set menu: {event.type} {event.data}!')

        if self.current_menu:
            self.entity_manager.entities_to_render.remove(self.current_menu)
            self.entity_manager.menu_entities.remove(self.current_menu)
        if self.current_selector:
            self.entity_manager.entities_to_render.remove(self.current_selector)
            self.entity_manager.menu_entities.remove(self.current_selector)

        self.current_menu = self.entity_manager.get_entity_by_name(event.data[0])
        self.current_selector = self.entity_manager.get_entity_by_name(event.data[1])

        self.entity_manager.entities_to_render.add(self.current_menu)
        self.entity_manager.menu_entities.add(self.current_menu)
        self.entity_manager.entities_to_render.add(self.current_selector)
        self.entity_manager.menu_entities.add(self.current_selector)

        self.entity_manager.get_component(self.current_selector, MenuSelectorComponent).current_selection = 0

        #TODO enter, joystick...., and mouse pressed for menu selector

    def update(self, delta_time):
        for entity in self.entity_manager.menu_entities:
            if self.entity_manager.has_component(entity, MenuSelectorComponent):
                selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                position_component = self.entity_manager.get_component(entity, PositionComponent)
                position_component.position = selector_component.options[selector_component.current_selection]['position']


    def handle_menu_event(self, event, troubleshooting=False):
        self.logger.loggers['menu_system'].info(f"Event received in menu system - Type '{event.type}', Data '{event.data}'")

        if (event.type == "down") and event.data[0] == "key_down":
            self.logger.loggers['menu_system'].info(f"Down event received in menu system: {event.data}")

            if self.current_selector:
                selector_component = self.entity_manager.get_component(self.current_selector, MenuSelectorComponent)
                selector_component.current_selection += 1
                if selector_component.current_selection >= len(selector_component.options):
                    selector_component.current_selection = 0

        elif (event.type == "up") and event.data[0] == "key_down":
            self.logger.loggers['menu_system'].info(f"Up event received in menu system: {event.data}")

            if self.current_selector:
                selector_component = self.entity_manager.get_component(self.current_selector, MenuSelectorComponent)
                selector_component.current_selection -= 1
                if selector_component.current_selection < 0:
                    selector_component.current_selection = len(selector_component.options) - 1

        elif event.type == "return" and event.data[0] == "key_down":
            self.logger.loggers['menu_system'].info(f"Return event received in menu system: {event.data}")
            if self.current_selector:
                selector_component = self.entity_manager.get_component(self.current_selector, MenuSelectorComponent)
                self.logger.loggers['menu_system'].info(f"Posting option: 'change_state', {selector_component.options[selector_component.current_selection]['name']}")
                self.event_manager.post(Event("change_state", selector_component.options[selector_component.current_selection]["name"]))



        """                    
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
        
        """