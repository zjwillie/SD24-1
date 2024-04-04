from common.components.cameraanchor_component import CameraAnchorComponent
from common.components.id_component import IDComponent
from common.components.images_component import ImagesComponent
from common.components.menubutton_component import MenuButtonComponent
from common.components.menu_component import MenuComponent
from common.components.menuselector_component import MenuSelectorComponent
from common.components.name_component import NameComponent
from common.components.player_component import PlayerComponent
from common.components.position_component import PositionComponent
from common.components.render_component import RenderComponent
from common.components.type_component import TypeComponent
from common.components.uuid_component import UUIDComponent

class ComponentFactory:
    def __init__(self):
        self.component_classes = {
            'CameraAnchorComponent': CameraAnchorComponent,
            'IDComponent': IDComponent,
            'ImagesComponent': ImagesComponent,
            'MenuButtonComponent': MenuButtonComponent,
            'MenuComponent': MenuComponent,
            'MenuSelectorComponent': MenuSelectorComponent,
            'NameComponent': NameComponent,
            'PlayerComponent': PlayerComponent,
            'PositionComponent': PositionComponent,
            'RenderComponent': RenderComponent,
            'TypeComponent': TypeComponent,
            'UUIDComponent': UUIDComponent,
        }

    def create_component(self, component_name, component_data):
        component_class = self.component_classes.get(component_name)
        if component_class:
            try:
                return component_class(**component_data)
            except ValueError:
                print(f"CRITICAL: Error: {component_name} constructor raised a ValueError. Check the keys in component_data.")
                return None
        else:
            print(f"Error: Component class for {component_name} not found in component_classes.")
            return None