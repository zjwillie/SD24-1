import os
import pygame
import sys
import time

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.event_manager import Event

class InputManager:
    def __init__(self, event_manager, logger):
        self.logger = logger
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

    def update_key_map(self, new_map):
        self.key_event_map = new_map

    def update(self, delta_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.loggers['input_manager'].info("Quitting Game")
                escape_event = Event("escape")
                self.event_manager.post(escape_event)

            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_event_map:
                    key_event = Event(self.key_event_map[event.key], (event.key, time.time()))
                    self.logger.loggers['input_manager'].info(f"Key Down: {key_event}")
                    self.event_manager.post(key_event)

            elif event.type == pygame.KEYUP:
                if event.key in self.key_event_map:
                    key_event = Event(self.key_event_map[event.key], (event.key, time.time()))
                    self.logger.loggers['input_manager'].info(f"Key Up: {event.key}")
                    self.event_manager.post(key_event)

            # Append any unhandled events to the event manager
            else:
                unhandled_event = Event("unflagged", event)
                #TODO self.event_manager.events.append(unhandled_event)