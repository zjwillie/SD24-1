import pygame
#import ctypes

class GameState:
    def __init__(self, resolution = (800, 600)):
        self.exit_requested = False
        self.resolution = resolution
        self.screen = None
        self.clock = None
        self.start_time = None

        self.sound_on = False
        self.volume = 1.0

        self.caption = "ECS SD Build 0.0.4.1"
        self.icon_path = "images/icons/main_icon.png"

        self.loggers = None

        self.initialize_pygame()

    def initialize_pygame(self):
        #ctypes.windll.user32.SetProcessDPIAware()

        pygame.init()

        self.screen = pygame.display.set_mode(self.resolution)

        self.set_caption(self.caption)
        self.set_icon(self.icon_path)

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_icon(self, icon):
        pygame.display.set_icon(pygame.image.load(icon))

def main():
    game_state = GameState()

    print("Game State Initialized")

    while game_state.exit_requested == False:
        current_time = pygame.time.get_ticks()
        if current_time - game_state.start_time >= 1000:
            game_state.exit_requested = True

if __name__ == "__main__":
    main()