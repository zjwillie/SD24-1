from components import *

class ComponentFactory:
    def create_component(self, component_name, component_data):
        factory_method = getattr(self, f"create_{component_name}", None)
        if factory_method:
            return factory_method(**component_data)
        raise ValueError(f"Factory method for {component_name} not found")

    def create_UUIDComponent(self, **kwargs):
        return UUIDComponent(**kwargs)

    def create_NameComponent(self, **kwargs):
        return NameComponent(**kwargs)