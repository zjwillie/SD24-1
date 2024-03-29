import os
import pygame
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.event_manager import Event

class InputManager:
    def __init__(self, event_manager, logger):
        self.logger = logger

        self.event_manager = event_manager

    def update(self, delta_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.loggers['input_manager'].info("Quitting Game")
                escape_event = Event("escape")
                self.event_manager.post(escape_event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escape_event = Event("escape")
                    self.event_manager.post(escape_event)

                print("hi")
                self.logger.loggers['input_manager'].info(f"Key Down: {event.key}")
                key_down_event = Event("key_down", event.key)
                self.event_manager.post(key_down_event)

            if event.type == pygame.KEYUP:
                self.logger.loggers['input_manager'].info(f"Key Up: {event.key}")
                key_up_event = Event("key_up", event.key)
                self.event_manager.post(key_up_event)