from typing import List, Any


class StaticResource:

    def __init__(self, resource_id: int, resource_position: List[float], resource_radius: float, resource_type_id: int):
        self.resource_id = resource_id
        self.resource_position = resource_position
        self.resource_radius = resource_radius
        self.resource_type_id = resource_type_id