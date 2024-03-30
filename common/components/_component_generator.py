import os

def create_component(component_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Create filename in snake_case
    file_name = component_name.lower() + '_component.py'

    # Create class name in CamelCase
    class_name = component_name + 'Component'

    # Path to the new component module
    component_path = os.path.join(script_dir, file_name)

    # Create the component module file
    with open(component_path, 'w') as f:
        f.write(f"""# {class_name}.py

from .base_component import Component

class {class_name}(Component):
    def __init__(self):
        super().__init__()
        # Component initialization

""")

    # Update the component factory
    factory_path = os.path.join(script_dir, 'component_factory.py')
    with open(factory_path, 'a') as f:
        f.write(f"""

    def create_{class_name}(self, **kwargs):
        return {class_name}(**kwargs)
""")

    # Update __init__.py
    init_path = os.path.join(script_dir, '__init__.py')
    with open(init_path, 'a') as f:
        f.write(f"\nfrom .{file_name.replace('.py', '')} import {class_name}")

    print(f"Component {class_name} created and added to the factory.")

# Example usage
create_component('Type')