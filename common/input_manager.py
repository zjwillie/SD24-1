import os
import pygame
import sys
import time

# If this script is run directly, add the parent directory to the system path
# This allows the script to import modules from the parent directory
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.event_manager import Event

# InputManager class handles all the keyboard inputs
class InputManager:

    # Initialize the InputManager with an event manager, logger, and time between key repeats
    def __init__(self, event_manager, logger, time_between_repeats=None):
        self.logger = logger
        self.logger.change_log_level("input_manager", "INFO")

        # Time between key repeats
        self.TIME_BETWEEN_REPEATS = time_between_repeats

        # Event manager instance
        self.event_manager = event_manager

        # Mapping of pygame key events to string representations
        self.key_event_map = {
            pygame.K_0: "0",
            pygame.K_1: "1",
            pygame.K_2: "2",
            pygame.K_3: "3",
            pygame.K_4: "4",
            pygame.K_5: "5",
            pygame.K_6: "6",
            pygame.K_7: "7",
            pygame.K_8: "8",
            pygame.K_9: "9",
            pygame.K_a: "a",
            pygame.K_b: "b",
            pygame.K_c: "c",
            pygame.K_d: "d",
            pygame.K_e: "e",
            pygame.K_f: "f",
            pygame.K_g: "g",
            pygame.K_h: "h",
            pygame.K_i: "i",
            pygame.K_j: "j",
            pygame.K_k: "k",
            pygame.K_l: "l",
            pygame.K_m: "m",
            pygame.K_n: "n",
            pygame.K_o: "o",
            pygame.K_p: "p",
            pygame.K_q: "q",
            pygame.K_r: "r",
            pygame.K_s: "s",
            pygame.K_t: "t",
            pygame.K_u: "u",
            pygame.K_v: "v",
            pygame.K_w: "w",
            pygame.K_x: "x",
            pygame.K_y: "y",
            pygame.K_z: "z",
            pygame.K_SPACE: "space",
            pygame.K_RETURN: "return",
            pygame.K_ESCAPE: "escape",
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right",
            pygame.K_LSHIFT: "left_shift",
            pygame.K_RSHIFT: "right_shift",
            pygame.K_LCTRL: "left_ctrl",
            pygame.K_RCTRL: "right_ctrl",
            pygame.K_LALT: "left_alt",
            pygame.K_RALT: "right_alt",
            pygame.K_TAB: "tab",
            pygame.K_CAPSLOCK: "caps_lock",
            pygame.K_BACKSPACE: "backspace",
            pygame.K_DELETE: "delete",
            pygame.K_HOME: "home",
            pygame.K_END: "end",
            pygame.K_PAGEUP: "page_up",
            pygame.K_PAGEDOWN: "page_down",
            pygame.K_INSERT: "insert",
            pygame.K_F1: "f1",
            pygame.K_F2: "f2",
            pygame.K_F3: "f3",
            pygame.K_F4: "f4",
            pygame.K_F5: "f5",
            pygame.K_F6: "f6",
            pygame.K_F7: "f7",
            pygame.K_F8: "f8",
            pygame.K_F9: "f9",
            pygame.K_F10: "f10",
            pygame.K_F11: "f11",
            pygame.K_F12: "f12",
            pygame.K_NUMLOCK: "num_lock",
            pygame.K_KP0: "keypad_0",
            pygame.K_KP1: "keypad_1",
            pygame.K_KP2: "keypad_2",
            pygame.K_KP3: "keypad_3",
            pygame.K_KP4: "keypad_4",
            pygame.K_KP5: "keypad_5",
            pygame.K_KP6: "keypad_6",
            pygame.K_KP7: "keypad_7",
            pygame.K_KP8: "keypad_8",
            pygame.K_KP9: "keypad_9",
            pygame.K_KP_ENTER: "keypad_enter",
            pygame.K_KP_PLUS: "keypad_plus",
            pygame.K_KP_MINUS: "keypad_minus",
            pygame.K_KP_MULTIPLY: "keypad_multiply",
            pygame.K_KP_DIVIDE: "keypad_divide",
        }

        # Current input map
        self.current_input_map = {}

        # Key repeat interval and timer
        self.key_repeat_interval = {}
        self.key_repeat_timer = {}
        self.repeat_keys = []

        # Keys currently being pressed down
        self.keys_down = {}
        self.keys_down_time = {}

        # Subscribe to TIME_BETWEEN_REPEATS event
        self.event_manager.subscribe(self.event_manager.TIME_BETWEEN_REPEATS, self.update_key_repeat_time)

    # Load world data
    def load_world(self, world_data_input):
        if "TIME_BETWEEN_REPEATS" in world_data_input:
            self.TIME_BETWEEN_REPEATS = world_data_input["TIME_BETWEEN_REPEATS"]
        
        if "repeat_keys" in world_data_input:
            self.repeat_keys = world_data_input["repeat_keys"]

        if "keybindings" in world_data_input:
            self.current_input_map = world_data_input["keybindings"]
        else:
            self.logger.loggers['input_manager'].critical("No keybindings found in world data")
            raise ValueError("No keybindings found in world data")

    # Update key repeat time
    def update_key_repeat_time(self, event):
        self.TIME_BETWEEN_REPEATS = event.data

    # Update function to handle key events
    def update(self):
        prev_keys_down = self.keys_down.copy()
        prev_keys_down_time = self.keys_down_time.copy()

        # Loop through all pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_manager.post(Event(self.event_manager.QUIT))

            # Handle key down events
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_event_map:
                    action = self.current_input_map.get(self.key_event_map[event.key])
                    if action:
                        # Post the action, that it is a down event, the time, and that it is not a repeat
                        key_event = Event(action, (self.event_manager.KEY_DOWN, time.time(), False))
                        self.logger.loggers['input_manager'].info(f"Key Down: {key_event}")
                        self.event_manager.post(key_event)
                        # Store the action in keys_down
                        self.keys_down[action] = time.time()

                        # Record the time when the key is pressed
                        self.keys_down_time[action] = time.time()
                        if self.TIME_BETWEEN_REPEATS is not None:
                            self.key_repeat_interval[action] = self.TIME_BETWEEN_REPEATS
                            self.key_repeat_timer[action] = time.time()

            # Handle key up events
            elif event.type == pygame.KEYUP:
                if event.key in self.key_event_map:
                    action = self.current_input_map.get(self.key_event_map[event.key])
                    if action:
                        if action in self.key_repeat_interval:
                            del self.key_repeat_interval[action]
                            del self.key_repeat_timer[action]

                        if action in self.keys_down_time:
                            # Calculate the duration the key was held down for
                            duration = time.time() - self.keys_down_time[action]
                            del self.keys_down_time[action]

                            # Post the action, that it is an up event, the time, and the duration
                            key_event = Event(action, (self.event_manager.KEY_UP, time.time(), duration))
                            self.logger.loggers['input_manager'].info(f"Key Up: {key_event}, Duration: {duration}")
                            self.event_manager.post(key_event)

                        if action in self.keys_down:
                            del self.keys_down[action]

            # Append any unhandled events to the event manager
            else:
                #unhandled_event = Event("unflagged", event)
                #TODO self.event_manager.events.append(unhandled_event)
                pass

        # Handle key repeat events
        for action in self.key_repeat_interval:
            # Only repeat keys that are in the repeat_keys list
            if action in self.repeat_keys and time.time() - self.key_repeat_timer[action] > self.key_repeat_interval[action]:
                # Post the action, that it is a down event, the time, and that it is a repeat
                repeat_event = Event(action, (self.event_manager.KEY_DOWN, time.time(), True))
                self.logger.loggers['input_manager'].info(f"Key Repeat: {repeat_event}")
                self.event_manager.post(repeat_event)
                self.key_repeat_timer[action] = time.time()

        # If the keys down or keys down time has changed, post a KEYS_DOWN_UPDATE event
        if prev_keys_down != self.keys_down or prev_keys_down_time != self.keys_down_time:
            self.event_manager.post(Event(self.event_manager.KEYS_DOWN_UPDATE, (self.keys_down, self.keys_down_time)))