from common.components.name_component import NameComponent
from common.components.uuid_component import UUIDComponent
from common.components.id_component import IDComponent
from common.components.type_component import TypeComponent
from common.components.player_component import PlayerComponent

class ComponentFactory:
    def __init__(self):
        self.component_classes = {
            'NameComponent': NameComponent,
            'UUIDComponent': UUIDComponent,
            'IDComponent': IDComponent,
            'TypeComponent': TypeComponent,
            'PlayerComponent': PlayerComponent
        }

    def create_component(self, component_name, component_data):
        component_class = self.component_classes.get(component_name)
        if component_class:
            try:
                return component_class(**component_data)
            except ValueError:
                print(f"Error: Factory method for {component_name} not found. Skipping this component.")
                return None
        else:
            print(f"Error: Factory method for {component_name} not found. Skipping this component.")
            return None