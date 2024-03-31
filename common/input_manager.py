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

    def update(self, delta_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.loggers['input_manager'].info("Quitting Game")
                escape_event = Event("escape")
                self.event_manager.post(escape_event)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escape_event = Event("escape")
                    self.event_manager.post(escape_event)
                elif event.key == pygame.K_UP:
                    up_event = Event("up")
                    self.event_manager.post(up_event)

                # TODO Not just key down!!! Needs to send the damn key
                key_down_event = Event("key_down", (event.key, time.time()))
                self.logger.loggers['input_manager'].info(f"Key Down: {key_down_event}")
                self.event_manager.post(key_down_event)

            elif event.type == pygame.KEYUP:
                key_up_event = Event("key_down", (event.key, time.time()))
                self.logger.loggers['input_manager'].info(f"Key Up: {event.key}")
                self.event_manager.post(key_up_event)

            # Append any unhandled events to the event manager
            else:
                unhandled_event = Event("unflagged", event)
                #TODO self.event_manager.events.append(unhandled_event)