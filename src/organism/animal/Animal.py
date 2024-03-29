import sys
import random
import math
sys.path.append("src")
from organism.Organism import Organism
from typing import List, Any

class Animal(Organism):

    def __init__(self, organism_position: List[float], animal_id: int):

        super().__init__(organism_position, animal_id)

        # inherited variables

        # self.organism_position = organism_position
        # self.animal_id = animal_id
        # self.all_known_resources = []
        # self.all_known_organisms = []
        # self.alive_status = True

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

        #Binary variables for AI
        self.needs_sleep = False
        self.in_danger = False
        self.needs_food = False
        self.needs_water = False
        self.needs_mate = False


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

    def add_post_creation_attributes(self, all_known_static_resources, all_known_dynamic_resources, all_known_organisms) -> None:
        self.all_known_static_resources = all_known_static_resources
        self.all_known_dynamic_resources = all_known_dynamic_resources
        self.all_known_organisms = all_known_organisms

    def drink_water(self) -> None:
        self.thirst = 0
        self.needs_water = False
    
    def eat_food(self, amount: float) -> None:
        self.hunger = 0
        self.needs_food = False

    # TODO: Implement this method, This needs to have creature movement implemented first
    def wander(self) -> None:
        one_in_four = random.randint(1, 4)
        if one_in_four == 1:
            self.current_direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
        else:
            self.current_direction = [0, 0]

    def sleep(self) -> None:
        self.decision_duration = self.sleep_duration
        self.current_direction = [0, 0]
        self.needs_sleep = False
        self.exhaustion = 0


    def run_away_from_threats(self) -> None:
        target = self.current_threat
        target_current_direction = target.current_direction

        self.current_direction = [target_current_direction[0] + random.uniform(-0.1,0.1), target_current_direction[1] + random.uniform(-0.1,0.1)]


    def Detect_Threats(self) -> None:
        for organism in self.all_known_organisms.values():
            organism_position = organism.organism_position
            distance = ((self.organism_position[0] - organism_position[0])**2 + (self.organism_position[1] - organism_position[1])**2)**0.5
            if distance < self.sight_range:
                if organism.species_id in self.potential_predators:
                    self.current_threat = organism
                    return

    def Detect_Mates(self) -> None:
        for organism in self.all_known_organisms.values():
            organism_position = organism.organism_position
            distance = ((self.organism_position[0] - organism_position[0])**2 + (self.organism_position[1] - organism_position[1])**2)**0.5
            if distance < self.sight_range:
                if organism.species_id == self.species_id:
                    self.current_target = organism
                    return
        self.current_target = None
    
    def Detect_Water(self):
        for resource in self.all_known_static_resources.values():
            resource_position = resource.resource_position
            distance = ((self.organism_position[0] - resource_position[0])**2 + (self.organism_position[1] - resource_position[1])**2)**0.5
            if distance < self.sight_range:
                if resource.resource_type_id in self.consumable_resources:
                    self.current_target = resource
                    return
        
        return False

    def move_towards_resource(self, resource_type_id: Any) -> None:

        def closest_resource_of_type(resource_type_id: Any) -> Any:
            min_distance = math.inf
            closest_resource = None
            for resource in self.all_known_static_resources.values():
                if resource.resource_type_id == resource_type_id:
                    resource_position = resource.resource_position
                    cur_distance = ((self.organism_position[0] - resource_position[0])**2 + (self.organism_position[1] - resource_position[1])**2)**0.5
                    if cur_distance < min_distance:
                        min_distance = cur_distance
                        closest_resource = resource
            return closest_resource
        
        resource = closest_resource_of_type(resource_type_id)
        self.current_target = resource
        resource_position = resource.resource_position
        slope = (resource_position[1] - self.organism_position[1]) / (resource_position[0] - self.organism_position[0])
        angle = math.atan(slope)
        self.current_direction = [math.cos(angle), math.sin(angle)]
    
    def move_towards_organism(self, organism: Any) -> None:
        organism_position = organism.organism_position
        slope = (organism_position[1] - self.organism_position[1]) / (organism_position[0] - self.organism_position[0])
        angle = math.atan(slope)
        self.current_direction = [math.cos(angle), math.sin(angle)]

    def move_towards_dynamic_resource(self, resource: Any) -> None:
        resource_position = resource.resource_position
        slope = (resource_position[1] - self.organism_position[1]) / (resource_position[0] - self.organism_position[0])
        angle = math.atan(slope)
        self.current_direction = [math.cos(angle), math.sin(angle)]
    
    def move(self) -> None:
        try:
            self.organism_position[0] += self.current_direction[0]*self.min_speed
            self.organism_position[1] += self.current_direction[1]*self.min_speed
        except:
            print(f"Error in move function {self.current_direction}")

    def run(self) -> None:
        self.organism_position[0] += self.current_direction[0]*self.max_speed
        self.organism_position[1] += self.current_direction[1]*self.max_speed
        
    def kill_organism(self, organism: Any) -> None:
        organism.alive_status = False

    def make_decision(self) -> None:
        pass

    def update(self) -> None:
        self.make_decision()
        self.move()
        self.hunger += 1
        self.thirst += 1
        self.exhaustion += 1
        self.procreate_cool_down -= 1


        if self.debug_mode:
            print(f"Current Direction {self.current_direction} ", end="")
            if self.needs_food:
                distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                print(f"Getting food : {self.hunger} : Distance to food : {distance}")
            if self.needs_water:
                distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                print(f"Getting water : {self.thirst} : Distance to water : {distance}")
            if self.needs_sleep:
                print(f"Sleeping : {self.exhaustion}")

            pass
            
            

