import sys
import random
sys.path.append("src/maplogic")
from typing import List, Any
from maplogic.StaticResource import StaticResource
from maplogic.DynamicResource import DynamicResource
from maplogic.Grass import Grass

class World:

    def __init__(self):
        self.static_resource_map = {}
        self.dynamic_resource_map = {}

        self.time_of_day = [0,12,0,0] # [day, hour, minute, second] ticks in day = 24*60*6 = 8640

    #TODO: Implement this method
    def update_time_of_day(self) -> None:
        self.time_of_day[3] += 10
        if self.time_of_day[3] >= 60:
            self.time_of_day[3] = 0
            self.time_of_day[2] += 1
        if self.time_of_day[2] >= 60:
            self.time_of_day[2] = 0
            self.time_of_day[1] += 1
        if self.time_of_day[1] >= 24:
            self.time_of_day[1] = 0
            self.time_of_day[0] += 1


    def spawn_resource(self, resource_id: int, resource_radius: float, resource_position: List[Any], resource_type_id: int) -> None:
        resource = StaticResource(resource_id, resource_position, resource_radius, resource_type_id)
        self.static_resource_map[resource_id] = resource
    
    def spawn_grass(self) -> None:

        def get_unique_grass_id() -> int:
            return len(self.dynamic_resource_map) + 1
        
        def get_random_valid_static_resource() -> List[float]:
            valid_points = []
            for resource in self.static_resource_map.values():
                if resource.resource_type_id == 1:
                    valid_points.append(resource)
            return random.choice(valid_points)

        
        resource_id = get_unique_grass_id()
        associated_static_resource = get_random_valid_static_resource()
        resource_position = [random.randint(associated_static_resource.resource_position[0] - associated_static_resource.resource_radius, associated_static_resource.resource_position[0] + associated_static_resource.resource_radius), random.randint(associated_static_resource.resource_position[1] - associated_static_resource.resource_radius, associated_static_resource.resource_position[1] + associated_static_resource.resource_radius)]

        grass = Grass(resource_id, resource_position, self.dynamic_resource_map, associated_static_resource)

        self.dynamic_resource_map[resource_id] = grass

    def update(self) -> None:
        copyofdynamicresourcemap = self.dynamic_resource_map.copy()
        for resource in copyofdynamicresourcemap.values():
            if resource.alive_status:
                resource.update()
            else:
                del self.dynamic_resource_map[resource.resource_id]
        self.update_time_of_day()






if __name__ == "__main__":
    pass