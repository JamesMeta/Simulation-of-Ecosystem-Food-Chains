import pygame as pg
from typing import List, Any
from organism import Organism
from organism.animal import Animal
from organism.animal.carnivor import Carnivor
from organism.animal.herbivor import Herbivor
from organism.animal.carnivor.carnivors import Fox, Owl, SmallBird, Hawk, Snake, Frog
from organism.animal.herbivor.herbivors import Rabbit, GrassHopper, Mouse 
from maplogic import World
from maplogic import Resource
from maplogic import Grass


class Simulation:
    
    def __init__(self):

        pg.init()
        self.screen = pg.display.set_mode((1920, 1080))
        self.clock = pg.time.Clock()

    def spawn_organisms(self, organism_list: List[Any]) -> None:
        pass

    def spawn_resources(self, resource_list: List[Any]) -> None:
        pass

    def update_all_Objects(self) -> None:
        pass

    def run_simulation(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False


            self.screen.fill((0, 0, 0))
            pg.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    
    # sim = Simulation()
    # sim.run_simulation()
    fox = Fox.Fox(1, True, 0.0, [0.0, 0.0], 1, 0.0, 100.0, 0.0, 100.0, 1.0, 1.0, 0.0, 100.0, 1.0, 1.0, 1.0, 1, 1.0, False, False, False, [1, 2, 3], [1, 2, 3], [1, 2, 3], 1)

    

    