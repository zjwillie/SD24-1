import typing
import os
import sys

# Adjusting the path temporarily if the module is run as the main script
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.components.base_component import Component
from common.components.component_factory import ComponentFactory

from common.components.acceleration_component import AccelerationComponent
from common.components.animation_component import AnimationComponent
from common.components.camera_component import CameraComponent
from common.components.collision_component import CollisionComponent
from common.components.image_component import ImageComponent
from common.components.name_component import NameComponent
from common.components.menu_component import MenuComponent
from common.components.position_component import PositionComponent
from common.components.player_component import PlayerComponent
from common.components.render_component import RenderComponent
from common.components.uuid_component import UUIDComponent
from common.components.velocity_component import VelocityComponent


from support.utils import get_JSON_data

class EntityManager:
    def __init__(self, logger):
        self.logger = logger

        self.next_enity_id = 0
        self.factory = ComponentFactory()

        self.player_ID = None
        self.entity_with_camera = None

        self.entities = {}
        
        self.entities_to_render = set()
        self.entities_with_animation = set()
        self.entities_with_image = set()
        self.entities_with_position = set()
        self.entities_with_collision = set()
        self.entities_with_velocity = set()
        self.entities_with_acceleration = set()

        self.menu_entities = set()

        self.component_maps = {}

        self.subscriptions = {}

        self.subscribe_to_component(AccelerationComponent, self.acceleration_component_callback)
        self.subscribe_to_component(AnimationComponent, self.animation_component_callback)
        self.subscribe_to_component(CollisionComponent, self.collision_component_callback)
        self.subscribe_to_component(ImageComponent, self.image_component_callback)
        self.subscribe_to_component(MenuComponent, self.menu_component_callback)
        self.subscribe_to_component(PlayerComponent, self.player_component_callback)
        self.subscribe_to_component(PositionComponent, self.position_component_callback)
        self.subscribe_to_component(RenderComponent, self.render_component_callback)
        self.subscribe_to_component(VelocityComponent, self.velocity_component_callback)

    def collision_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} to entities with collision.")
            self.entities_with_collision.add(entity_id)
        elif action == "remove":
            self.logger.loggers["entity_manager"].info(f"Removing entity {entity_id} from entities with collision.")
            self.entities_with_collision.remove(entity_id)

    def velocity_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} to entities with velocity.")
            self.entities_with_velocity.add(entity_id)
        elif action == "remove":
            self.logger.loggers["entity_manager"].info(f"Removing entity {entity_id} from entities with velocity.")
            self.entities_with_velocity.remove(entity_id)

    def acceleration_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} to entities with acceleration.")
            self.entities_with_acceleration.add(entity_id)
        elif action == "remove":
            self.logger.loggers["entity_manager"].info(f"Removing entity {entity_id} from entities with acceleration.")
            self.entities_with_acceleration.remove(entity_id)

    def position_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} to entities with position.")
            self.entities_with_position.add(entity_id)
        elif action == "remove":
            self.logger.loggers["entity_manager"].info(f"Removing entity {entity_id} from entities with position.")
            self.entities_with_position.remove(entity_id)

    def animation_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} to entities with animation.")
            self.entities_with_animation.add(entity_id)
        elif action == "remove":
            self.logger.loggers["entity_manager"].info(f"Removing entity {entity_id} from entities with animation.")
            self.entities_with_animation.remove(entity_id)

    def image_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} to entities with images.")
            self.entities_with_image.add(entity_id)
        elif action == "remove":
            self.entities_with_image.remove(entity_id)

    def menu_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} to menu entities.")
            self.menu_entities.add(entity_id)
        elif action == "remove":
            self.logger.loggers["entity_manager"].info(f"Removing entity {entity_id} from menu entities.")
            self.menu_entities.remove(entity_id)

    def player_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} as player.")
            self.player_ID = entity_id
        elif action == "remove":
            self.logger.loggers["entity_manager"].info(f"Removing entity {entity_id} as player and setting player_ID to None.")
            self.player_ID = None

    def render_component_callback(self, entity_id: int, component: Component, action: str):
        if action == "add":
            self.logger.loggers["entity_manager"].info(f"Adding entity {entity_id} to render list.")
            self.entities_to_render.add(entity_id)
        elif action == "remove":
            self.entities_to_render.remove(entity_id)

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
    
    def remove_component(self, entity_id: int, component_type: typing.Type[Component]):
        component = self.component_maps.get(component_type, {}).pop(entity_id, None)

        if component:
            self.notify_subscribers(component_type, entity_id, component, "remove")

    def notify_subscribers(self, component_type: typing.Type[Component], entity_id: int, component: Component, action: str) -> None:
        for callback in self.subscriptions.get(component_type, []):
            callback(entity_id, component, action)

    def subscribe_to_component(self, component_type: typing.Type[Component], callback: typing.Callable):
        self.subscriptions.setdefault(component_type, []).append(callback)

    def get_component(self, entity_id: int, component_type: typing.Type[Component]) -> typing.Optional[Component]:
        return self.component_maps.get(component_type, {}).get(entity_id, None)

    def get_entity_by_name(self, name: str) -> typing.Optional[int]:
        for entity_id, component in self.component_maps.get(NameComponent, {}).items():
            if component.name == name:
                return entity_id
        return None

    def has_component(self, entity_id: int, component_type: typing.Type[Component]) -> bool:
        return entity_id in self.component_maps.get(component_type, {})

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
    
    def create_world_entities(self, world_entities: dict):
        entities = []
        for entity_JSON in world_entities:
            new_entity = self.create_entity_from_JSON(entity_JSON)
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