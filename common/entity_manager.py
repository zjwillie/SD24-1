import typing
import os
import sys

# Adjusting the path temporarily if the module is run as the main script
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.components import *
from core.utils import get_JSON_data

class EntityManager:
    def __init__(self, logger):
        self.logger = logger

        self.next_enity_id = 0
        self.factory = ComponentFactory()

        self.player_ID = None

        self.entities = {}

        self.component_maps = {}

        self.subscriptions = {}

    def create_entity(self, components: typing.List[typing.Any] = []):
        entity_id = self.next_enity_id
        self.next_enity_id += 1

        self.entities[entity_id] = entity_id

        for component in components:
            self.add_component(entity_id, component)

        return entity_id

    def add_component(self, entity_id: int, component: typing.Any):
        component_type = type(component)

        if component_type == PlayerComponent:
            self.player_ID = entity_id

        self.component_maps.setdefault(component_type, {})[entity_id] = component

        self.notify_subscribers(component_type, entity_id, component, "add")

    def notify_subscribers(self, component_type: typing.Type[Component], entity_id: int, component: Component, action: str) -> None:
        for callback in self.subscriptions.get(component_type, []):
            callback(entity_id, component, action)

    def get_component(self, entity_id: int, component_type: typing.Type[Component]) -> typing.Optional[Component]:
        return self.component_maps.get(component_type, {}).get(entity_id, None)

    def create_entity_from_dict(self, entity_dict: dict):
        entity_id = self.next_enity_id
        self.next_enity_id += 1

        self.entities[entity_id] = entity_id

        for component_type, component_data in entity_dict.items():
            component = self.factory.create_component(component_type, component_data)
            self.add_component(entity_id, component)

        return entity_id
    
    def create_entity_from_JSON(self, entity_json: str):
        entity_dict = get_JSON_data(entity_json)
        return self.create_entity_from_dict(entity_dict)
    
    def create_world_entities(self, world_json: str):
        entities = []
        world_dict = get_JSON_data(world_json)
        for entity_json in world_dict["entities"]:
            new_entity = self.create_entity_from_JSON(entity_json)
            entities.append(new_entity)
        return entities

def main():
    entity_manager = EntityManager()

    test_entity = entity_manager.create_entity([
        NameComponent("Player"), 
        UUIDComponent()
        ])
    
    test_dict = {
        "NameComponent": {
            "name": "Player 2"
        },
        "UUIDComponent": {}
    }
    test_dict_entity = entity_manager.create_entity_from_dict(test_dict)

    test_json = "common/test_json_entity.json"
    test_json_entity = entity_manager.create_entity_from_JSON(test_json)

    test_world_json = "common/test_world.json"
    world_entities = entity_manager.create_world_entities(test_world_json)

    print("Test Entity:")
    print(entity_manager.get_component(test_entity, NameComponent).name)
    print(entity_manager.get_component(test_entity, UUIDComponent).uuid)
    print("")
    print("Test Dict Entity:")
    print(entity_manager.get_component(test_dict_entity, NameComponent).name)
    print(entity_manager.get_component(test_dict_entity, UUIDComponent).uuid)
    print("")
    print("Test JSON Entity:")
    print(entity_manager.get_component(test_json_entity, NameComponent).name)
    print(entity_manager.get_component(test_json_entity, UUIDComponent).uuid)
    print("Test World Entities:")
    for i, entity in enumerate(world_entities):
        print(f"Entity {i}:")
        print(entity_manager.get_component(entity, NameComponent).name)
        print(entity_manager.get_component(entity, UUIDComponent).uuid)


if __name__ == "__main__":
    main()