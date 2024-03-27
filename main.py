import ctypes
import json
import os
import pygame
import random
import time
import typing
import uuid

# package imports
#from common.components import *
from common.entity_manager import EntityManager

# Debugging
import cProfile
import logging

def main():
    #ctypes.windll.user32.SetProcessDPIAware()

    # region Initialize pygame
    pygame.init()

    # create a screen
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)#, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED)
    pygame.display.set_caption("ECS SD Build 0.0.4.1")

    # Set the title of the window
    pygame.display.set_caption("Somebody's Dream Build 0.0.4")

    icon = pygame.image.load("images/icons/main_icon.png")
    pygame.display.set_icon(icon)
    # endregion

    # Set up clock
    clock = pygame.time.Clock()
    start_time = time.time()

    #! Debugging Setup
    # region Set up logger
    loggers = {
        'component': logging.getLogger('component'),
        'current': logging.getLogger('current')
    }
    loggers['component'].setLevel(logging.WARNING)  # Only log warning, error, and critical messages from 'component'
    loggers['current'].setLevel(logging.DEBUG)  # Log all messages from 'current'

    # Create a console handler
    console_handler = logging.StreamHandler()

    # Set the level of the console handler
    console_handler.setLevel(logging.DEBUG)  # Handle all messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the loggers
    for logger in loggers.values():
        logger.addHandler(console_handler)

    # Profiler
    profiler = cProfile.Profile()
    profiler.enable()

    # endregion

    entity_manager = EntityManager()

    pygame.quit()
    os._exit(0)

if __name__ == "__main__":
    main()