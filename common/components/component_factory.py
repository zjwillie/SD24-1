# Component factory

from common.components.acceleration_component import AccelerationComponent
from common.components.animation_component import AnimationComponent
from common.components.cameraanchor_component import CameraAnchorComponent
from common.components.camera_component import CameraComponent
from common.components.collision_component import CollisionComponent
from common.components.control_component import ControlComponent
from common.components.dashing_component import DashingComponent
from common.components.description_component import DescriptionComponent
from common.components.directionmoving_component import DirectionMovingComponent
from common.components.directionfacing_component import DirectionFacingComponent
from common.components.entitystatus_component import EntityStatusComponent
from common.components.focuspoint_component import FocusPointComponent
from common.components.font_component import FontComponent
from common.components.id_component import IDComponent
from common.components.image_component import ImageComponent
from common.components.menubutton_component import MenuButtonComponent
from common.components.menu_component import MenuComponent
from common.components.menuselector_component import MenuSelectorComponent
from common.components.name_component import NameComponent
from common.components.player_component import PlayerComponent
from common.components.position_component import PositionComponent
from common.components.render_component import RenderComponent
from common.components.size_component import SizeComponent
from common.components.type_component import TypeComponent
from common.components.uuid_component import UUIDComponent
from common.components.velocity_component import VelocityComponent

class ComponentFactory:
    def __init__(self):
        self.component_classes = {
            'AccelerationComponent': AccelerationComponent,
            'AnimationComponent': AnimationComponent,
            'CameraAnchorComponent': CameraAnchorComponent,
            'CameraComponent': CameraComponent,
            'CollisionComponent': CollisionComponent,
            'ControlComponent': ControlComponent,
            'DashingComponent': DashingComponent,
            'DescriptionComponent': DescriptionComponent,
            'DirectionMovingComponent': DirectionMovingComponent,
            'DirectionFacingComponent': DirectionFacingComponent,
            'EntityStatusComponent': EntityStatusComponent,
            'FocusPointComponent': FocusPointComponent,
            'FontComponent': FontComponent,
            'IDComponent': IDComponent,
            'ImageComponent': ImageComponent,
            'MenuButtonComponent': MenuButtonComponent,
            'MenuComponent': MenuComponent,
            'MenuSelectorComponent': MenuSelectorComponent,
            'NameComponent': NameComponent,
            'PlayerComponent': PlayerComponent,
            'PositionComponent': PositionComponent,
            'RenderComponent': RenderComponent,
            'SizeComponent': SizeComponent,
            'TypeComponent': TypeComponent,
            'UUIDComponent': UUIDComponent,
            'VelocityComponent': VelocityComponent
        }

    def create_component(self, component_name, component_data):
        component_class = self.component_classes.get(component_name)
        if component_class:
            try:
                return component_class(**component_data)
            except ValueError:
                print(f"CRITICAL: 'component_factory.py' Error: {component_name} constructor raised a ValueError. Check the keys in component_data.")
                return None
        else:
            print(f"EXCEPTION: 'component_factory.py' Component class for {component_name} not found in component_classes.")
            return None