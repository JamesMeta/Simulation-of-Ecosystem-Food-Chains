import sys
sys.path.append("src/maplogic")
from typing import List, Any
from Resource import Resource

class World:

    def __init__(self):
        self.resource_map = {}
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
        resource = Resource(resource_id, resource_position, resource_radius, resource_type_id)
        self.resource_map[resource_id] = resource
    
    def update(self) -> None:
        for resource in self.resource_map.values():
            resource.update()
        self.update_time_of_day()






if __name__ == "__main__":
    pass