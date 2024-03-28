class InputManager:
    def __init__(self, loggers):
        self.loggers = loggers

        self.key_down_subscribers = {}
        self.key_up_subscribers = {}