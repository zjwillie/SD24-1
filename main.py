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

    game_manager = GameManager()

    if run_profiler:
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats("cumulative")
        stats.print_stats()

    pygame.quit()
    os._exit(0)

if __name__ == "__main__":
    main()