import os
import pygame
import sys
import time

# If this script is run directly, add the parent directory to the system path
# This allows the script to import modules from the parent directory
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.managers.event_manager import Event

# InputManager class handles all the keyboard inputs
class InputManager:
    REPEAT_DIVISION_FACTOR = 1.6

    # Initialize the InputManager with an event manager, logger, and time between key repeats
    def __init__(self, game_state, event_manager, logger):

        self.logger = logger.loggers['input_manager']

        # Time between key repeats
        self.KEY_REPEAT_INITAL_DELAY = None
        self.KEY_REPEAT_INITAL_SPEED = None
        self.KEY_REPEAT_MAX_SPEED = None

        # Reference to the game state and event manager
        self.game_state = game_state
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

        self.mouse_event_map = {
            1: "mouse_left",
            2: "mouse_middle",
            3: "mouse_right",
            4: "mouse_scroll_up",
            5: "mouse_scroll_down",
            6: "mouse_forward",
            7: "mouse_back"
        }

        self.joystick_event_map = {
            0: "joystick_0",
            1: "joystick_1",
            2: "joystick_2",
            3: "joystick_3",
            4: "joystick_4",
            5: "joystick_5",
            6: "joystick_6",
            7: "joystick_7",
            8: "joystick_8",
            9: "joystick_9",
            10: "joystick_10"
        }

        self.joystick_hat_event_map = {
            (0, (0, 1)): 'joystick_hat_up',
            (0, (0, -1)): 'joystick_hat_down',
            (0, (-1, 0)): 'joystick_hat_left',
            (0, (1, 0)): 'joystick_hat_right',
            (0, (-1, 1)): 'joystick_hat_up_left',
            (0, (1, 1)): 'joystick_hat_up_right',
            (0, (-1, -1)): 'joystick_hat_down_left',
            (0, (1, -1)): 'joystick_hat_down_right',
        }

        # Current input map
        self.current_input_map = {}

        # Key repeat interval and timer
        self.key_repeat_interval = {}
        self.key_repeat_timer = {}
        self.repeat_keys = {}

        # Keys currently being pressed down
        self.keys_down = {}
        self.keys_down_time = {}

        # Joystick axis
        self.joystick_axis = {'x': 0, 'y': 0, 'facing_x': 0, 'facing_y': 0}

    # Load world data
    def load_input_data(self, world_data_input):
        if "KEY_REPEAT_INITAL_DELAY" in world_data_input:
            self.KEY_REPEAT_INITAL_DELAY = world_data_input["KEY_REPEAT_INITAL_DELAY"]

        if "KEY_REPEAT_INITAL_SPEED" in world_data_input:
            self.KEY_REPEAT_INITAL_SPEED = world_data_input["KEY_REPEAT_INITAL_SPEED"]

        if "KEY_REPEAT_MAX_SPEED" in world_data_input:
            self.KEY_REPEAT_MAX_SPEED = world_data_input["KEY_REPEAT_MAX_SPEED"]

        if "repeat_keys" in world_data_input:
            self.repeat_keys = world_data_input["repeat_keys"]

        if "keybindings" in world_data_input:
            self.current_input_map = world_data_input["keybindings"]
        else:
            self.logger.critical("No keybindings found in world data")
            raise ValueError("No keybindings found in world data")

    # Update function to handle key events
    def update(self):

        # Loop through all pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_manager.post(Event(self.event_manager.QUIT))

            #^ KEYBOARD #########################################################################################
            # Handle key down events
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_event_map:
                    action = self.current_input_map.get(self.key_event_map[event.key])
                    if action:
                        if action not in self.keys_down:
                            self.keys_down[action] = True
                            self.keys_down_time[action] = time.time()

                            # Post the action, that it is a down event, and the time
                            key_event = Event(action, (self.event_manager.KEY_DOWN, time.time(), self.event_manager.KEYBOARD_EVENT))
                            self.logger.info(f"Key Down: {key_event}")
                            self.event_manager.post(key_event)

                        if action in self.repeat_keys and action not in self.key_repeat_interval:
                            self.key_repeat_interval[action] = self.KEY_REPEAT_INITAL_SPEED
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
                            self.logger.info(f"Key Up: {key_event}, Duration: {duration}")
                            self.event_manager.post(key_event)

                        if action in self.keys_down:
                            del self.keys_down[action]

            #^ MOUSE #########################################################################################
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in self.mouse_event_map:
                    action = self.current_input_map.get(self.mouse_event_map[event.button])
                    if action:
                        self.keys_down[action] = True
                        self.keys_down_time[action] = time.time()

                        mouse_pos = event.pos

                        # Post the action, that it is a down event, and the time
                        key_event = Event(action, (self.event_manager.KEY_DOWN, time.time(), self.event_manager.MOUSE_EVENT, mouse_pos))
                        self.logger.info(f"Mouse Down: {key_event}")
                        self.event_manager.post(key_event)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in self.mouse_event_map:
                    action = self.current_input_map.get(self.mouse_event_map[event.button])
                    if action:
                        if action in self.keys_down_time:
                            # Calculate the duration the key was held down for
                            duration = time.time() - self.keys_down_time[action]
                            del self.keys_down_time[action]

                            mouse_pos = event.pos

                            # Post the action, that it is an up event, the time, and the duration
                            key_event = Event(action, (self.event_manager.KEY_UP, time.time(), duration, self.event_manager.MOUSE_EVENT, mouse_pos))
                            self.logger.info(f"Mouse Up: {key_event}, Duration: {duration}")
                            self.event_manager.post(key_event)

                        if action in self.keys_down:
                            del self.keys_down[action]

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                # Could send if a mouse button is held down or not as well, would need to keep a list of mouse being down but dont' think this is needed right now
                self.logger.info(f"Mouse Motion: {mouse_pos}")
                self.event_manager.post(Event(self.event_manager.MOUSE_POSITION, mouse_pos))

            #^ JOYSTICK #########################################################################################
            elif event.type == pygame.JOYDEVICEADDED:
                self.game_state.activate_joysticks()

            elif event.type == pygame.JOYDEVICEREMOVED:
                self.game_state.deactivate_joysticks()

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in self.joystick_event_map:
                    action = self.current_input_map.get(self.joystick_event_map[event.button])
                    
                    if action:
                        self.keys_down[action] = True
                        self.keys_down_time[action] = time.time()

                        # Post the action, that it is a down event, and the time
                        key_event = Event(action, (self.event_manager.KEY_DOWN, time.time(), self.event_manager.JOYSTICK_EVENT))
                        self.logger.info(f"Joystick Down: {key_event}")
                        self.event_manager.post(key_event)

            elif event.type == pygame.JOYBUTTONUP:
                if event.button in self.joystick_event_map:
                    action = self.current_input_map.get(self.joystick_event_map[event.button])
                    if action:
                        if action in self.keys_down_time:
                            # Calculate the duration the key was held down for
                            duration = time.time() - self.keys_down_time[action]
                            del self.keys_down_time[action]

                            # Post the action, that it is an up event, the time, and the duration
                            key_event = Event(action, (self.event_manager.KEY_UP, time.time(), duration, self.event_manager.JOYSTICK_EVENT))
                            self.logger.info(f"Joystick Up: {key_event}, Duration: {duration}")
                            self.event_manager.post(key_event)

                        if action in self.keys_down:
                            del self.keys_down[action]

            elif event.type == pygame.JOYHATMOTION:
                hat_data = (event.hat, event.value)
                self.logger.info(f"Joystick Hat: {hat_data}")
                if hat_data in self.joystick_hat_event_map:
                    action = self.current_input_map.get(self.joystick_hat_event_map[hat_data])
                    if action:
                        self.keys_down[action] = True
                        self.keys_down_time[action] = time.time()
            
                        # Post the action, that it is a down event, the time, and the hat value
                        key_event = Event(action, (self.event_manager.KEY_DOWN, time.time(), event.value, self.event_manager.JOYSTICK_EVENT))
                        self.logger.info(f"Joystick Hat to post: {key_event}")
                        self.event_manager.post(key_event)


            elif event.type == pygame.JOYAXISMOTION:
                axis_data = (event.axis, event.value)

                TESTING_THRESHOLD = 0.1

                if abs(event.value) > TESTING_THRESHOLD:
                    self.logger.info(f"Joystick Axis: {axis_data}")
            
            
                if event.axis == 0:
                    if abs(event.value) > TESTING_THRESHOLD:
                        self.joystick_axis["x"] = event.value
                    else:
                        self.joystick_axis["x"] = 0
                elif event.axis == 1:
                    if abs(event.value) > TESTING_THRESHOLD:
                        self.joystick_axis["y"] = event.value
                    else:
                        self.joystick_axis["y"] = 0
                elif event.axis == 2:
                    if abs(event.value) > TESTING_THRESHOLD:
                        self.joystick_axis["facing_x"] = event.value
                    else:
                        self.joystick_axis["facing_x"] = 0
                elif event.axis == 3:
                    if abs(event.value) > TESTING_THRESHOLD:
                        self.joystick_axis["facing_y"] = event.value
                    else:
                        self.joystick_axis["facing_y"] = 0


            # Append any unhandled events to the event manager
            else:
                # Handle ACTIVEEVENT like window being moved
                #unhandled_event = Event("unflagged", event)
                #print(event)
                #TODO self.event_manager.events.append(unhandled_event)
                pass

        # Handle key repeat events
        for action in self.key_repeat_interval:
            # Only repeat keys that are in the repeat_keys dictionary
            if action in self.repeat_keys:
                # Add a delay before repeating
                if time.time() - self.keys_down_time[action] > self.KEY_REPEAT_INITAL_DELAY:
                    # Increase the repeat speed exponentially until it reaches max speed
                    if time.time() - self.key_repeat_timer[action] > self.key_repeat_interval[action]:
                        # Change the division factor from 2 to a larger number for a more gradual speed increase
                        self.key_repeat_interval[action] = max(self.key_repeat_interval[action] / self.REPEAT_DIVISION_FACTOR, self.KEY_REPEAT_MAX_SPEED)

                        # Post the action, that it is a down event, the time, and that it is a repeat
                        repeat_event = Event(action, (self.event_manager.KEY_DOWN, time.time(), True))
                        self.logger.info(f"Key Repeat: {repeat_event}")
                        self.event_manager.post(repeat_event)
                        self.key_repeat_timer[action] = time.time()

        # If the keys down or keys down time has changed, post a movementment key event
        self.logger.info(f"Keys Down: {self.keys_down}, Keys Down Time: {self.keys_down_time}, Joystick Axis: {self.joystick_axis}")
        self.event_manager.post(Event(self.event_manager.MOVEMENT_KEY_EVENT, {'keys_down_time': self.keys_down_time, 'joystick_axis': self.joystick_axis}))
