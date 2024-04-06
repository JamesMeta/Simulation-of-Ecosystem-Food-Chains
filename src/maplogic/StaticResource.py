from typing import List

# StaticResource class
# This class is the parent class for all static resources in the simulation
# Static resources are resources that do not move and are not consumed
# Static resources are used to generate dynamic resources and guide the movement of animals
class StaticResource:

    def __init__(self, resource_id: int, resource_position: List[float], resource_radius: float, resource_type_id: int):
        self.resource_id = resource_id
        self.resource_position = resource_position
        self.resource_radius = resource_radius
        self.resource_type_id = resource_type_id
        self.dynamic = False

    def update(self) -> None:
        pass