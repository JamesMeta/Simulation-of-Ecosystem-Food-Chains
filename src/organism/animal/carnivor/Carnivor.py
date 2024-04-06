import sys
import random
import math
import numpy as np
sys.path.append("src/organism/animal")
from Animal import Animal
from typing import List, Any

class Carnivor(Animal):

    def __init__(self, organism_position: List[float], animal_id: int, all_known_static_resources: Any,  all_known_organisms: Any):
        
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

        self.stalking = False
        self.dietary_classification = 0
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
        self.consumable_organisms = None
        self.decision_duration = None
        self.potential_predators = None
        self.visited_static_resources = []

    # This function serves to begin the food detection process
    # It will detect food in the sight range of the organism and begin the stalking process if found
    # It will also cause the organism to wander to different static resources if no food is found in its vacinity
    # It will also cause the organism to wander if all static resources have been visited
    def begin_hunting(self):

        # Failsafe to prevent target being in stalker mode despite not having a target
        if self.current_target is None or not self.is_current_target_organism:
            self.stalking = False

        # Used to detect food and begin stalking if food is found
        if self.detect_food():
            self.begin_stalking()
            self.stalking = True
            self.visited_static_resources = []
        
        # Used to wander to different static resources if no food is found in the vacinity
        elif len(self.visited_static_resources) != len(self.all_known_static_resources):

            if self.is_current_target_static():
                self.move_towards_specific_resource(self.current_target)
                return
            else:
                for resource in self.all_known_static_resources.values():
                    if resource not in self.visited_static_resources:
                        self.move_towards_specific_resource(resource)
                        return
        
        # Used to wander if all static resources have been visited
        else:
            self.wander()
            self.visited_static_resources = [] # Reset the visited static resources list

    # This function serves to begin the consumption process of food
    # Once an organism is detected the organism will move towards the organism
    # If the organism is out of the sight range of the organism, the organism will move towards the future position of the organism
    # If the organism is in the sight range of the organism, the organism will move towards the current position of the organism
    # Once the organism is in the feeding range of the organism, the organism will eat the organism
    # Speed will change depending on the strategy currently being used
    def begin_stalking(self):

        if self.current_target is None or not self.is_current_target_organism():
            self.stalking = False
            return
        
        if self.current_target.alive_status == False:
            self.current_target = None
            self.stalking = False
            return
        
        distance = ((self.organism_position[0] - self.current_target.organism_position[0])**2 + (self.organism_position[1] - self.current_target.organism_position[1])**2)**0.5

        if distance <= self.feeding_range:
            self.eat_food()
            return
        
        if distance > self.sight_range:
            self.current_target = None
            self.stalking = False
            return
        
        target_position = np.array(self.current_target.organism_position)
        target_view_range = self.current_target.sight_range
        target_current_direction = np.array(self.current_target.current_direction)
        target_current_speed = self.current_target.min_speed
        target_remaining_ticks = self.current_target.progress_left_on_decision

        if distance > target_view_range:
            target_future_position = target_position + (target_current_direction * target_current_speed * target_remaining_ticks)
            angle = math.atan2(target_future_position[1] - self.organism_position[1], target_future_position[0] - self.organism_position[0])
            self.current_direction = [math.cos(angle), math.sin(angle)]
            self.stalking = True

        if distance <= target_view_range or self.current_target.in_danger:
            angle = math.atan2(target_position[1] - self.organism_position[1], target_position[0] - self.organism_position[0])
            self.current_direction = [math.cos(angle), math.sin(angle)]
            self.needs_for_speed = True
            self.stalking = False

    # This function serves to check if the current task can be completed during the current decision cycle
    # If the task is in range, the function will call the appropriate function to complete the task
    # This serves to correct the issue with the previous implementation 
    # Where the organism would become out of range of the task before being able to make a decision to complete the task
    # This function is generally light weight computationally speaking since it is called every tick 
    # Rather then every 50 like the decision making function
    # Refer to the herbivore implementation for a more detailed line by line explanation
    def check_if_current_task_in_range(self) -> None:


        if self.is_absolute_need():
            self.progress_left_on_decision = 0
        
        if self.needs_sleep and self.current_target is not None:
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            if distance < self.current_target.resource_radius:
                self.sleep()
                self.hidden = True
                return
            else:
                self.move_towards_specific_resource(self.current_target)
                return

        if self.needs_food:

            if self.is_current_target_static():
                if self.is_at_center_of_resource():
                    self.visited_static_resources.append(self.current_target)
                    self.current_target = None
                    self.current_direction = [0,0]


            if self.is_current_target_organism():
                distance = ((self.organism_position[0] - self.current_target.organism_position[0])**2 + (self.organism_position[1] - self.current_target.organism_position[1])**2)**0.5
                if distance < self.feeding_range:
                    self.eat_food()
                else:
                    self.begin_stalking()

                
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

    # This function serves to detect prey in the sight range of the organism
    # It targets the closest organism in the sight range of the organism
    # Its generally very heavy computationally speaking since it scans through all organisms in the simulation
    # In the future, this function can be optimized by using a quad tree data structure to store the organisms
    def detect_food(self) -> bool:
        potential_food = [None,None]
        for organism in self.all_known_organisms.values():

            if organism.hidden:
                continue

            if organism.species_id in self.consumable_organisms:
                distance = ((self.organism_position[0] - organism.organism_position[0])**2 + (self.organism_position[1] - organism.organism_position[1])**2)**0.5
                if distance <= self.sight_range:

                    if potential_food[0] is None:
                        potential_food = [distance, organism]

                    if potential_food[0] > distance:
                        potential_food = [distance, organism]
        
        if potential_food[1] is None:
            return False

        self.current_target = potential_food[1]
        return True

    #if the animal is close to death, it will have an absolute need to eat or drink
    #this will override all other needs except for sleep
    #predators will nolonger scare the animal whether for the better or for the very very worse...
    def is_absolute_need(self):
        if self.hunger > self.max_hunger * 0.95:
            self.absolute_need = True
            self.consumable_organisms.append(self.species_id)
            return True
        
        if self.hunger > self.max_hunger * 0.8:
            self.absolute_need = True
            return True
        
        if self.thirst > self.max_thirst * 0.8:
            self.absolute_need = True
            return True
        
        self.absolute_need = False
    
        if self.species_id in self.consumable_organisms:
            self.consumable_organisms.remove(self.species_id)

        return False

    # Similar to the herbivore implementation, this function serves to check if the organism is at the center of the resource
    # Used to determine if the organism has been to this resource before
    def is_at_center_of_resource(self) -> bool:
        if self.is_current_target_static():
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            if distance < self.feeding_range:
                return True
        else:
            print("Something went wrong in is_at_center_of_resource()")

    # This function serves to make a decision for the organism
    # It is the main brain of the organism
    # It is called once every decision_duration which is currently set to 50 ticks
    # It follows a decision tree structure to determine the best course of action for the organism based on priority
    # It starts by checking if the organism is alive, then if it is in danger, then if it needs sleep, food, or water
    # If none of these conditions are met, the organism will check if it is ready to mate
    # If thats not true, the organism will wander around
    # Refer to the herbivore implementation for a more detailed line by line explanation
    def make_decision(self) -> None:

        self.is_absolute_need()

        if self.hidden:
                self.hidden = False

        if self.hunger > self.max_hunger:
            self.die("starvation")
        
        if self.thirst > self.max_thirst:
            self.die("dehydration")

        if self.current_task:
            self.check_if_current_task_in_range()

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

        if self.progress_left_on_decision == 0:

            # first layer of decision making: Check alive status

            if not self.alive_status:
                self.die("not sure why")
                return
            
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
                    
                if percent_water_remaining < percent_food_remaining:
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

                if self.stalking:
                    self.begin_stalking()
                    self.progress_left_on_decision = self.decision_duration
                    return

                self.begin_hunting()
        
                self.progress_left_on_decision = self.decision_duration
                return
                
           
            if self.needs_water:

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

    # override this function in the child class
    def procreate(self) -> Any:
        pass
    

    

    


            

        
        


                    



