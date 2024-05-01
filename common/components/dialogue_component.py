# DialogueComponent.py
import json

from .base_component import Component


class Condition:
    def __init__(self, type, name, operator, value):
        self.type = type
        self.name = name
        self.operator = operator
        self.value = value

    @classmethod
    def from_dict(cls, data):
        return cls(data['type'], data['name'], data['operator'], data['value'])

class Event:
    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.event_data = event_data

    @classmethod
    def from_dict(cls, data):
        return cls(data['event_type'], data['event_data'])

class Text:
    def __init__(self, content, conditions, events):
        self.content = content
        self.conditions = [Condition.from_dict(cond) for cond in conditions]
        self.events = [Event.from_dict(event) for event in events]

    @classmethod
    def from_dict(cls, data):
        return cls(data['content'], data['conditions'], data['events'])

class Response:
    def __init__(self, content, conditions, next_dialogue, events):
        self.content = content
        self.conditions = [Condition.from_dict(cond) for cond in conditions]
        self.next_dialogue = next_dialogue
        self.events = [Event.from_dict(event) for event in events]

    @classmethod
    def from_dict(cls, data):
        conditions = data.get('conditions', [])
        events = data.get('events', [])
        return cls(data['content'], conditions, data.get('next_dialogue'), events)

class Dialogue:
    def __init__(self, dialogue_id, texts, responses, events):
        self.dialogue_id = dialogue_id
        self.texts = [Text.from_dict(text) for text in texts]
        self.responses = [Response.from_dict(response) for response in responses]
        self.events = [Event.from_dict(event) for event in events]

    @classmethod
    def from_dict(cls, dialogue_id, data):
        return cls(dialogue_id, data['text'], data['responses'], data['events'])

class DialogueComponent(Component):
    def __init__(self, dialogue_id):
        with open(dialogue_id, 'r') as dialogue_file:
            dialogue_data = json.load(dialogue_file)
        
        self.dialogue_name = dialogue_data['dialogue_name']
        self.metadata = dialogue_data['metadata']

        self.dialogues = {k: Dialogue.from_dict(k, v) for k, v in dialogue_data.items() if k not in ['dialogue_name', 'metadata']}

        self.current_dialogue = self.dialogues['start']

    def print_dialogues(self):
        for dialogue_name, dialogue in self.dialogues.items():
            print(f"Dialogue Name: {dialogue_name}")
            print("Texts:")
            for text in dialogue.texts:
                print(f"  Content: {text.content}")
                print("  Conditions:")
                for condition in text.conditions:
                    print(f"    Type: {condition.type}, Name: {condition.name}, Operator: {condition.operator}, Value: {condition.value}")
                print("  Events:")
                for event in text.events:
                    print(f"    Event Type: {event.event_type}, Event Data: {event.event_data}")
            print("Responses:")
            for response in dialogue.responses:
                print(f"  Content: {response.content}, Next Dialogue: {response.next_dialogue}")
                print("  Conditions:")
                for condition in response.conditions:
                    print(f"    Type: {condition.type}, Name: {condition.name}, Operator: {condition.operator}, Value: {condition.value}")
                print("  Events:")
                for event in response.events:
                    print(f"    Event Type: {event.event_type}, Event Data: {event.event_data}")
            print("Events:")
            for event in dialogue.events:
                print(f"  Event Type: {event.event_type}, Event Data: {event.event_data}")
            print("\n")