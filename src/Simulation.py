#import all necessary libraries and classes
import pygame as pg
import random
import math
import matplotlib.pyplot as plt
import os

from typing import List, Any
from organism import Organism
from organism.utility import Utility
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

        self.current_day = 1
        self.end_day = 100
        self.predator_prey_test = False

        self.organism_population_over_time = {
            "Grass": []
        }

        self.extinction_timers = {}

        self.debug_mode = True

    def draw_all_objects(self) -> None:
        
        self.screen.fill((190,214,197))

        # If-else for debugging. Will always toggle sprites off/on.
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

                if isinstance(organism, Utility):
                    continue

                if not organism.hidden:
                    pg.draw.circle(self.screen, organism.color, organism.organism_position, organism.radius)   
        else:
            #   This code will ALWAYS display the same map if debug mode is off, 
            #   the sprite is independant of the fields used for reasource identification. 
            #   Either fix this later or ship it with activation only for a single map.
            self.screen.blit(pg.transform.scale(pg.image.load(f"assets/map/land2.jpg"), (self.screen_x_resolution, self.screen_y_resolution)), (0,0))
            for organism in self.organism_map.values():

                if isinstance(organism, Utility):
                    continue

                organism.load_sprite()
                self.screen.blit(organism.sprite, organism.organism_position)
            for resource in self.world.static_resource_map.values():
                if resource.resource_type_id == 1:
                    for grass_plant in resource.dynamic_resource_map.values():
                        grass_plant.load_sprite()
                        self.screen.blit(grass_plant.sprite, grass_plant.resource_position)
        
        font = pg.font.Font(None, 36)
        text = font.render(f"Year: {self.world.time_of_day[0]}", 1, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def log_population(self) -> None:
        fox_count, owl_count, frog_count, snake_count, hawk_count, small_bird_count, rabbit_count, grass_hopper_count, mouse_count, grass_count = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        for organism in self.organism_map.values():
            if isinstance(organism, Fox):
                fox_count += 1
            elif isinstance(organism, Owl):
                owl_count += 1
            elif isinstance(organism, Frog):
                frog_count += 1
            elif isinstance(organism, Snake):
                snake_count += 1
            elif isinstance(organism, Hawk):
                hawk_count += 1
            elif isinstance(organism, SmallBird):
                small_bird_count += 1
            elif isinstance(organism, Rabbit):
                rabbit_count += 1
            elif isinstance(organism, GrassHopper):
                grass_hopper_count += 1
            elif isinstance(organism, Mouse):
                mouse_count += 1

        for resource in self.world.static_resource_map.values():
            if resource.resource_type_id == 1:
                grass_count += len(resource.dynamic_resource_map)

        if "Fox" in self.organism_population_over_time or fox_count > 0:
            self.organism_population_over_time["Fox"].append(fox_count)
        if "Owl" in self.organism_population_over_time or owl_count > 0:
            self.organism_population_over_time["Owl"].append(owl_count)
        if "Frog" in self.organism_population_over_time or frog_count > 0:
            self.organism_population_over_time["Frog"].append(frog_count)
        if "Snake" in self.organism_population_over_time or snake_count > 0:
            self.organism_population_over_time["Snake"].append(snake_count)
        if "Hawk" in self.organism_population_over_time or hawk_count > 0:
            self.organism_population_over_time["Hawk"].append(hawk_count)
        if "Small Bird" in self.organism_population_over_time or small_bird_count > 0:
            self.organism_population_over_time["Small Bird"].append(small_bird_count)
        if "Rabbit" in self.organism_population_over_time or rabbit_count > 0:
            self.organism_population_over_time["Rabbit"].append(rabbit_count)
        if "Grass Hopper" in self.organism_population_over_time or grass_hopper_count > 0:
            self.organism_population_over_time["Grass Hopper"].append(grass_hopper_count)
        if "Mouse" in self.organism_population_over_time or mouse_count > 0:
            self.organism_population_over_time["Mouse"].append(mouse_count)
        if "Grass" in self.organism_population_over_time or grass_count > 0:
            self.organism_population_over_time["Grass"].append(grass_count)

        for species, population in self.organism_population_over_time.items():
            if len(population) >= 2:
                print(f"{species} Saw a {population[-1] - population[-2]} Change in Population")
        

    
    def plot_population(self) -> None:
        
        plt.figure(figsize=(10, 5))
        for species, population in self.organism_population_over_time.items():
            plt.plot(population, label=species)
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.title("Population Over Time")
        plt.legend()
        plt.show()

        #plot without grass
        plt.figure(figsize=(10, 5))
        for species, population in self.organism_population_over_time.items():
            if species != "Grass":
                plt.plot(population, label=species)
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.title("Population Over Time (Excluding Grass)")
        plt.legend()
        plt.show()

        #plot grass, sum of herbivors, and sum of carnivors


        total_sum_producers = 0
        total_sum_primary_consumers = 0
        total_sum_secondary_consumers = 0
        total_sum_tertiary_consumers = 0

        for resource in self.world.static_resource_map.values():
            if resource.resource_type_id == 1:
                total_sum_producers += resource.lifetime_population

        for keys, values in self.organism_population_over_time.items():
            
            if keys == "Grass":
                pass
            elif keys == "Grass Hopper" or keys == "Mouse" or keys == "Rabbit":
                total_sum_primary_consumers += sum(values)
            elif keys == "Small Bird" or keys == "Frog" or keys == "Snake":
                total_sum_secondary_consumers += sum(values)
            elif keys == "Fox" or keys == "Owl" or keys == "Hawk":
                total_sum_tertiary_consumers += sum(values)

            
        colors = ['blue', 'green', 'red', 'purple']
        labels = ['Producers', 'Primary Consumers', 'Secondary Consumers', 'Tertiary Consumers']
        values = [total_sum_producers, total_sum_primary_consumers, total_sum_secondary_consumers, total_sum_tertiary_consumers]
        plt.bar(labels, values, color=colors)
        plt.xlabel("Population Type")
        plt.ylabel("Population")
        plt.title("Population Total Over 10 Years (By Trophic Level)")
        plt.yscale('log')
        plt.show()
        
        #plot utility cause of deaths
        utility = self.organism_map["utility"]
        deaths = utility.count_deaths
        labels = deaths.keys()
        values = deaths.values()
        plt.figure(figsize=(10, 5))
        plt.bar(labels, values)
        plt.xlabel("Cause of Death")
        plt.ylabel("Number of Deaths")
        plt.title("Utility Cause of Deaths")
        plt.show()

    #Organism Types: 1 = Fox, 2 = Owl, 3 = Frog, 4 = Snake, 5 = Hawk, 6 = Small Bird, 7 = Rabbit, 8 = Grass Hopper, 9 = Mouse, 10 = Utility
    def spawn_organism(self, species_id: int) -> None:

        #utility class is a special class that is used to track the cause of death for all organisms
        #it is not a real organism and is not displayed on the screen
        #it is embedded into the organism map so that it can be accessed by all organisms to report their cause of death
        if species_id == 10:
            utility = Utility(self.organism_map)
            self.organism_map["utility"] = utility
            return

        def get_unique_animal_id() -> int:
            return len(self.organism_map) + 1

        x = random.randint(0, self.screen_x_resolution)
        y = random.randint(0, self.screen_y_resolution)
        position = [x, y]
        animal_id = get_unique_animal_id()
        new_organism = None

        if species_id == 1:
            new_organism = Fox(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Fox" not in self.organism_population_over_time:
                self.organism_population_over_time["Fox"] = []
        elif species_id == 2:
            new_organism = Owl(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Owl" not in self.organism_population_over_time:
                self.organism_population_over_time["Owl"] = []
        elif species_id == 3:
            new_organism = Frog(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Frog" not in self.organism_population_over_time:
                self.organism_population_over_time["Frog"] = []
        elif species_id == 4:
            new_organism = Snake(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Snake" not in self.organism_population_over_time:
                self.organism_population_over_time["Snake"] = []
        elif species_id == 5:
            new_organism = Hawk(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Hawk" not in self.organism_population_over_time:
                self.organism_population_over_time["Hawk"] = []
        elif species_id == 6:
            new_organism = SmallBird(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Small Bird" not in self.organism_population_over_time:
                self.organism_population_over_time["Small Bird"] = []
        elif species_id == 7:
            new_organism = Rabbit(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Rabbit" not in self.organism_population_over_time:
                self.organism_population_over_time["Rabbit"] = []
        elif species_id == 8:
            new_organism = GrassHopper(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Grass Hopper" not in self.organism_population_over_time:
                self.organism_population_over_time["Grass Hopper"] = []
        elif species_id == 9:
            new_organism = Mouse(position, animal_id, self.world.static_resource_map, self.organism_map)
            if "Mouse" not in self.organism_population_over_time:
                self.organism_population_over_time["Mouse"] = []
        else:
            print("Invalid Species ID")

        #if the species is not in the extinction timer then add it to the timer
        self.extinction_timers[species_id] = 0

        #add the new organism to the organism map
        self.organism_map[animal_id] = new_organism

        #if the organism has a random start then randomize its starting values
        if new_organism.random_start:
            new_organism.randomize_start()
        
    def update_all_Objects(self) -> None:

        #update all organisms in the simulation
        copyof_organism_map = self.organism_map.copy()
        for organism in copyof_organism_map.values():
            
            if isinstance(organism, Utility):
                continue

            organism.update()

        #call the world update function which updates all the resources in the simulation
        self.world.update()

        #check if the day has changed and update the once a day functions
        if self.world.time_of_day[0] != self.current_day:

            print(f"New Year: {self.world.time_of_day[0]}")

            #if the extinction timer hasnt been started then start a timer
            #this will be overruled later if the species is still alive
            for key in self.extinction_timers:
                if self.extinction_timers[key] == 0:
                    self.extinction_timers[key] = self.current_day + 12 #12 Days until respawn
                

            for organism in self.organism_map.values():
                if isinstance(organism, Utility):
                    continue

                #if the species is still alive then reset the extinction timer
                #this species will not need to be respawned yet
                if organism.species_id in self.extinction_timers:
                    self.extinction_timers[organism.species_id] = 0
            
            #if the extinction timer has been reached then respawn the species
            for key, value in self.extinction_timers.items():
                if value == self.current_day:
                    print(f"Respawning Species {key}")
                    for _ in range(10):
                        self.spawn_organism(key)


            self.log_population()
            self.current_day = self.world.time_of_day[0]
 
    #test world generation and basic organism spawning and movement
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
        
        #spawn utility class
        self.spawn_organism(10)
        

        self.log_population()
    
    #test advanced organism movement and tasking
    def test_two(self) -> None:
    
        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [800, 800], grass)
        self.world.spawn_resource(3, 100, [1020, 680], water)
        self.world.spawn_resource(4, 100, [1020, 200], forest)
        self.world.spawn_resource(5, 100, [300, 450], forest)
        self.world.spawn_resource(6, 100, [250, 800], water)
        self.world.spawn_resource(7, 100, [1500, 100], grass)
        self.world.spawn_resource(8, 100, [1250, 500], grass)
        self.world.spawn_resource(9, 100, [1750, 800], water)

        #fox
        for i in range(5):
            self.spawn_organism(1) 

        #owl
        for i in range(5):
            self.spawn_organism(2) 

        #frog
        for i in range(100):
            self.spawn_organism(3) 

        #snake
        for i in range(20):
            self.spawn_organism(4) 

        #hawk
        for i in range(5):
            self.spawn_organism(5) 

        #small bird
        for i in range(80):
            self.spawn_organism(6) 

        #rabbit
        for i in range(20):
            self.spawn_organism(7) 

        #grass hopper
        for i in range(1000):
            self.spawn_organism(8) 

        #mouse
        for i in range(60):
            self.spawn_organism(9)

        #spawn utility class
        self.spawn_organism(10)
        

        self.log_population()
        
    #test advanced world generation and biome spawning
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


        for i in range(2):
            self.spawn_organism(1) 

        #owl
        for i in range(1):
            self.spawn_organism(2) 

        #frog
        for i in range(10):
            self.spawn_organism(3) 

        #snake
        for i in range(2):
            self.spawn_organism(4) 

        #hawk
        for i in range(1):
            self.spawn_organism(5) 

        #small bird
        for i in range(8):
            self.spawn_organism(6) 

        #rabbit
        for i in range(10):
            self.spawn_organism(7) 

        #grass hopper
        for i in range(100):
            self.spawn_organism(8) 

        #mouse
        for i in range(10):
            self.spawn_organism(9)

        self.spawn_organism(10)
        

        self.log_population()
        
    #test sprites 
    def test_four(self) -> None:


        self.debug_mode = False

        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 225, [875, 175], grass)
        self.world.spawn_resource(2, 100, [1450, 950], grass)
        self.world.spawn_resource(3, 275, [1700, 500], forest)
        self.world.spawn_resource(4, 125, [300, 450], forest)
        self.world.spawn_resource(5, 300, [150, 1000], water)
        self.world.spawn_resource(6, 300, [300, 1000], water)
        self.world.spawn_resource(7, 300, [450, 1000], water)
        self.world.spawn_resource(8, 300, [600, 1000], water)
        self.world.spawn_resource(9, 300, [750, 1000], water)

 
        #fox
        for i in range(2):
            self.spawn_organism(1) 

        #owl
        for i in range(1):
            self.spawn_organism(2) 

        #frog
        for i in range(10):
            self.spawn_organism(3) 

        #snake
        for i in range(2):
            self.spawn_organism(4) 

        #hawk
        for i in range(1):
            self.spawn_organism(5) 

        #small bird
        for i in range(8):
            self.spawn_organism(6) 

        #rabbit
        for i in range(10):
            self.spawn_organism(7) 

        #grass hopper
        for i in range(100):
            self.spawn_organism(8) 

        #mouse
        for i in range(10):
            self.spawn_organism(9)

        self.spawn_organism(10)
        

        self.log_population()
    
    #test advanced AI decision making
    def test_five(self) -> None:
        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [800, 800], grass)
        self.world.spawn_resource(3, 100, [1020, 680], water)
        self.world.spawn_resource(4, 100, [1020, 200], forest)
        self.world.spawn_resource(5, 100, [300, 450], forest)
        self.world.spawn_resource(6, 100, [250, 800], water)
        self.world.spawn_resource(7, 100, [1500, 100], grass)
        self.world.spawn_resource(8, 100, [1250, 500], grass)
        self.world.spawn_resource(9, 100, [1750, 800], water)

        #spawn 5 rabbits and 1 fox
        for i in range(10):
             self.spawn_organism(7)

        # self.spawn_organism(1)

        self.spawn_organism(5)

        self.spawn_organism(10)
        

        self.log_population()
    
    #test extinction timers
    def test_six(self) -> None:
        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [800, 800], grass)
        self.world.spawn_resource(3, 100, [1020, 680], water)
        self.world.spawn_resource(4, 100, [1020, 200], forest)
        self.world.spawn_resource(5, 100, [300, 450], forest)
        self.world.spawn_resource(6, 100, [250, 800], water)
        self.world.spawn_resource(7, 100, [1500, 100], grass)
        self.world.spawn_resource(8, 100, [1250, 500], grass)
        self.world.spawn_resource(9, 100, [1750, 800], water)

        #1 fox

        self.spawn_organism(5)
        
        self.spawn_organism(10)
        
        self.log_population()
            
    def version_demonstration(self) -> None:
        self.debug_mode = False

        self.end_day = 4

        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 225, [875, 175], grass)
        self.world.spawn_resource(2, 100, [1450, 950], grass)
        self.world.spawn_resource(3, 275, [1700, 500], forest)
        self.world.spawn_resource(4, 125, [300, 450], forest)
        self.world.spawn_resource(5, 300, [150, 1000], water)
        self.world.spawn_resource(6, 300, [300, 1000], water)
        self.world.spawn_resource(7, 300, [450, 1000], water)
        self.world.spawn_resource(8, 300, [600, 1000], water)
        self.world.spawn_resource(9, 300, [750, 1000], water)

        #fox
        for i in range(3):
            self.spawn_organism(1) 

        #owl
        for i in range(2):
            self.spawn_organism(2) 

        #frog
        for i in range(10):
            self.spawn_organism(3) 

        #snake
        for i in range(2):
            self.spawn_organism(4) 

        #hawk
        for i in range(1):
            self.spawn_organism(5) 

        #small bird
        for i in range(12):
            self.spawn_organism(6) 

        #rabbit
        for i in range(20):
            self.spawn_organism(7) 

        #grass hopper
        for i in range(120):
            self.spawn_organism(8) 

        #mouse
        for i in range(20):
            self.spawn_organism(9)

        #spawn utility class
        self.spawn_organism(10)
        
        self.log_population()

    def version_test(self) -> None:
        self.debug_mode = True

        self.end_day = 10

        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 225, [875, 175], grass)
        self.world.spawn_resource(2, 100, [1450, 950], grass)
        self.world.spawn_resource(3, 275, [1700, 500], forest)
        self.world.spawn_resource(4, 125, [300, 450], forest)
        self.world.spawn_resource(5, 300, [150, 1000], water)
        self.world.spawn_resource(6, 300, [300, 1000], water)
        self.world.spawn_resource(7, 300, [450, 1000], water)
        self.world.spawn_resource(8, 300, [600, 1000], water)
        self.world.spawn_resource(9, 300, [750, 1000], water)

        #fox
        for i in range(3):
            self.spawn_organism(1) 

        #owl
        for i in range(2):
            self.spawn_organism(2) 

        #frog
        for i in range(10):
            self.spawn_organism(3) 

        #snake
        for i in range(2):
            self.spawn_organism(4) 

        #hawk
        for i in range(1):
            self.spawn_organism(5) 

        #small bird
        for i in range(12):
            self.spawn_organism(6) 

        #rabbit
        for i in range(20):
            self.spawn_organism(7) 

        #grass hopper
        for i in range(120):
            self.spawn_organism(8) 

        #mouse
        for i in range(20):
            self.spawn_organism(9)

        #spawn utility class
        self.spawn_organism(10)
        
        self.log_population()

    def fox_and_rabbit_test(self) -> None:
        self.debug_mode = True

        self.predator_prey_test = True
        self.end_day = 80

        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [800, 800], grass)
        self.world.spawn_resource(3, 100, [1020, 680], water)
        self.world.spawn_resource(4, 100, [1020, 200], forest)
        self.world.spawn_resource(5, 100, [300, 450], forest)
        self.world.spawn_resource(6, 100, [250, 800], water)
        self.world.spawn_resource(7, 100, [1500, 100], grass)
        self.world.spawn_resource(8, 100, [1250, 500], grass)
        self.world.spawn_resource(9, 100, [1750, 800], water)

        #fox
        for i in range(50):
            self.spawn_organism(1)
        
        #rabbit
        for i in range(500):
            self.spawn_organism(7)

        self.spawn_organism(10)
        
        self.log_population()

    def no_predators_test(self) -> None:

        self.debug_mode = True

        self.end_day = 50

        grass = 1
        water = 2
        forest = 3

        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [800, 800], grass)
        self.world.spawn_resource(3, 100, [1020, 680], water)
        self.world.spawn_resource(4, 100, [1020, 200], forest)
        self.world.spawn_resource(5, 100, [300, 450], forest)
        self.world.spawn_resource(6, 100, [250, 800], water)
        self.world.spawn_resource(7, 100, [1500, 100], grass)
        self.world.spawn_resource(8, 100, [1250, 500], grass)
        self.world.spawn_resource(9, 100, [1750, 800], water)

        #rabbit
        for i in range(10):
            self.spawn_organism(7) 

        self.spawn_organism(10)
        

        self.log_population()
 
    def trophic_levels_test(self) -> None:
        self.debug_mode = True

        self.end_day = 10

        grass = 1
        water = 2
        forest = 3

        self.world.max_cap = 5000
        self.world.regen_rate_cap = 5

        self.world.spawn_resource(1, 100, [500, 200], grass)
        self.world.spawn_resource(2, 100, [800, 800], grass)
        self.world.spawn_resource(3, 100, [1020, 680], water)
        self.world.spawn_resource(4, 100, [1020, 200], forest)
        self.world.spawn_resource(5, 100, [300, 450], forest)
        self.world.spawn_resource(6, 100, [250, 800], water)
        self.world.spawn_resource(7, 100, [1500, 100], grass)
        self.world.spawn_resource(8, 100, [1250, 500], grass)
        self.world.spawn_resource(9, 100, [1750, 800], water)

        #fox
        for i in range(5):
            self.spawn_organism(1) 

        #owl
        for i in range(5):
            self.spawn_organism(2) 

        #frog
        for i in range(100):
            self.spawn_organism(3) 

        #snake
        for i in range(20):
            self.spawn_organism(4) 

        #hawk
        for i in range(5):
            self.spawn_organism(5) 

        #small bird
        for i in range(80):
            self.spawn_organism(6) 

        #rabbit
        for i in range(20):
            self.spawn_organism(7) 

        #grass hopper
        for i in range(1000):
            self.spawn_organism(8) 

        #mouse
        for i in range(60):
            self.spawn_organism(9)

        self.spawn_organism(10)
        

        self.log_population()

    def run_simulation(self) -> None:

        option = input("\nPlease Select Additional Options:\n\n1. Normal Speed\n2. 2x Speed\n3. Max Speed\n\nPlease Select Option: ")

        if option == "1":
            tick_rate = 30
        elif option == "2":
            tick_rate = 60
        elif option == "3":
            tick_rate = math.inf
        else:
            print("Invalid Option Selected. Running Simulation at Normal Speed.")
            tick_rate = 30

        print("\nRunning Simulation switch to the pygame window to view the simulation")

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            if self.current_day > self.end_day:
                running = False
            
            self.update_all_Objects()
            self.draw_all_objects()
            self.clock.tick(tick_rate)
            pg.display.flip()
        self.plot_population()


if __name__ == "__main__":
    
    

    print("\nRunning Simulation")
    print("1. Demonstration Version")
    print("2. All Species No Heavy Graphics Test (performance mode)")
    print("3. Specific Tests (1-3)")
    print("4. Pre-Alpha Tests")
    option = input("Select Model to Run: ")

    if option == "1":
        sim = Simulation()
        sim.version_demonstration()
    elif option == "2":
        sim = Simulation()
        sim.version_test()
    elif option == "3":
        print("\n1. Predator Prey Test")
        print("2. Carrying Capacity Test")
        print("3. Trophic Levels Test")
        test_option = input("Select Test to Run: ")
        if test_option == "1":
            sim = Simulation()
            sim.fox_and_rabbit_test()
        elif test_option == "2":
            sim = Simulation()
            sim.no_predators_test()
        elif test_option == "3":
            sim = Simulation()
            sim.trophic_levels_test()
        else:
            print("Invalid Test Option")
    elif option == "4":
        print("\nThe following tests are prototype test environments some of which may not be fully functional as critical components have been redesigned")
        print("1. Test One")
        print("2. Test Two")
        print("3. Test Three")
        print("4. Test Four")
        print("5. Test Five")
        print("6. Test Six")
        test_option = input("Select Test to Run: ")
        if test_option == "1":
            sim = Simulation()
            sim.test_one()
        elif test_option == "2":
            sim = Simulation()
            sim.test_two()
        elif test_option == "3":
            sim = Simulation()
            sim.test_three()
        elif test_option == "4":
            sim = Simulation()
            sim.test_four()
        elif test_option == "5":
            sim = Simulation()
            sim.test_five()
        elif test_option == "6":
            sim = Simulation()
            sim.test_six()
        else:
            print("Invalid Test Option")
    else:
        print("Invalid Option")

    sim.run_simulation()

    print("Simulation Complete")
    


    


    

    