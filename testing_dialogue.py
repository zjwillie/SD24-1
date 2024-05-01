import json

from common.components.dialogue_component import DialogueComponent

class WorldFlagsComponent:
    def __init__(self, flags):
        self.flags = flags

    @classmethod
    def from_json(cls, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        return cls(data['flags'])


def main():
    dialogue_component = DialogueComponent.from_json('dialogues/testing/test_template_02.json')

    dialogue_component.print_dialogues()



if __name__ == "__main__":
    main()