import logging
import os

class LoggingManager:
    def __init__(self):
        self.loggers = None
        self.handlers = {}  # Keep track of handlers to switch between them
        self.initialize_logging()

    def initialize_logging(self):
        self.loggers = {
            'entity_manager': logging.getLogger('entity'),
            'event_manager': logging.getLogger('event_manager'),
            'input_manager': logging.getLogger('input_manager'),
            'game_manager': logging.getLogger('game_manager'),
            'component': logging.getLogger('component'),
            'system': logging.getLogger('system'),
            'player_system': logging.getLogger('player_system'),
            'render_system': logging.getLogger('render_system'),
            'current': logging.getLogger('current'),
        }
        for logger_name in self.loggers:
            logger = self.loggers[logger_name]
            logger.setLevel(logging.WARNING if logger_name == 'component' else logging.DEBUG)
            self.handlers[logger_name] = logging.StreamHandler()  # Default to console
            self.setup_handler(self.handlers[logger_name], logger)
            logger.propagate = False

    def getLogger(self, name):
        if name not in self.loggers:
            self.loggers[name] = logging.getLogger(name)
        return self.loggers[name]

    def setup_handler(self, handler, logger):
        # Remove all handlers from the logger
        while logger.hasHandlers():
            logger.removeHandler(logger.handlers[0])

        formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)  # Handle all messages
        logger.addHandler(handler)

    def set_output_to_file(self, logger_name, filename):
        logger = self.loggers.get(logger_name)
        if logger:
            logger.removeHandler(self.handlers[logger_name])  # Remove the previous handler
            file_handler = logging.FileHandler(os.path.join('core', 'logs', filename))
            self.setup_handler(file_handler, logger)
            self.handlers[logger_name] = file_handler  # Update the current handler

    def set_output_to_console(self, logger_name):
        logger = self.loggers.get(logger_name)
        if logger:
            logger.removeHandler(self.handlers[logger_name])  # Remove the previous handler
            console_handler = logging.StreamHandler()
            self.setup_handler(console_handler, logger)
            self.handlers[logger_name] = console_handler  # Update the current handler

    def change_log_level(self, logger_name, new_level):
        if new_level is False:
            new_level = logging.CRITICAL + 1

        logger = self.loggers.get(logger_name)
        if logger:
            logger.setLevel(new_level)

def main():
    logging_manager = LoggingManager()

    # Initial logging to console
    logging_manager.loggers['current'].debug("This message goes to the console.")

    # Switch 'current' logger output to file
    logging_manager.set_output_to_file('current', 'current_log.txt')
    logging_manager.loggers['current'].info("This message goes to the file.")

    # Change 'component' logger level to DEBUG and output to file
    logging_manager.change_log_level('component', logging.DEBUG)
    logging_manager.set_output_to_file('component', 'component_log.txt')
    logging_manager.loggers['component'].debug("Component debug message goes to the file.")

    # Switch 'current' logger output back to console and change level to WARNING
    logging_manager.set_output_to_console('current')
    logging_manager.change_log_level('current', logging.WARNING)
    logging_manager.loggers['current'].debug("This debug message won't appear.")
    logging_manager.loggers['current'].warning("This warning message goes back to the console.")

if __name__ == "__main__":
    main()
