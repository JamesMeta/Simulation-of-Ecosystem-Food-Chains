import pygame as pg
import random
import os
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
from maplogic.StaticResource import StaticResource
from maplogic.GrassLands import GrassLands
from maplogic.GrassPlant import GrassPlant

from maplogic.HeightMap import generate_resource_map

class Simulation:
    
    def __init__(self):
        #Background is None by default, attribute can be changed to a pygame Image type to be used for predrawn background overlays.
        self.background = None 

        self.screen_x_resolution = 1820
        self.screen_y_resolution = 980

        pg.init()
        self.screen = pg.display.set_mode((self.screen_x_resolution, self.screen_y_resolution))
        self.clock = pg.time.Clock()

        self.organism_map = {}
        self.world = World()

        self.organism_population_over_time = []

        self.debug_mode = True

    #Organism Types: 1 = Fox, 2 = Owl, 3 = Frog, 4 = Snake, 5 = Hawk, 6 = Small Bird, 7 = Rabbit, 8 = Grass Hopper, 9 = Mouse
    def spawn_organism(self, species_id: int) -> None:

        def get_unique_animal_id() -> int:
            return len(self.organism_map) + 1


        x = random.randint(0, self.screen_x_resolution)
        y = random.randint(0, self.screen_y_resolution)
        position = [x, y]
        animal_id = get_unique_animal_id()
        new_organism = None

        if species_id == 1:
            new_organism = Fox(position, animal_id, self.world.static_resource_map, self.organism_map)
        elif species_id == 2:
            new_organism = Owl(position, animal_id, self.world.static_resource_map, self.organism_map)
        elif species_id == 3:
            new_organism = Frog(position, animal_id, self.world.static_resource_map, self.organism_map)
        elif species_id == 4:
            new_organism = Snake(position, animal_id, self.world.static_resource_map, self.organism_map)
        elif species_id == 5:
            new_organism = Hawk(position, animal_id, self.world.static_resource_map, self.organism_map)
        elif species_id == 6:
            new_organism = SmallBird(position, animal_id, self.world.static_resource_map, self.organism_map)
        elif species_id == 7:
            new_organism = Rabbit(position, animal_id, self.world.static_resource_map, self.organism_map)
        elif species_id == 8:
            new_organism = GrassHopper(position, animal_id, self.world.static_resource_map, self.organism_map)
        elif species_id == 9:
            new_organism = Mouse(position, animal_id, self.world.static_resource_map, self.organism_map)
        else:
            print("Invalid Species ID")
        
        self.organism_map[animal_id] = new_organism
        
 
    def update_all_Objects(self) -> None:
        copyof_organism_map = self.organism_map.copy()
        for organism in copyof_organism_map.values():
            organism.update()
        self.world.update()
    
    def draw_all_objects(self) -> None:

        def interpolate_color(color1, color2, ratio):
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            return (r, g, b)
        
        def get_current_color(current_time):

            time_intervals = [(4, (255, 218, 185)),    # Morning
                  (8, (255, 240, 165)),    # Late Morning
                  (12, (173, 216, 230)),    # Afternoon
                  (16, (255, 192, 203)),   # Evening
                  (20, (47, 79, 79))]      # Night

            # Find the current time interval
            for i in range(len(time_intervals) - 1):
                if time_intervals[i][0] <= current_time < time_intervals[i + 1][0]:
                    start_time, start_color = time_intervals[i]
                    end_time, end_color = time_intervals[i + 1]
                    # Calculate ratio of time elapsed in the current interval
                    ratio = (current_time - start_time) / (end_time - start_time)
                    return interpolate_color(start_color, end_color, ratio)

            # If current time is beyond the defined intervals, return last color
            return time_intervals[-1][1]

        time = self.world.time_of_day
        
        self.screen.fill(get_current_color(time[1]))

        if self.debug_mode:
            for resource in self.world.static_resource_map.values():
                if resource.resource_type_id == 1:
                    pg.draw.circle(self.screen, (58, 117, 33), resource.resource_position, resource.resource_radius)
                    for grass_plant in resource.dynamic_resource_map.values():
                        pg.draw.circle(self.screen, (0, 255, 0), grass_plant.resource_position, grass_plant.radius)
                elif resource.resource_type_id == 2:
                    pg.draw.circle(self.screen, (0, 0, 255), resource.resource_position, resource.resource_radius)
                elif resource.resource_type_id == 3:
                    pg.draw.circle(self.screen, (150, 75, 0), resource.resource_position, resource.resource_radius)
                else:
                    print("Invalid Resource Type ID")
        
        for organism in self.organism_map.values():
            pg.draw.circle(self.screen, organism.color, organism.organism_position, organism.radius)
        
        font = pg.font.Font(None, 36)
        text = font.render(f"Day: {self.world.time_of_day[0]} Time: {self.world.time_of_day[1]}:{self.world.time_of_day[2]}:{self.world.time_of_day[3]}", 1, (255, 255, 255))
        self.screen.blit(text, (10, 10))
 
    def test_one(self) -> None:
        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 100, [100, 100], grass)
        self.world.spawn_resource(2, 100, [1720, 880], water)
        self.world.spawn_resource(3, 100, [1720, 100], forest)

        #Spawn 10 of each organism

        #Organism Types: 1 = Fox, 2 = Owl, 3 = Frog, 4 = Snake, 5 = Hawk, 6 = Small Bird, 7 = Rabbit, 8 = Grass Hopper, 9 = Mouse
        for i in range(10):
            self.spawn_organism(1) 

        for i in range(10):
            self.spawn_organism(2) 

        for i in range(10):
            self.spawn_organism(3) 

        for i in range(10):
            self.spawn_organism(4) 

        for i in range(10):
            self.spawn_organism(5) 

        for i in range(10):
            self.spawn_organism(6) 

        for i in range(10):
            self.spawn_organism(7) 

        for i in range(10):
            self.spawn_organism(8) 

        for i in range(10):
            self.spawn_organism(9)
    
    def test_two(self) -> None:
        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [800, 800], grass)
        self.world.spawn_resource(3, 100, [1020, 680], water)
        self.world.spawn_resource(4, 100, [1020, 200], forest)

        #Spawn 1 rabbit
        self.spawn_organism(7)
        self.spawn_organism(7)
        self.spawn_organism(7)
        self.spawn_organism(7)
        self.spawn_organism(7)
        self.spawn_organism(7)


    def test_three(self) -> None:
        #getting biome generation working
        grass = 1
        water = 2
        forest = 3


        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [1020, 680], water)
        self.world.spawn_resource(3, 100, [1020, 200], forest)

        #logic for map generation using a randint from the amount of available biomes
        #mapped into a 2d array
        i=0
        biome_size = 100
        map = generate_resource_map(self.screen_x_resolution, self.screen_y_resolution)
        for x in range(0, self.screen_x_resolution, biome_size):
            for y in range(0, self.screen_y_resolution, biome_size):
                self.world.spawn_resource(i, biome_size/2, [x, y], map[x][y])
                i+=1


        self.spawn_organism(7)
        self.spawn_organism(7)
        self.spawn_organism(7)
        self.spawn_organism(7)
        

    def test_four(self) -> None:
        #sprite rendering
        grass = 1
        water = 2
        forest = 3
        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [1020, 680], water)
        self.world.spawn_resource(3, 100, [1020, 200], forest)

        self.background = pg.image.load(os.path.join("assets", "map", "land1.png"))
        self.background = pg.transform.scale(self.background, (self.screen_x_resolution, self.screen_y_resolution))


        
    def run_simulation(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            self.update_all_Objects()
            self.draw_all_objects()
            pg.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    
    sim = Simulation()
    sim.test_two()
    sim.run_simulation()


    

    