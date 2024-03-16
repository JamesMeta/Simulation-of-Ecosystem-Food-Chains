from World import Resource
from typing import List, Any

class Grass(Resource):

    def __init__(self, resource_id: int, resource_position: List[float], resource_radius: float, resource_type_id: int, regen_rate: float, grass_list: List[Any] ,max_capacity: int):
        super().__init__(resource_id, resource_position, resource_radius, resource_type_id)
        self.regen_rate = regen_rate
        self.grass_list = grass_list
        self.max_capacity = max_capacity
        self.current_capacity = len(grass_list)
    
    ## TODO: Implement this method, May have to change design of how grass is implemented as an organism, might just be a resource instead of an organism
    def spawn_grass(self, grass_list: List[Any]) -> None:
        pass





if __name__ == "__main__":
    pass