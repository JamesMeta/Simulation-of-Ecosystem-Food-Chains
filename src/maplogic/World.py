import sys
sys.path.append("src/maplogic")
from typing import List, Any
from Resource import Resource

class World:

    def __init__(self):
        self.resource_map = {}
        self.time_of_day = 0

    #TODO: Implement this method
    def update_time_of_day(self) -> None:
        pass

    def spawn_resource(self, resource_id: int, resource_radius: float, resource_position: List[Any], resource_type_id: int) -> None:
        resource = Resource(resource_id, resource_position, resource_radius, resource_type_id)
        self.resource_map[resource_id] = resource
        






if __name__ == "__main__":
    pass