import sys
import random
import math
import pygame as pg
sys.path.append("src")
sys.path.append("src/maplogic")

from maplogic.StaticResource import StaticResource
from maplogic.GrassLands import GrassLands

from organism.Organism import Organism
from typing import List, Any

# Grandparent class
# This class is the parent class for all animals in the simulation
# It contains more advanced attributes and methods that are specific to animals
# It will be used frequently for the AI of the animals
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

        #Determines if the animal will have random hunger, thirst, exhaustion, and procreate cool down values on start
        self.random_start = True

        #Determines if the animal will be a sprite or a circle on the map
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
        self.hidden = False 


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


    # function is used to detect the closest resource of a specific type
    # it works by iterating through all known static resources and finding the closest resource of the specified type
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

    # function is used to detect mates
    # the animal will check if any known organisms capable of mating are within its sight range
    # if a mate is found, the animal will move towards the mate
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

            # sight range is multiplied by 4 to represent mating calls
            if distance < self.sight_range*4:
                self.move_towards_organism(organism)

    # function is used to scan the area for threats
    # the animal will check if any known predators are within its sight range
    # if a predator is found, the animal will set the predator as its current threat if it is not already and the predator needs food and is not either sleeping, hidden, or dead
    def detect_threats(self) -> None:
        for organism in self.all_known_organisms.values():

            if organism.species_id not in self.potential_predators or not organism.alive_status or organism.needs_sleep or organism.hidden or not organism.needs_food:
                continue

            threat_position = organism.organism_position
            distance = ((self.organism_position[0] - threat_position[0])**2 + (self.organism_position[1] - threat_position[1])**2)**0.5

            if distance < self.sight_range:
                self.current_threat = organism
                self.in_danger = True
                return

    def drink_water(self) -> None:
        self.thirst = 0
        self.needs_water = False
        self.current_target = None
        self.current_direction = [0, 0]
        self.current_task = False
        # need satisfied so the animal will not be in danger of dying from hunger
        self.absolute_need = False

    def eat_food(self) -> None:
        
        # confirm that the target is still alive and was not eaten by the previous predator during this turn
        if self.current_target.alive_status == False:
            self.current_target = None
            self.current_direction = [0, 0]
            return
        
        # calculate the amount of food the animal needs to eat
        food_need = self.mass * self.metabolism_constant

        # carnivore Eating method
        if self.dietary_classification == 0:
            
            # if the target has more mass than the animal needs, the animal will eat the target and the hunger will be reset
            # the target will still die since the animal will kill the target before eating it
            if self.current_target.mass > food_need:
                self.kill_organism(self.current_target)
                self.hunger = 0
                self.needs_food = False
                self.current_target = None
                self.current_direction = [0, 0]
                self.current_task = False
        
            # if the target has less mass than the animal needs, the animal will eat the target and the hunger will be reduced by the difference
            elif self.current_target.mass <= food_need:
                self.kill_organism(self.current_target)
                percent_reduction = abs(1 - ((food_need - self.current_target.mass) / food_need))
                self.hunger -= self.max_hunger * percent_reduction
                self.current_direction = [0, 0]

        # herbivore Eating method
        if self.dietary_classification == 1:

            # if the target has more mass than the animal needs, the animal will eat the target and the hunger will be reset
            # the target will not die since the animal will not kill the target before eating it
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
        
        # need satisfied so the animal will not be in danger of dying from hunger
        self.absolute_need = False

    #if the animal is close to death, it will have an absolute need to eat or drink
    #this will override all other needs except for sleep
    #predators will nolonger scare the animal whether for the better or for the very very worse...
    def is_absolute_need(self):
        if self.hunger > self.max_hunger * 0.8 or self.thirst > self.max_thirst * 0.8:
            self.absolute_need = True
            return True
        self.absolute_need = False
        return False

    def is_current_target_static(self) -> bool:
        return isinstance(self.current_target, StaticResource) or isinstance(self.current_target, GrassLands)
    
    def is_current_target_organism(self) -> bool:

        if isinstance(self.current_target, StaticResource) or isinstance(self.current_target, GrassLands):
            return False

        return self.current_target in self.all_known_organisms.values()

    # function is used to kill the passed organism
    # the organism will be removed from the simulation
    # the cause of death will be counted
    def kill_organism(self, organism: Any) -> None:
        organism.die("predation")

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

    # function is used to move at the animals min speed
    # it works by taking the direction vector: current direction and multiplying it by the min speed
    # it then adds the result to the animals position
    def move(self) -> None:
        try:
            self.organism_position[0] += self.current_direction[0]*self.min_speed
            self.organism_position[1] += self.current_direction[1]*self.min_speed
        except:
            print(f"Error in move function {self.current_direction}")

    # function is used to move towards the closest resource of a specific type
    # the animal will move towards the resource at its min speed
    # the animal will stop moving when it reaches the resource
    # the animal will not move towards the resource if it is already been visited within the length of its most recent type of decision
    def move_towards_resource(self, resource_type_id: Any) -> None:

        resource = self.closest_resource_of_type(resource_type_id)

        # if there are no resources of the specified type, this means the animal has already visited all resources of that type
        # the animal will empty its visited resources and try again
        if resource is None:
            self.visited_static_resources = []
            return

        self.current_target = resource
        resource_position = resource.resource_position
        angle = math.atan2(resource_position[1] - self.organism_position[1], resource_position[0] - self.organism_position[0])

        self.current_direction = [math.cos(angle), math.sin(angle)]

    # function is used to move towards the closest resource of a specific type
    # very similar to the move_towards_resource function except it will not search for the closest resource
    # it will move towards the resource that is passed as a parameter
    def move_towards_specific_resource(self, resource: Any) -> None:

        self.current_target = resource
        resource_position = resource.resource_position
        angle = math.atan2(resource_position[1] - self.organism_position[1], resource_position[0] - self.organism_position[0])

        self.current_direction = [math.cos(angle), math.sin(angle)]
    
    # function is used to move towards the passed organism
    # the animal will move towards the organism at its min speed
    def move_towards_organism(self, organism: Any) -> None:
        self.current_target = organism
        organism_position = organism.organism_position
        angle = math.atan2(organism_position[1] - self.organism_position[1], organism_position[0] - self.organism_position[0])
        self.current_direction = [math.cos(angle), math.sin(angle)]

    def randomize_start(self) -> None:
        self.hunger = random.randint(0, self.min_hunger)
        self.thirst = random.randint(0, self.min_thirst)
        self.exhaustion = random.randint(0, self.max_exhaustion)
        self.procreate_cool_down = random.randint(0, self.procreate_cool_down)

    # function is used to move at the animals max speed
    # it works by taking the direction vector: current direction and multiplying it by the max speed
    # it then adds the result to the animals position
    def run(self) -> None:
        try:
            self.organism_position[0] += self.current_direction[0]*self.max_speed
            self.organism_position[1] += self.current_direction[1]*self.min_speed
        except:
            print(f"Error in move function {self.current_direction}")

    # function is used to make the animal run away from threats
    # the animal will move in the opposite direction of the threat at its max speed
    # the animal will not move towards the threat until the threat is out of sight
    # the animal will not move towards the threat if the threat does not need food
    # the animal may run into other threats while running away from their current threat
    def run_away_from_threats(self) -> None:
        target = self.current_threat
        target_position = target.organism_position
        angle = math.atan2(target_position[1] - self.organism_position[1], target_position[0] - self.organism_position[0])
        distance = ((self.organism_position[0] - target_position[0])**2 + (self.organism_position[1] - target_position[1])**2)**0.5
        self.current_direction = [-math.cos(angle), -math.sin(angle)]

        # if the threat is out of sight, the animal will stop running and will hide
        # when hidden, the animal will not move, make decisions, or be at risk of being eaten
        if distance > target.sight_range * 3:
            self.in_danger = False
            self.current_threat = None
            self.needs_for_speed = False
            self.hidden = True
            self.current_direction = [0, 0]
            self.progress_left_on_decision = self.sleep_duration
            self.current_task = False

    # function is used to make the animal sleep
    # it works by setting the animals progress left on decision to the sleep duration
    # the animal will not move or make any decisions until the progress left on decision is 0
    # the animal can still die from hunger, thirst, while sleeping
    # this represents the animal dying from completely exhausting itself
    def sleep(self) -> None:
        self.progress_left_on_decision = self.sleep_duration
        self.current_direction = [0, 0]
        self.current_target = None
        self.needs_sleep = False
        self.exhaustion = 0
        self.current_task = False

    # function is used to update the animal attributes and make AI decisions
    def update(self) -> None:

        # updates the animals AI decision
        self.make_decision()

        # if the animal is in danger, it will move at the max speed
        if self.needs_for_speed:
            self.run()
        # if not, it will move at the min speed
        else:
            self.move()

        # increment the animals hunger, thirst, exhaustion, and procreate cool down
        # this is called every tick regardless if the animal can make a decision yet or not
        self.hunger += 1
        self.thirst += 1
        self.exhaustion += 1
        self.procreate_cool_down -= 1

    # implements random walks
    # the animal will move in a random direction
    # this is used when the animal is not in danger, does not need sleep, food, water, or a mate
    def wander(self) -> None:

        # 50% chance of moving in a random direction
        # 50% chance of not moving
        one_in_two = random.randint(1, 2)

        if one_in_two == 1:

            # make sure the animal has no bias towards a specific resource
            self.visited_static_resources = []

            # find the closest water resource
            water = self.closest_resource_of_type(2)
            distance_to_water = ((self.organism_position[0] - water.resource_position[0])**2 + (self.organism_position[1] - water.resource_position[1])**2)**0.5

            # try its best to avoid walking through water
            if distance_to_water <= self.min_speed*self.progress_left_on_decision:
                angle = math.atan2(water.resource_position[1] - self.organism_position[1], water.resource_position[0] - self.organism_position[0])
                angle += math.pi
                self.current_direction = [math.cos(angle), math.sin(angle)]
            else:
                self.current_direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
        else:
            self.current_direction = [0, 0]

    # override this function in the child class
    def make_decision(self) -> None:
        pass

    # override this function in the child class
    def procreate(self) -> Any:
        pass









    

    




    






         
