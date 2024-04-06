import sys
import random
import math

sys.path.append("src/maplogic")
sys.path.append("src/organism/animal")

from Animal import Animal
from maplogic.GrassPlant import GrassPlant
from typing import List, Any


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


    # This function serves to check if the current task can be completed during the current decision cycle
    # If the task is in range, the function will call the appropriate function to complete the task
    # This serves to correct the issue with the previous implementation 
    # Where the organism would become out of range of the task before being able to make a decision to complete the task
    # This function is generally light weight computationally speaking since it is called every tick 
    # Rather then every 50 like the decision making function
    def check_if_current_task_in_range(self) -> None:

        # If organism passes absolute need threshold allow it to make a decision immediately
        if self.is_absolute_need():
            self.progress_left_on_decision = 0
            return

        # If the organism is in danger, allow it to make a decision immediately to run away
        if self.in_danger:
            self.run_away_from_threats()
            return

        # If the organism needs sleep and is at the safe place, allow it to sleep
        if self.needs_sleep and self.current_target is not None:
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            if distance < self.current_target.resource_radius:
                self.sleep()
                self.hidden = True
                return
            else:
                self.move_towards_specific_resource(self.current_target)
                return

        # If the organism needs food and is at the food source, allow it to eat
        if self.needs_food and self.current_target is not None:
            if self.is_current_target_static():
                
                if self.is_at_grass_lands_center() and not self.detect_grass_plants():
                    self.visited_static_resources.append(self.current_target)
                    self.current_target = None
                    self.current_direction = [0, 0]
                    return
                
                elif self.is_within_grass_lands():
                    if self.detect_grass_plants():
                        self.move_towards_grass_plants(self.current_target)
                        return
                    
                else:
                    self.detect_grass_plants()
                    self.move_towards_grass_plants(self.current_target)
                
            elif self.is_current_target_grass_plants():
                distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                if distance < self.feeding_range:
                    self.eat_food()
                    return
                else:
                    self.move_towards_grass_plants(self.current_target)
                    return

        # If the organism needs water and is at the water source, allow it to drink
        if self.needs_water and self.current_target is not None:
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            distance -= self.current_target.resource_radius
            if distance < self.feeding_range:
                self.drink_water()
            else:
                pass

        # If the organism is ready to mate and is at the mate, allow it to mate
        if self.ready_to_mate and self.current_target is not None:

            if not self.is_current_target_organism():
                return
            
            distance = ((self.organism_position[0] - self.current_target.organism_position[0])**2 + (self.organism_position[1] - self.current_target.organism_position[1])**2)**0.5
            if distance <= self.feeding_range:
                self.procreate()
            else:
                pass

    # This function serves to detect grass plants within the sight range of the organism
    # It is called when the organism is in need of food
    # It will set the current target to the nearest grass plant within the sight range
    # If no grass plants are within the sight range, the function will return False
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
    
    # This function serves to check the current target of the organism is grass and not someting else
    # This function is used as a failsafe to ensure the organism is targeting the correct resource 
    def is_current_target_grass_plants(self) -> bool:
        if isinstance(self.current_target, GrassPlant):
            return True
        return False

    # This function serves to check if the organism is within the grass lands
    # Behavior is different if the organism is inside the static resource or not
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

    # This function serves to check if the organism is at the center of the grass lands
    # Behavior is different if the organism is at the center of the static resource or not
    # This is because if the organism is at the center of the static resource and still has not found any grass plants
    # It should move to a new static resource since this one currently has no food
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

    # This function serves to make a decision for the organism
    # It is the main brain of the organism
    # It is called once every decision_duration which is currently set to 50 ticks
    # It follows a decision tree structure to determine the best course of action for the organism based on priority
    # It starts by checking if the organism is alive, then if it is in danger, then if it needs sleep, food, or water
    # If none of these conditions are met, the organism will check if it is ready to mate
    # If thats not true, the organism will wander around
    def make_decision(self) -> None:

        self.is_absolute_need()

        if self.hunger > self.max_hunger:
            self.die("starvation")
        
        if self.thirst > self.max_thirst:
            self.die("dehydration")

        if self.current_task:
            self.check_if_current_task_in_range()

        if self.progress_left_on_decision == 0:

            #disable hide as the organism is now making a decision can be reenabled if needed
            if self.hidden:
                self.hidden = False

            # first layer of decision making: Check alive status
            if not self.alive_status:
                self.die("not sure why") # This should never be called but is here as a failsafe
                return
            
            # second layer of decision making: Check if the organism is in danger
            # this layer can be overridden by absolute needs
            # if absolute needs are not met it will overrule all previous decisions

            self.detect_threats()
            if self.current_threat is not None and not self.absolute_need:
                self.in_danger = True

            if self.in_danger and not self.absolute_need:
                self.run_away_from_threats()
                self.progress_left_on_decision = self.decision_duration
                self.needs_for_speed = True
                self.needs_food = False
                self.needs_water = False
                self.needs_sleep = False
                self.ready_to_mate = False
                self.current_task = True
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
                self.current_task = True
            
            if self.needs_sleep:

                #if the organism has a safe place to sleep at, move towards it
                if self.safe_place is not None:
                    self.move_towards_specific_resource(self.safe_place)
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

                # pick a random food source within the consumable resources to target
                # currently only grass plants are available so this is redundant
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

                water_id = 2

                if self.is_current_target_static():
                    if self.current_target.resource_type_id == water_id:
                        self.move_towards_specific_resource(self.current_target)
                        distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                        distance -= self.current_target.resource_radius
                        if distance < self.feeding_range:
                            self.drink_water()
                        else:
                            pass
                    else:
                        self.move_towards_resource(water_id)
                else:
                    self.move_towards_resource(water_id)
                        
                self.progress_left_on_decision = self.decision_duration
                return
            
            # fourth layer of decision making: Check if the organism is ready to mate

            if self.procreate_cool_down <= 0:
                self.ready_to_mate = True
                self.current_task = True

            if self.ready_to_mate:

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

    # This function serves to move the organism towards a living grass plant
    # It is called when the organism is in need of food
    # Grass should be detected by the organism before this function is called
    def move_towards_grass_plants(self, grass_plants: Any) -> None:
        
        angle = math.atan2(grass_plants.resource_position[1] - self.organism_position[1], grass_plants.resource_position[0] - self.organism_position[0])
        self.current_direction = [math.cos(angle), math.sin(angle)]
    
    # override this function in the child class
    def procreate(self) -> Any:
        pass

    