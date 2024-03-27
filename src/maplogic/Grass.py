import sys
import random
sys.path.append("src/maplogic")
from maplogic.DynamicResource import DynamicResource
from typing import List, Any

class Grass(DynamicResource):

    def __init__(self, resource_id: int, resource_position: List[float]):
        super().__init__(resource_id, resource_position, 5, 1)
        self.regen_rate = 100
        self.current_regen = 0
        self.max_capacity = 100
        self.mass = 1
        self.alive = True
    
    def spawn_grass(self) -> None:

        def get_unique_grass_id() -> int:
            return len(self.dynamic_resource_map) + 1

        x = random.randint(self.associated_static_resource.resource_position[0] - self.resource_radius, self.associated_static_resource.resource_position[0] + self.associated_static_resource.resource_radius)
        y = random.randint(self.associated_static_resource.resource_position[1] - self.resource_radius, self.associated_static_resource.resource_position[1] + self.associated_static_resource.resource_radius)
        position = [x, y]
        grass_id = get_unique_grass_id()
        new_grass = Grass(grass_id, position)
        new_grass.set_post_creation_data(self.dynamic_resource_map, self.associated_static_resource)
        self.dynamic_resource_map[grass_id] = new_grass

    def set_post_creation_data(self, dynamic_resource_map, associated_static_resource) -> None:
        self.dynamic_resource_map = dynamic_resource_map
        self.associated_static_resource = associated_static_resource

    

    def update(self) -> None:

        current_capacity = 0
        for resource in self.dynamic_resource_map.values():
            if resource.resource_type_id == 1:
                current_capacity += 1

        if self.mass <= 0:
            self.alive = False

        if self.alive:
            self.current_regen += 1
            if current_capacity < self.max_capacity and self.current_regen >= self.regen_rate:
                self.current_regen = 0
                current_capacity += 1
                self.spawn_grass()
        





if __name__ == "__main__":
    pass