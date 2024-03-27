import typing
from components import *

class EntityManager:
    def __init__(self):
        self.next_enity_id = 0

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

        #if component_type == PlayerComponent:
            #self.player_ID = entity_id

        self.component_maps.setdefault(component_type, {})[entity_id] = component

        self.notify_subscribers(component_type, entity_id, component, "add")

    def notify_subscribers(self, component_type: typing.Type[Component], entity_id: int, component: Component, action: str) -> None:
        for callback in self.subscriptions.get(component_type, []):
            callback(entity_id, component, action)

    def get_component(self, entity_id: int, component_type: typing.Type[Component]) -> typing.Optional[Component]:
        return self.component_maps.get(component_type, {}).get(entity_id, None)


def main():
    entity_manager = EntityManager()

    test_entity = entity_manager.create_entity([
        NameComponent("Player"), 
        UUIDComponent()
        ])

    print(entity_manager.get_component(test_entity, UUIDComponent).uuid)
    print(entity_manager.get_component(test_entity, NameComponent).name)

if __name__ == "__main__":
    main()