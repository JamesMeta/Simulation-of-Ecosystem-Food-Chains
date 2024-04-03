import sys
import random
import pygame as pg
sys.path.append("src/maplogic")
from typing import List, Any

class GrassPlant():

    def __init__(self, resource_id: int, resource_position: List[float]):
        self.resource_id = resource_id
        self.resource_position = resource_position
        self.alive_status = True
        self.radius = 5
        self.resource_type_id = 1
        self.mass = 0.020

        #Spriteloader variables
        self.sprite = None

    
    # def spawn_grass(self) -> None:

    #     def get_unique_grass_id() -> int:
    #         for i in range(1, len(self.dynamic_resource_map) + 2):
    #             if i not in self.dynamic_resource_map:
    #                 return i

    #     x = random.randint(self.associated_static_resource.resource_position[0] - self.associated_static_resource.resource_radius, self.associated_static_resource.resource_position[0] + self.associated_static_resource.resource_radius)
    #     y = random.randint(self.associated_static_resource.resource_position[1] - self.associated_static_resource.resource_radius, self.associated_static_resource.resource_position[1] + self.associated_static_resource.resource_radius)
    #     position = [x, y]
    #     grass_id = get_unique_grass_id()
    #     new_grass = Grass(grass_id, position, self.dynamic_resource_map, self.associated_static_resource)
    #     self.dynamic_resource_map[grass_id] = new_grass
        
    

    def update(self) -> None:

        # current_capacity = 0
        # for resource in self.dynamic_resource_map.values():
        #     if resource.resource_type_id == 1:
        #         current_capacity += 1

        if self.hp <= 0:
            self.alive_status = False

        # if self.alive_status:
        #     self.current_regen += 1
        #     if current_capacity < self.max_capacity and self.current_regen >= self.regen_rate:
        #         self.current_regen = 0
        #         current_capacity += 1
        #         self.spawn_grass()
        


    #Animal sprite loading handler.
    def load_sprite(self) -> None:
            sprite_filename = f"assets/sprites/grass_sprite.png"
            try:
                self.sprite = pg.image.load(sprite_filename)
            except pg.error:
                print(f"Error loading grass sprite.")
                return




if __name__ == "__main__":
    pass