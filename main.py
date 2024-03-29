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
from common.game_manager import GameManager

# Debugging
import cProfile
import pstats

def main():

    run_profiler = False

    if run_profiler:
        profiler = cProfile.Profile()
        profiler.enable()

#?##############################################################################

    game_manager = GameManager()
    game_manager.test_initialize() #! This is just for testing purposes

    while game_manager.game_state.exit_requested == False:
        game_manager.game_state.clock.tick(60)
        delta_time = game_manager.game_state.clock.get_time()
        game_manager.update(delta_time)

        pygame.display.flip()

#?##############################################################################

    if run_profiler:
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats("cumulative")
        stats.print_stats()

    pygame.quit()
    os._exit(0)

if __name__ == "__main__":
    main()