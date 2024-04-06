import pygame as pg
from typing import List

class GrassPlant():

    def __init__(self, resource_id: int, resource_position: List[float]):
        self.resource_id = resource_id
        self.resource_position = resource_position
        self.alive_status = True
        self.radius = 5
        self.resource_type_id = 1
        self.species_id = -1
        self.mass = 0.020

        #Spriteloader variables
        self.sprite = None

    def update(self) -> None:

        #Check if the grass plant has been eaten completely
        if self.mass <= 0:
            self.alive_status = False
        
    #function will be used by other classes to remove eaten grass from the map
    def die(self, cause_of_death) -> None:
        self.alive_status = False


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