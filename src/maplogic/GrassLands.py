import sys
import random
sys.path.append("src/maplogic")
from maplogic.StaticResource import StaticResource
from maplogic.GrassPlant import GrassPlant
from typing import List, Any

class GrassLands(StaticResource):

    def __init__(self, resource_id: int, resource_position: List[float], resource_radius: float, resource_type_id: int):
        super().__init__(resource_id, resource_position, resource_radius, resource_type_id)
        self.regen_rate = 50
        self.current_regen = 0
        self.max_capacity = 100
        self.mass = 1
        self.alive_status = True
        self.dynamic_resource_map = {}
        self.screen_resolutions = [1820, 980]

        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()
        self.spawn_grass()

    
    def spawn_grass(self) -> None:

        def get_unique_grass_id() -> int:
            for i in range(1, len(self.dynamic_resource_map) + 2):
                if i not in self.dynamic_resource_map:
                    return i
        x,y = random.randint(self.resource_position[0] - self.resource_radius, self.resource_position[0] + self.resource_radius), random.randint(self.resource_position[1] - self.resource_radius, self.resource_position[1] + self.resource_radius)
        while x < 0 or x > self.screen_resolutions[0] or y < 0 or y > self.screen_resolutions[1]:
            x = random.randint(self.resource_position[0] - self.resource_radius, self.resource_position[0] + self.resource_radius)
            y = random.randint(self.resource_position[1] - self.resource_radius, self.resource_position[1] + self.resource_radius)

        position = [x, y]
        grass_id = get_unique_grass_id()
        new_grass = GrassPlant(grass_id, position)
        self.dynamic_resource_map[grass_id] = new_grass

    def update(self) -> None:

        current_capacity = 0

        for resource in self.dynamic_resource_map.copy().values():
            if resource.alive_status == False:
                del self.dynamic_resource_map[resource.resource_id]
            else:
                current_capacity += 1

        if self.mass <= 0:
            self.alive_status = False

        self.current_regen += 1
        if current_capacity < self.max_capacity and self.current_regen >= self.regen_rate:
            self.current_regen = 0
            current_capacity += 1
            self.spawn_grass()
        





if __name__ == "__main__":
    pass