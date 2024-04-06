import sys
import random
import math
import pygame as pg
sys.path.append("src")
sys.path.append("src/maplogic")

from maplogic.GrassPlant import GrassPlant
from maplogic.StaticResource import StaticResource
from maplogic.GrassLands import GrassLands

from organism.Organism import Organism
from typing import List, Any

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BLACK = '\033[30m'
    BOLD = '\033[1m'
    

# Colorizing function
def colorize(text, color):
    return f"{color}{text}{colors.RESET}"

class Animal(Organism):

    def __init__(self, organism_position: List[float], animal_id: int, all_known_static_resources: Any, all_known_organisms: Any):

        super().__init__(organism_position, animal_id)

        # inherited variables

        # self.organism_position = organism_position
        # self.animal_id = animal_id

        # self.all_known_static_resources = {}
        # self.all_known_dynamic_resources = {}
        # self.all_known_organisms = {}
        # self.alive_status = True
        # self.visited_static_resources = []
        # self.gender = None

        # 0 = male, 1 = female
        self.gender = random.randint(0, 1)
        
        self.all_known_static_resources = all_known_static_resources
        self.all_known_organisms = all_known_organisms

        self.hunger = 0
        self.thirst = 0
        self.exhaustion = 0
        self.ready_to_mate = False
        self.current_target = None
        self.current_threat = None
        self.progress_left_on_decision = 0
        self.current_direction = [0, 0]
        self.safe_place = None

        self.random_start = True
        self.debug_mode = True

        #Spriteloader Variables
        self.sprite = None 

        #Binary variables for AI
        self.needs_sleep = False
        self.in_danger = False
        self.needs_food = False
        self.needs_water = False
        self.needs_mate = False
        self.female = False
        self.needs_for_speed = False
        self.current_task = False
        self.absolute_need = False


        #override these variables in the child class
        self.species_id = None
        self.procreate_cool_down = None
        self.max_hunger = None
        self.max_thirst = None
        self.max_exhaustion = None
        self.min_hunger = None
        self.min_thirst = None
        self.max_speed = None
        self.min_speed = None
        self.mass = None
        self.sight_range = None
        self.feeding_range = None
        self.sleep_duration = None
        self.detection_multiplier = None
        self.consumable_resources = None
        self.decision_duration = None
        self.potential_predators = None
        self.visited_static_resources = []
        self.hidden = False # for herbivores
        

    def randomize_start(self) -> None:
        self.hunger = random.randint(0, self.min_hunger)
        self.thirst = random.randint(0, self.min_thirst)
        self.exhaustion = random.randint(0, self.max_exhaustion)
        self.procreate_cool_down = random.randint(0, self.procreate_cool_down)

    def is_absolute_need(self):
        if self.hunger > self.max_hunger * 0.8 or self.thirst > self.max_thirst * 0.8:
            self.absolute_need = True
            return True
        self.absolute_need = False
        return False
        

    def drink_water(self) -> None:
        #print(colorize("Drinking", colors.BLUE))
        self.thirst = 0
        self.needs_water = False
        self.current_target = None
        self.current_direction = [0, 0]
        self.current_task = False
        self.absolute_need = False
    
    def eat_food(self) -> None:

        #print(colorize("Eating", colors.GREEN))

        if self.current_target.alive_status == False:
            self.current_target = None
            self.current_direction = [0, 0]
            return
        
        food_need = self.mass * self.metabolism_constant

        # carnivore Eating method
        if self.dietary_classification == 0:
            
            if self.current_target.mass > food_need:
                self.kill_organism(self.current_target)
                self.hunger = 0
                self.needs_food = False
                self.current_target = None
                self.current_direction = [0, 0]
                self.current_task = False
        
            elif self.current_target.mass <= food_need:
                self.kill_organism(self.current_target)
                percent_reduction = abs(1 - ((food_need - self.current_target.mass) / food_need))
                self.hunger -= self.max_hunger * percent_reduction
                self.current_direction = [0, 0]

        # herbivore Eating method
        if self.dietary_classification == 1:

            if self.current_target.mass > food_need:
                self.current_target.mass -= food_need
                self.hunger = 0
                self.needs_food = False
                self.current_target = None
                self.current_direction = [0, 0]
                self.current_task = False
                self.visited_static_resources = []
            
            elif self.current_target.mass <= food_need:
                self.kill_organism(self.current_target)
                percent_reduction = abs(1 - ((food_need - self.current_target.mass) / food_need))
                self.hunger -= self.max_hunger * percent_reduction
                self.current_direction = [0, 0]
        
        self.absolute_need = False
            

    # TODO: Implement this method, This needs to have creature movement implemented first
    def wander(self) -> None:
        one_in_four = random.randint(1, 2)

        
        if one_in_four == 1:

            self.visited_static_resources = []
            water = self.closest_resource_of_type(2)
            distance_to_water = ((self.organism_position[0] - water.resource_position[0])**2 + (self.organism_position[1] - water.resource_position[1])**2)**0.5

            if distance_to_water <= self.min_speed*self.progress_left_on_decision:
                angle = math.atan2(water.resource_position[1] - self.organism_position[1], water.resource_position[0] - self.organism_position[0])
                angle += math.pi
                self.current_direction = [math.cos(angle), math.sin(angle)]
            else:
                self.current_direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
            #print(colorize("Wandering", colors.BLACK))
        else:
            self.current_direction = [0, 0]
            #print(colorize("Not Moving", colors.BLACK))

    def sleep(self) -> None:
        #print(colorize("Sleeping", colors.YELLOW))
        self.progress_left_on_decision = self.sleep_duration
        self.current_direction = [0, 0]
        self.current_target = None
        self.needs_sleep = False
        self.exhaustion = 0
        self.current_task = False


    def run_away_from_threats(self) -> None:
        target = self.current_threat
        target_position = target.organism_position
        angle = math.atan2(target_position[1] - self.organism_position[1], target_position[0] - self.organism_position[0])
        distance = ((self.organism_position[0] - target_position[0])**2 + (self.organism_position[1] - target_position[1])**2)**0.5
        self.current_direction = [-math.cos(angle), -math.sin(angle)]

        if distance > target.sight_range * 3 and target.needs_food:
            self.in_danger = False
            self.current_threat = None
            self.needs_for_speed = False
            self.hidden = True
            self.current_direction = [0, 0]
            self.progress_left_on_decision = self.sleep_duration
            self.current_task = False
        
        if distance > target.sight_range * 3 and not target.needs_food:
            self.in_danger = False
            self.current_threat = None
            self.needs_for_speed = False
            self.current_task = False

    def detect_threats(self) -> None:
        for organism in self.all_known_organisms.values():
            if organism.species_id not in self.potential_predators or not organism.alive_status or organism.needs_sleep or organism.hidden:
                continue
            threat_position = organism.organism_position
            distance = ((self.organism_position[0] - threat_position[0])**2 + (self.organism_position[1] - threat_position[1])**2)**0.5
            if distance < self.sight_range:
                self.current_threat = organism
                self.in_danger = True
                #print(colorize("Threat Detected", colors.RED))
                return


    def detect_mates(self) -> None:
        self.current_target = None
        for organism in self.all_known_organisms.values():
            mate_position = organism.organism_position
            distance = ((self.organism_position[0] - mate_position[0])**2 + (self.organism_position[1] - mate_position[1])**2)**0.5

            if organism.species_id != self.species_id:
                continue

            if not organism.ready_to_mate:
                continue

            if distance > self.sight_range:
                continue

            if organism.animal_id == self.animal_id:
                continue

            if organism.gender == self.gender:
                continue

            if distance < self.sight_range*4:
                self.move_towards_organism(organism)

    def closest_resource_of_type(self, resource_type_id: Any) -> Any:
        min_distance = math.inf
        closest_resource = None
        for resource in self.all_known_static_resources.values():
            if resource.resource_type_id == resource_type_id:
                resource_position = resource.resource_position
                cur_distance = ((self.organism_position[0] - resource_position[0])**2 + (self.organism_position[1] - resource_position[1])**2)**0.5
                if cur_distance < min_distance and resource not in self.visited_static_resources:
                    min_distance = cur_distance
                    closest_resource = resource
        return closest_resource

    def move_towards_resource(self, resource_type_id: Any) -> None:

        resource = self.closest_resource_of_type(resource_type_id)

        if resource is None:
            #print(colorize("No resource found emptying visited resources", colors.BOLD))
            self.visited_static_resources = []
            return

        self.current_target = resource
        resource_position = resource.resource_position
        angle = math.atan2(resource_position[1] - self.organism_position[1], resource_position[0] - self.organism_position[0])

        self.current_direction = [math.cos(angle), math.sin(angle)]

    def move_towards_specific_resource(self, resource: Any) -> None:

        self.current_target = resource
        resource_position = resource.resource_position
        angle = math.atan2(resource_position[1] - self.organism_position[1], resource_position[0] - self.organism_position[0])

        self.current_direction = [math.cos(angle), math.sin(angle)]
    
    def move_towards_organism(self, organism: Any) -> None:
        self.current_target = organism
        organism_position = organism.organism_position
        angle = math.atan2(organism_position[1] - self.organism_position[1], organism_position[0] - self.organism_position[0])
        self.current_direction = [math.cos(angle), math.sin(angle)]

    # def is_current_target_dynamic(self) -> bool:
    #     return self.current_target in self.all_known_dynamic_resources.values()
    
    def is_current_target_static(self) -> bool:
        return isinstance(self.current_target, StaticResource) or isinstance(self.current_target, GrassLands)
    
    def is_current_target_organism(self) -> bool:

        if isinstance(self.current_target, StaticResource) or isinstance(self.current_target, GrassLands):
            return False

        return self.current_target in self.all_known_organisms.values()

    # def move_towards_dynamic_resource(self, resource: Any) -> None:
    #     resource_position = resource.resource_position
    #     angle = math.atan2(resource_position[1] - self.organism_position[1], resource_position[0] - self.organism_position[0])
    #     self.current_direction = [math.cos(angle), math.sin(angle)]
    
    def move(self) -> None:
        try:
            self.organism_position[0] += self.current_direction[0]*self.min_speed
            self.organism_position[1] += self.current_direction[1]*self.min_speed
        except:
            print(f"Error in move function {self.current_direction}")

    def run(self) -> None:
        try:
            self.organism_position[0] += self.current_direction[0]*self.max_speed
            self.organism_position[1] += self.current_direction[1]*self.min_speed
        except:
            print(f"Error in move function {self.current_direction}")
        
    def kill_organism(self, organism: Any) -> None:
        organism.die("predation")

    def make_decision(self) -> None:
        pass

    def procreate(self) -> Any:
        pass

    def update(self) -> None:

        self.make_decision()

        if self.needs_for_speed:
            self.run()
        else:
            self.move()


        self.hunger += 1
        self.thirst += 1
        self.exhaustion += 1
        self.procreate_cool_down -= 1




        # if self.debug_mode:
        #     print(f"Current Direction {self.current_direction} ", end="")
        #     if self.needs_food:
        #         distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
        #         print(f"Getting food : {self.hunger} : Distance to food : {distance}")
        #     if self.needs_water:
        #         distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
        #         print(f"Getting water : {self.thirst} : Distance to water : {distance}")
        #     if self.needs_sleep:
        #         print(f"Sleeping : {self.exhaustion}")
        #     pass
            
            
    #Animal sprite loading handler.
    def load_sprite(self) -> None:
        for i in range(10):
            if i == self.species_id:
                sprite_filename = f"assets/sprites/sprite_{self.species_id}.png"
                try:
                    self.sprite = pg.image.load(sprite_filename)
                except pg.error:
                    print(f"Error loading sprite for species ID {self.species_id}")
                    return
                break
        else:
            print(f"Invalid animal ID {self.species_id}")