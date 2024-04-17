import time

class Event:
    def __init__(self, event_type, data=None):
        self.type = event_type
        self.data = data

    def __str__(self):
        return f"Event: Type({self.type}) Data{self.data} <- EVENT OBJECT"

class EventManager:
    # region Event Types
    EVENT_DOWN = "down"
    EVENT_UP = "up"
    EVENT_LEFT = "left"
    EVENT_RIGHT = "right"
    EVENT_RETURN = "return"
    EVENT_ESCAPE = "escape"
    EVENT_TAB = "tab"
    EVENT_RUN = "run"
    EVENT_LIGHT_ATTACK = "light_attack"
    EVENT_HEAVY_ATTACK = "heavy_attack"
    EVENT_DODGE = "dodge"
    EVENT_BLOCK = "block"
    EVENT_JUMP = "jump"
    EVENT_INTERACT = "interact"
    EVENT_SPACE = "space"

    KEY_DOWN = "key_down"
    KEY_UP = "key_up"

    MOVEMENT_KEY_EVENT = "movement_key_event"
    JOYSTICK_AXIS_UPDATE = "joystick_axis_update"

    PLAYER_ANIMATION_FINISHED = "player_animation_finished"

    KEYBOARD_EVENT = "keyboard_event"
    MOUSE_EVENT = "mouse_event"
    MOUSE_POSITION = "mouse_position"
    JOYSTICK_EVENT = "joystick_event"

    MAIN_MENU_BACKGROUND = "main_menu_background"
    MAIN_MENU_SELECTOR = "main_menu_selector"
    OPTIONS_MENU_BACKGROUND = "options_menu_background"
    OPTIONS_MENU_BACKGROUND_NO_SOUND = "options_menu_background_no_sound"
    OPTIONS_MENU_SELECTOR = "options_menu_selector"

    TIME_BETWEEN_REPEATS = "time_between_repeats"

    SET_MENU = "set_menu"
    QUIT = "quit"
    CHANGE_STATE = "change_state"
    OPTIONS = "options"
    MAIN_MENU = "main_menu"
    SOUND = "sound"
    EXIT_REQUESTED = "exit_requested"

    START_GAME = "start_game"
    # endregion

    def __init__(self, logger):
        self.logger = logger
        self.logger.change_log_level("event_manager", "OFF")
        
        self.events = []
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)

    def post(self, event):
        self.logger.loggers['event_manager'].info(f"Event Posted:\n Type: {event.type}, Data: {event.data}")
        self.events.append(event)

    def urgent_post(self, event):
        self.logger.loggers['event_manager'].info(f"Urgent Event Posted:\n Type: {event.type}, Data: {event.data}")
        self.events.insert(0, event)

    def critical_post(self, event):
        self.logger.loggers['event_manager'].info(f"Critical Event Posted:\n Type: {event.type}, Data: {event.data}")
        for subscriber in self.subscribers.get(event.type, []):
            subscriber(event)

    def process_events(self):
        while self.events:
            event = self.events.pop(0)
            self.logger.loggers['event_manager'].info(f"Event processing:\n Type: {event.type}, Data: {event.data}")
            for subscriber in self.subscribers.get(event.type, []):
                subscriber(event)

    def update(self):
        self.process_events()