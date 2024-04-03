import os
import pygame
import sys
import time

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.event_manager import Event

class InputManager:

    def __init__(self, event_manager, logger, time_between_repeats=None):
        self.logger = logger
        self.logger.change_log_level("input_manager", "OFF")

        self.TIME_BETWEEN_REPEATS = time_between_repeats

        self.event_manager = event_manager

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

        self.key_repeat_interval = {}
        self.key_repeat_timer = {}

        self.keys_down = {}
        self.keys_down_time = {}

        self.event_manager.subscribe(self.event_manager.TIME_BETWEEN_REPEATS, self.update_key_repeat_time)

    def load_world(self, world_data_input):
        if "TIME_BETWEEN_REPEATS" in world_data_input:
            self.TIME_BETWEEN_REPEATS = world_data_input["TIME_BETWEEN_REPEATS"]

    def key_down(self, key, repeat_interval=None):
        self.keys_down[key] = True
        self.keys_down_time[key] = time.time()
        if repeat_interval is not None:
            self.key_repeat_interval[key] = repeat_interval
            self.key_repeat_timer[key] = time.time()

    def key_up(self, key):
        if key in self.key_repeat_interval:
            del self.key_repeat_interval[key]
            del self.key_repeat_timer[key]

        if key in self.keys_down_time:
            duration = time.time() - self.keys_down_time[key]
            del self.keys_down_time[key]
            key_event = Event(self.key_event_map[key], (self.event_manager.KEY_UP, time.time(), duration))
            self.logger.loggers['input_manager'].info(f"Key Up: {key_event}, Duration: {duration}")
            self.event_manager.post(key_event)

        if key in self.keys_down:
            del self.keys_down[key] 

    def update_key_repeat_time(self, event):
        self.TIME_BETWEEN_REPEATS = event.data

    def set_key_repeat_interval(self, key, interval):
        self.key_repeat_interval[key] = interval

    def remove_key_repeat_interval(self, key):
        if key in self.key_repeat_interval:
            del self.key_repeat_interval[key]

#? **************** UPDATE FUNCTION ****************

    def update(self):
        prev_keys_down = self.keys_down.copy()
        prev_keys_down_time = self.keys_down_time.copy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.loggers['input_manager'].info("Quitting Game")
                escape_event = Event(self.event_manager.EVENT_ESCAPE, (self.event_manager.QUIT, time.time()))
                self.event_manager.post(escape_event)

            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_event_map:
                    # Post the key, that it is a down event, the time, and that it is not a repeat
                    key_event = Event(self.key_event_map[event.key], (self.event_manager.KEY_DOWN, time.time(), False))
                    self.logger.loggers['input_manager'].info(f"Key Down: {key_event}")
                    self.event_manager.post(key_event)

                    # Record the time when the key is pressed
                    self.keys_down[event.key] = True
                    self.keys_down_time[event.key] = time.time()
                    if self.TIME_BETWEEN_REPEATS is not None:
                        self.key_repeat_interval[event.key] = self.TIME_BETWEEN_REPEATS
                        self.key_repeat_timer[event.key] = time.time()

            elif event.type == pygame.KEYUP:
                if event.key in self.key_event_map:
                    if event.key in self.key_repeat_interval:
                        del self.key_repeat_interval[event.key]
                        del self.key_repeat_timer[event.key]

                    if event.key in self.keys_down_time:
                        # Calculate the duration the key was held down for
                        duration = time.time() - self.keys_down_time[event.key]
                        del self.keys_down_time[event.key]

                        # Post the key, that it is an up event, the time, and the duration
                        key_event = Event(self.key_event_map[event.key], (self.event_manager.KEY_UP, time.time(), duration))
                        self.logger.loggers['input_manager'].info(f"Key Up: {key_event}, Duration: {duration}")
                        self.event_manager.post(key_event)

                    if event.key in self.keys_down:
                        del self.keys_down[event.key]

            # Append any unhandled events to the event manager
            else:
                #unhandled_event = Event("unflagged", event)
                #TODO self.event_manager.events.append(unhandled_event)
                pass

        for key in self.key_repeat_interval:
            if time.time() - self.key_repeat_timer[key] > self.key_repeat_interval[key]:

                # Post the key, that it is a down event, the time, and that it is a repeat
                repeat_event = Event(self.key_event_map[key], (self.event_manager.KEY_DOWN, time.time(), True))
                self.logger.loggers['input_manager'].info(f"Key Repeat: {repeat_event}")
                self.event_manager.post(repeat_event)
                self.key_repeat_timer[key] = time.time()

        if prev_keys_down != self.keys_down or prev_keys_down_time != self.keys_down_time:
            self.event_manager.post(Event(self.event_manager.KEYS_DOWN_UPDATE, (self.keys_down, self.keys_down_time)))