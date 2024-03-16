from typing import List, Any

class World:

    def __init__(self, resource_list: List[Any], time_of_day: int):
        self.resource_list = resource_list
        self.time_of_day = time_of_day

class Resource:

    def __init__(self, resource_id: int, resource_position: List[float], resource_radius: float, resource_type_id: int):
        self.resource_id = resource_id
        self.resource_position = resource_position
        self.resource_radius = resource_radius
        self.resource_type_id = resource_type_id







if __name__ == "__main__":
    pass