class Event:
    def __init__(self, event_type, data=None):
        self.type = event_type
        self.data = data
    
    def __str__(self):
        return f"Event: Type({self.type}) Data{self.data} <- EVENT OBJECT"

class EventManager:
    def __init__(self, logger):
        self.logger = logger
        self.logger.change_log_level("event_manager", "OFF")
        
        self.events = []
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)

    def post(self, event):
        self.logger.loggers['event_manager'].info(f"Event Posted:\n Type: {event.type}, Data: {event.data}")
        self.events.append(event)

    def urgent_post(self, event):
        self.logger.loggers['event_manager'].info(f"Urgent Event Posted:\n Type: {event.type}, Data: {event.data}")
        self.events.insert(0, event)

    def critical_post(self, event):
        self.logger.loggers['event_manager'].info(f"Critical Event Posted:\n Type: {event.type}, Data: {event.data}")
        for subscriber in self.subscribers.get(event.type, []):
            subscriber(event)

    def process_events(self):
        while self.events:
            event = self.events.pop(0)
            self.logger.loggers['event_manager'].info(f"Event:\n Type: {event.type}, Data: {event.data}")
            for subscriber in self.subscribers.get(event.type, []):
                subscriber(event)

    def update(self):
        self.process_events()