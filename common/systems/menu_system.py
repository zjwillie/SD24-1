from .base_system import System
from common.components.menubutton_component import MenuButtonComponent
from common.components.menuselector_component import MenuSelectorComponent

class MenuSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.menu_entities = []
        self.event_queue = []

        self.entity_manager.subscribe_to_component(MenuButtonComponent, self.on_menu_component_added)
        self.entity_manager.subscribe_to_component(MenuSelectorComponent, self.on_menu_component_added)

        self.event_manager.subscribe("mouse", self.handle_menu_event)

        self.event_manager.subscribe("down", self.handle_menu_event)
        self.event_manager.subscribe("right", self.handle_menu_event)
        self.event_manager.subscribe("up", self.handle_menu_event)
        self.event_manager.subscribe("left", self.handle_menu_event)

        self.event_manager.subscribe("enter", self.handle_menu_event)

        #TODO enter, joystick...., and mouse pressed for menu selector


    def handle_menu_event(self, event, troubleshooting=False):
        print(f"Event received in menu system: {event.type} {event.data}") if troubleshooting else None


        if (event.type == "down" or event.type == "right") and event.data[0] == "down":
            print(f"Down event received in menu system: {event.data}") if troubleshooting else None
            # TODO Coming back after updating "Update Key Maps" in input system to handle one at a time
            
            # TODO This is only to change the current selector
            for entity in self.menu_entities:
                if self.entity_manager.has_component(entity, MenuSelectorComponent):
                    selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                    selector_component.current_selection += 1
                    if selector_component.current_selection >= len(selector_component.menu_options):
                        selector_component.current_selection = 0
        elif (event.type == "up" or event.type == "left") and event.data[0] == "down":
            print(f"Up event received in menu system: {event.data}") if troubleshooting else None
            # TODO Coming back after updating "Update Key Maps" in input system to handle one at a time
            
            # TODO This is only to change the current selector
            for entity in self.menu_entities:
                if self.entity_manager.has_component(entity, MenuSelectorComponent):
                    selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                    selector_component.current_selection -= 1
                    if selector_component.current_selection < 0:
                        selector_component.current_selection = len(selector_component.menu_options) - 1
        elif event.type == "enter" and event.data[0] == "down":
            for entity in self.menu_entities:
                if self.entity_manager.has_component(entity, MenuSelectorComponent):
                    selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                    print(f"Selected option: {selector_component.menu_options[selector_component.current_selection]}") if troubleshooting else None
                    self.event_manager.post(Event("change_state", selector_component.menu_options[selector_component.current_selection][0]))
                    
        
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
        
        self.event_manager.events.remove(event)

    def on_menu_component_added(self, entity, menu_component, action, troubleshooting=False):
        if action == "add":
            print(f"Menu component added to entity {entity}.") if troubleshooting else None
            self.menu_entities.append(entity)
        elif action == "remove":
            print(f"Menu component removed from entity {entity}.") if troubleshooting else None
            self.menu_entities.remove(entity)

    def update(self, delta_time):
        for entity in self.menu_entities:
            if self.entity_manager.has_component(entity, MenuSelectorComponent):
                selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                position_component = self.entity_manager.get_component(entity, PositionComponent)
                position_component.position = selector_component.menu_options[selector_component.current_selection][1]
