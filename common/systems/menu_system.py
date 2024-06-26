from pygame.math import Vector2

from .base_system import System

from common.managers.event_manager import Event

from common.components.menu_component import MenuComponent
from common.components.menuselector_component import MenuSelectorComponent
from common.components.render_component import RenderComponent
from common.components.position_component import PositionComponent
from common.components.size_component import SizeComponent

class MenuSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger.loggers['menu_system']

        self.current_menu = None
        self.current_selector = None

        self.event_manager.subscribe(self.event_manager.EVENT_MOVE_DOWN, self.handle_menu_event)
        self.event_manager.subscribe(self.event_manager.EVENT_MOVE_RIGHT, self.handle_menu_event)
        self.event_manager.subscribe(self.event_manager.EVENT_MOVE_UP, self.handle_menu_event)
        self.event_manager.subscribe(self.event_manager.EVENT_MOVE_LEFT, self.handle_menu_event)
        self.event_manager.subscribe(self.event_manager.EVENT_RETURN, self.handle_menu_event)

        self.event_manager.subscribe(self.event_manager.MOUSE_POSITION, self.handle_menu_event)

        self.event_manager.subscribe("set_menu", self.set_menu)

    def set_menu(self, event):
        self.logger.info(f'Set menu: {event.type} {event.data}!')
    
        self.entity_manager.component_sets[MenuComponent].clear()
    
        # Hide the current menu and selector
        if self.current_menu:
            self.entity_manager.get_component(self.current_menu, RenderComponent).render = False
        if self.current_selector:
            self.entity_manager.get_component(self.current_selector, RenderComponent).render = False
    
        # Change to the new menu and selector
        self.current_menu = self.entity_manager.get_entity_by_name(event.data[0])
        self.current_selector = self.entity_manager.get_entity_by_name(event.data[1])
    
        # Add the current menu items to the menu_entities
        self.entity_manager.component_sets[MenuComponent].add(self.current_menu)
        self.entity_manager.component_sets[MenuComponent].add(self.current_selector)
    
        self.entity_manager.get_component(self.current_menu, RenderComponent).render = True
        self.entity_manager.get_component(self.current_selector, RenderComponent).render = True
    
        if event.data[2]:
            self.entity_manager.get_component(self.current_selector, MenuSelectorComponent).current_selection = 0

    def update(self, delta_time):
        for entity in self.entity_manager.component_sets[MenuComponent]:
            if self.entity_manager.has_component(entity, MenuSelectorComponent):
                selector_component = self.entity_manager.get_component(entity, MenuSelectorComponent)
                position_component = self.entity_manager.get_component(entity, PositionComponent)
                position_component.position = Vector2(selector_component.options[selector_component.current_selection]['position'])


    def handle_menu_event(self, event):
        self.logger.info(f"Event received in menu system - Type '{event.type}', Data '{event.data}'")

        if (event.type == self.event_manager.EVENT_MOVE_DOWN) and event.data[0] == self.event_manager.KEY_DOWN:
            self.logger.info(f"Down event received in menu system: {event.data}")

            self.update_selection(1)

        elif (event.type == self.event_manager.EVENT_MOVE_UP) and event.data[0] == self.event_manager.KEY_DOWN:
            self.logger.info(f"Up event received in menu system: {event.data}")

            self.update_selection(-1)

        elif event.type == self.event_manager.EVENT_RETURN and event.data[0] == self.event_manager.KEY_DOWN:
            self.logger.info(f"Return event received in menu system: {event.data}")
            if self.current_selector:
                if event.data[2] == self.event_manager.KEYBOARD_EVENT or event.data[2] == self.event_manager.JOYSTICK_EVENT:
                    selector_component = self.entity_manager.get_component(self.current_selector, MenuSelectorComponent)
                    self.logger.info(f"Posting option: 'change_state', {selector_component.options[selector_component.current_selection]['name']}")
                    self.event_manager.post(Event("change_state", (selector_component.options[selector_component.current_selection]["name"], True)))
                elif event.data[2] == self.event_manager.MOUSE_EVENT:
                    # check if the mouse is over the selector
                    mouse_position = event.data[3]
                    selector_position = self.entity_manager.get_component(self.current_selector, PositionComponent).position
                    selector_size = self.entity_manager.get_component(self.current_selector, SizeComponent)
                    if (selector_position[0] < mouse_position[0] < selector_position[0] + selector_size.width) and (selector_position[1] < mouse_position[1] < selector_position[1] + selector_size.height):
                        selector_component = self.entity_manager.get_component(self.current_selector, MenuSelectorComponent)
                        self.logger.info(f"Posting option: 'change_state', {selector_component.options[selector_component.current_selection]['name']}")
                        self.event_manager.post(Event("change_state", (selector_component.options[selector_component.current_selection]["name"], True)))

        elif event.type == self.event_manager.MOUSE_POSITION:
            self.logger.info(f"Mouse position event received in menu system: {event.data}")
            if self.current_selector:
                selector_component = self.entity_manager.get_component(self.current_selector, MenuSelectorComponent)
                for i in range(len(selector_component.options)):
                    option = selector_component.options[i]
                    position = option['position']
                    size = option['size']
                    if (position[0] < event.data[0] < position[0] + size[0]) and (position[1] < event.data[1] < position[1] + size[1]):
                        selector_component.current_selection = i

    def update_selection(self, increment):
        if self.current_selector:
            selector_component = self.entity_manager.get_component(self.current_selector, MenuSelectorComponent)
            selector_component.current_selection += increment
            if selector_component.current_selection >= len(selector_component.options):
                selector_component.current_selection = 0
            elif selector_component.current_selection < 0:
                selector_component.current_selection = len(selector_component.options) - 1