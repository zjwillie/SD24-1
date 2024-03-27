import os

def create_component(component_name):
    # Convert to snake_case for filenames
    file_name = ''.join(['_' + i.lower() if i.isupper() else i for i in component_name]).lstrip('_') + '.py'

    # Path to the new component module
    component_path = os.path.join('components', file_name)

    # Create the component module file
    with open(component_path, 'w') as f:
        f.write(f"""# {component_name}.py

from .base_component import BaseComponent

class {component_name}(BaseComponent):
    def __init__(self):
        super().__init__()
        # Component initialization

""")

    # Update the component factory
    factory_path = os.path.join('components', 'component_factory.py')
    with open(factory_path, 'a') as f:
        f.write(f"""

    def create_{component_name.lower()}(self, **kwargs):
        return {component_name}(**kwargs)
""")

    print(f"Component {component_name} created and added to the factory.")

# Example usage
create_component('NewComponent')
