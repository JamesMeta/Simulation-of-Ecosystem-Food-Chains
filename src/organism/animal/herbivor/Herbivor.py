import sys
import random
sys.path.append("src/maplogic")
sys.path.append("src/organism/animal")
from Animal import Animal
from maplogic.GrassPlant import GrassPlant
from typing import List, Any
import math

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
    

# Colorizing function
def colorize(text, color):
    return f"{color}{text}{colors.RESET}"

class Herbivor(Animal):
    
    def __init__(self, organism_position: List[float], animal_id: int, all_known_static_resources: Any, all_known_organisms: Any):

        super().__init__(organism_position, animal_id, all_known_static_resources, all_known_organisms)

        # inherited variables

        # self.organism_position = organism_position
        # self.animal_id = animal_id

        # self.all_known_static_resources = {}
        # self.all_known_dynamic_resources = {}
        # self.all_known_organisms = {}
        # self.alive_status = True
        # self.visited_static_resources = []
        # self.gender = None

        # self.hunger = 0
        # self.thirst = 0
        # self.exhaustion = 0
        # self.ready_to_mate = False
        # self.current_target = None
        # self.current_threat = None
        # self.progress_left_on_decision = 0
        # self.current_direction = [0, 0]
        # self.safe_place = None

        # self.random_start = True
        # self.debug_mode = True

        # #Binary variables for AI
        # self.needs_sleep = False
        # self.in_danger = False
        # self.needs_food = False
        # self.needs_water = False
        # self.needs_mate = False
        # self.female = False
        # self.needs_for_speed = False
        # self.current_task = False

        self.hidden = False
        self.dietary_classification = 1

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



    def check_if_current_task_in_range(self) -> None:
        if self.needs_food and self.current_target is not None:
            if self.is_current_target_static():
                
                if self.is_at_grass_lands_center() and not self.detect_grass_plants():
                    self.visited_static_resources.append(self.current_target)
                    self.current_target = None
                    self.progress_left_on_decision = self.decision_duration
                    return
                
                elif self.is_within_grass_lands():
                    if self.detect_grass_plants():
                        self.move_towards_grass_plants(self.current_target)
                        self.progress_left_on_decision = self.decision_duration
                        return
                    

                else:
                    self.detect_grass_plants()
                    self.move_towards_grass_plants(self.current_target)
                    self.progress_left_on_decision = self.decision_duration
                
            elif self.is_current_target_grass_plants():
                distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                if distance < self.feeding_range:
                    self.eat_food()
                    self.progress_left_on_decision = self.decision_duration
                    return
                else:
                    self.move_towards_grass_plants(self.current_target)
                    self.progress_left_on_decision = self.decision_duration
                    return

                
        if self.needs_water and self.current_target is not None:
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            distance -= self.current_target.resource_radius
            if distance < self.feeding_range:
                self.drink_water()
            else:
                pass

        if self.ready_to_mate and self.current_target is not None:
            distance = ((self.organism_position[0] - self.current_target.organism_position[0])**2 + (self.organism_position[1] - self.current_target.organism_position[1])**2)**0.5
            if distance <= self.feeding_range:
                self.procreate()
            else:
                pass

    def make_decision(self) -> None:

        if self.hunger > self.max_hunger:
            self.die()
        
        if self.thirst > self.max_thirst:
            self.die()

        if self.current_task:
            self.check_if_current_task_in_range()

        if self.progress_left_on_decision == 0:

            #print(colorize(f"{self.name}#{self.animal_id} Making Decision:", colors.WHITE), end=" ")

            # first layer of decision making: Check alive status
            
            # second layer of decision making: Check if the organism is in danger
            if self.in_danger:
                self.run_away_from_threats()
                self.progress_left_on_decision = self.decision_duration
                self.needs_for_speed = True
                self.needs_food = False
                self.needs_water = False
                self.needs_sleep = False
                self.ready_to_mate = False
                self.current_task = False
                return
            
            else:
                self.needs_for_speed = False
            
            # third layer of decision making: Check if the organism needs sleep, food, or water balancing the priorities based on absolute needs

            if self.hunger > self.min_hunger or self.thirst > self.min_thirst:
                percent_food_remaining = 1 - (self.hunger / self.max_hunger)
                percent_water_remaining = 1 - (self.thirst / self.max_thirst)
                self.ready_to_mate = False
                self.current_task = True
            

                if percent_food_remaining <= percent_water_remaining:
                    self.needs_food = True
                    self.needs_water = False
                    
                if percent_water_remaining <= percent_food_remaining:
                    self.needs_water = True
                    self.needs_food = False

            exhaustion_remaining = self.max_exhaustion - self.exhaustion

            if exhaustion_remaining < 0:
                self.needs_sleep = True
                self.needs_food = False
                self.needs_water = False
                self.ready_to_mate = False
                self.current_task = False
            
            if self.needs_sleep:
                #print(colorize("Needs Sleep", colors.YELLOW))
                if self.safe_place is not None:
                    self.move_towards_resource(self.safe_place.resource_type_id)
                    distance = ((self.organism_position[0] - self.safe_place.resource_position[0])**2 + (self.organism_position[1] - self.safe_place.resource_position[1])**2)**0.5
                    if distance < self.safe_place.resource_radius:
                        self.sleep()
                        self.hidden = True
                        return
                    else:
                        self.progress_left_on_decision = self.decision_duration
                        return
                else:
                    self.sleep()
                    return
            
            if self.needs_food:
                #print(colorize("Needs Food", colors.GREEN))

                food_id = random.choice(self.consumable_resources)

                if self.is_current_target_grass_plants():
                    distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                    if distance < self.feeding_range:
                        self.eat_food()
                        self.progress_left_on_decision = self.decision_duration
                        return
                    else:
                        self.move_towards_grass_plants(self.current_target)
                        self.progress_left_on_decision = self.decision_duration
                        return

                elif self.is_within_grass_lands():
                    found = self.detect_grass_plants()
                    if not found:
                        self.visited_static_resources.append(self.current_target)
                        self.current_target = None
                        self.progress_left_on_decision = self.decision_duration
                        return
                    
                    if found:
                        self.move_towards_grass_plants(self.current_target)
                        self.progress_left_on_decision = self.decision_duration
                        return
                    
                else:
                    self.move_towards_resource(food_id)
                    self.progress_left_on_decision = self.decision_duration
                    return
                


            
            if self.needs_water:
                #print(colorize("Needs Water", colors.BLUE))

                water_id = 2

                if self.is_current_target_static():
                    self.move_towards_resource(self.current_target.resource_type_id)
                    distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                    distance -= self.current_target.resource_radius
                    if distance < self.feeding_range:
                        self.drink_water()
                    else:
                        pass
                else:
                    self.move_towards_resource(water_id)
                        
                self.progress_left_on_decision = self.decision_duration
                return
            
            # fourth layer of decision making: Check if the organism is ready to mate

            if self.procreate_cool_down <= 0:
                self.ready_to_mate = True
                self.current_task = True

            if self.ready_to_mate:
                #print(colorize("Looking for Mate", colors.MAGENTA))

                if self.current_target is None:
                    self.wander()
                    self.detect_mates()
    
                if self.is_current_target_organism():
                    self.move_towards_organism(self.current_target)
                    distance = ((self.organism_position[0] - self.current_target.organism_position[0])**2 + (self.organism_position[1] - self.current_target.organism_position[1])**2)**0.5
                    if distance < self.feeding_range:
                        self.procreate()
                
                self.progress_left_on_decision = self.decision_duration
                return
            
            # fifth layer of decision making: Wander around
            self.wander()
            self.current_task = False
            self.progress_left_on_decision = self.decision_duration
            return
                
                
        
        else:
            self.progress_left_on_decision -= 1

    def move_towards_grass_plants(self, grass_plants: Any) -> None:
        
        angle = math.atan2(grass_plants.resource_position[1] - self.organism_position[1], grass_plants.resource_position[0] - self.organism_position[0])
        self.current_direction = [math.cos(angle), math.sin(angle)]
    
    def detect_grass_plants(self) -> bool:
        if self.is_current_target_static():
            resource_map = self.current_target.dynamic_resource_map
            for resource in resource_map.values():
                pos = resource.resource_position
                distance = ((self.organism_position[0] - pos[0])**2 + (self.organism_position[1] - pos[1])**2)**0.5
                if distance < self.sight_range:
                    self.current_target = resource
                    return True
                
            return False
        else:
            print(f"Something has gone seriously wrong {self.name}{self.animal_id} Current target: {self.current_target}")
            
    def is_current_target_grass_plants(self) -> bool:
        if isinstance(self.current_target, GrassPlant):
            return True
        return False

    def is_within_grass_lands(self) -> bool:
        if self.is_current_target_static():
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            if distance < self.current_target.resource_radius:
                return True
        else:
            for resource in self.all_known_static_resources.values():
                if resource.resource_type_id == 1:
                    distance = ((self.organism_position[0] - resource.resource_position[0])**2 + (self.organism_position[1] - resource.resource_position[1])**2)**0.5
                    if distance < resource.resource_radius:
                        self.current_target = resource
                        return True
        return False

    def is_at_grass_lands_center(self) -> bool:
        if self.is_current_target_static():
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            if distance < 20:
                return True
        else:
            for resource in self.all_known_static_resources.values():
                if resource.resource_type_id == 1:
                    distance = ((self.organism_position[0] - resource.resource_position[0])**2 + (self.organism_position[1] - resource.resource_position[1])**2)**0.5
                    if distance < 20:
                        return True
        return False
    
    def procreate(self) -> Any:
        pass

    