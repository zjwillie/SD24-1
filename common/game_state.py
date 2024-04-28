import pygame
#import ctypes

class GameState:
    def __init__(self, resolution = (800, 600)):
        self.exit_requested = False
        self.pause_requested = False

        self.resolution = resolution
        self.screen = None
        self.clock = None
        self.start_time = None

        self.sound_on = False
        self.volume = 1.0

        self.caption = "ECS SD Build 0.0.4.3"
        self.icon_path = "images/icons/main_icon.png"

        self.joystick_active = False

        self.loggers = None

        self.world_data = None

        self.initialize_game()

    def initialize_game(self):
        #ctypes.windll.user32.SetProcessDPIAware()

        pygame.init()

        self.world_data = None

        self.screen = pygame.display.set_mode(self.resolution)
        self.world_size = None

        self.set_caption(self.caption)
        self.set_icon(self.icon_path)

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        self.activate_joysticks()

    def activate_joysticks(self):
        # check for joysticks
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.joystick_active = True
        else:
            self.joystick = None

    def deactivate_joysticks(self):
        if self.joystick:
            self.joystick.quit()
            self.joystick_active = False
            self.joystick = None

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_icon(self, icon):
        pygame.display.set_icon(pygame.image.load(icon))

    def set_world_data(self, world_data):
        self.world_data = world_data
        if "world" in self.world_data:
            self.world_size = tuple((self.world_data["world"]["width"], self.world_data["world"]["height"]))

def main():
    game_state = GameState()

    print("Game State Initialized")

    while game_state.exit_requested == False:
        current_time = pygame.time.get_ticks()
        if current_time - game_state.start_time >= 1000:
            game_state.exit_requested = True

if __name__ == "__main__":
    main()