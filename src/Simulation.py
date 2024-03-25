import pygame as pg
from typing import List, Any
from organism import Organism
from organism.animal import Animal
from organism.animal.carnivor import Carnivor
from organism.animal.herbivor import Herbivor
from organism.animal.carnivor.carnivors.Fox import Fox
from organism.animal.carnivor.carnivors.Owl import Owl
from organism.animal.carnivor.carnivors.Frog import Frog
from organism.animal.carnivor.carnivors.Snake import Snake
from organism.animal.carnivor.carnivors.Hawk import Hawk
from organism.animal.carnivor.carnivors.SmallBird import SmallBird
from organism.animal.herbivor.herbivors.Rabbit import Rabbit
from organism.animal.herbivor.herbivors.GrassHopper import GrassHopper
from organism.animal.herbivor.herbivors.Mouse import Mouse
from maplogic.World import World
from maplogic.Resource import Resource
from maplogic.Grass import Grass


class Simulation:
    
    def __init__(self):

        pg.init()
        self.screen = pg.display.set_mode((1820, 980))
        self.clock = pg.time.Clock()

        self.organism_map = {}
        self.world = World()

        self.organism_population_over_time = []

        self.debug_mode = True

    #Organism Types: 1 = Fox 2 = Owl 3 = Frog 4 = Snake 5 = Hawk 6 = Small Bird 7 = Rabbit 8 = Grass Hopper 9 = Mouse
    def spawn_organisms(self, organism_type: int) -> None:
        pass

    #Resource IDs: 1 = Grass, 2 = Water, 3 = Forest
    def spawn_resources(self, resource_id: int, resource_radius: float, resource_position: List[Any], resource_type_id: int) -> None:
        self.world.spawn_resource(resource_id, resource_radius, resource_position, resource_type_id)

    def update_all_Objects(self) -> None:
        for organism in self.organism_map.values():
            organism.update()

    def draw_all_objects(self) -> None:

        if self.debug_mode:
            for resource in self.world.resource_map.values():
                if resource.resource_type_id == 1:
                    pg.draw.circle(self.screen, (58, 117, 33), resource.resource_position, resource.resource_radius)
                elif resource.resource_type_id == 2:
                    pg.draw.circle(self.screen, (0, 0, 255), resource.resource_position, resource.resource_radius)
                elif resource.resource_type_id == 3:
                    pg.draw.circle(self.screen, (150, 75, 0), resource.resource_position, resource.resource_radius)
                else:
                    print("Invalid Resource Type ID")
        
        for organism in self.organism_map.values():
            pg.draw.circle(self.screen, "red", organism.position, 5)

    def test_one(self) -> None:
        grass = 1
        water = 2
        forest = 3

        self.spawn_resources(1, 100, [100, 100], grass)
        self.spawn_resources(2, 100, [1720, 880], water)
        self.spawn_resources(3, 100, [1720, 100], forest)

    def run_simulation(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False


            self.screen.fill((141, 240, 98))
            self.draw_all_objects()
            pg.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    
    sim = Simulation()
    sim.test_one()
    sim.run_simulation()


    

    