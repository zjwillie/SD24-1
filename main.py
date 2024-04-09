import os
import pygame

from common.managers.game_manager import GameManager

# Debugging
import cProfile
import pstats
 
def main():

    # Flag to run the profiler
    run_profiler = False

    if run_profiler:
        profiler = cProfile.Profile()
        profiler.enable()

#?##############################################################################

    game_manager = GameManager()
    game_manager.intialize_game()

    while game_manager.game_state.exit_requested == False:

        delta_time = game_manager.game_state.clock.tick(60) / 1000.0       
       
        game_manager.update(delta_time)

#?##############################################################################7

    if run_profiler:
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats("cumulative")
        stats.print_stats()

    pygame.quit()
    os._exit(0)

if __name__ == "__main__":
    main() 