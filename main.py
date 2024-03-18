import os
import pygame
import time

class NameComponent:
    def __init__(self, name):
        self.name = name

def main():
    # Initialize pygame
    pygame.init()

    # create a screen
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)

    # Set the title of the window
    pygame.display.set_caption("Somebody's Dream Build 0.0.4")

    icon = pygame.image.load("images/icons/main_icon.png")
    pygame.display.set_icon(icon)

    # Set up clock
    clock = pygame.time.Clock()
    start_time = time.time()


    pygame.quit()
    os._exit(0)

if __name__ == "__main__":
    main()