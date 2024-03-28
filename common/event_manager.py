class Event:
    def __init__(self, type, data=None):
        self.type = type
        self.data = data
    
    def __str__(self):
        return f"Event: Type({self.type}) Data({self.data}) <- EVENT OBJECT"

class EventManager:
    def __init__(self, loggers):
        self.events = []
        self.subscribers = {}

        self.loggers = loggers

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)

    def post(self, event):
        self.events.append(event)
        for subscriber in self.subscribers.get(event.type, []):
            subscriber(event)

    def process_events(self, troubleshooting=False):
        while self.events:
            event = self.events.pop(0)
            print(f"Event:\n Type: {event.type}, Data: {event.data}") if troubleshooting else None
            for subscriber in self.subscribers.get(event.type, []):
                subscriber(event)