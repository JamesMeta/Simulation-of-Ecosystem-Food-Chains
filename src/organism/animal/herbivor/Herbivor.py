import sys
import random
sys.path.append("src/organism/animal")
from Animal import Animal
from typing import List, Any

class Herbivor(Animal):
    
    def __init__(self, organism_position: List[float], animal_id: int, all_known_static_resources: Any, all_known_dynamic_resources: Any, all_known_organisms: Any):

        super().__init__(organism_position, animal_id, all_known_static_resources, all_known_dynamic_resources, all_known_organisms)

        # inherited variables

        # self.organism_position = organism_position
        # self.animal_id = animal_id

        # self.all_known_static_resources = {}
        # self.all_known_dynamic_resources = {}
        # self.all_known_organisms = {}
        # self.alive_status = True

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

        self.hidden = False

    def make_decision(self) -> None:

        if self.hunger > self.max_hunger:
            self.die()
        
        if self.thirst > self.max_thirst:
            self.die()

        if self.needs_food:
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            if self.is_current_target_dyanmic():
                if distance < self.feeding_range:
                    self.eat_food()
                else:
                    pass
            else:
                if distance < self.sight_range:
                    self.Detect_Food()
                    self.move_towards_dynamic_resource(self.current_target)
                else:
                    pass
                
        if self.needs_water:
            distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
            distance -= self.current_target.resource_radius
            if distance < self.feeding_range:
                self.drink_water()
            else:
                pass

        if self.ready_to_mate and self.current_target is not None:
            distance = ((self.organism_position[0] - self.current_target.organism_position[0])**2 + (self.organism_position[1] - self.current_target.organism_position[1])**2)**0.5
            if distance < self.feeding_range:
                self.procreate()
            else:
                pass
        
        if self.progress_left_on_decision == 0:

            print("Making decision")

            # first layer of decision making: Check alive status

            if not self.alive_status:
                self.die()
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
                return
            
            else:
                self.needs_for_speed = False
            
            # third layer of decision making: Check if the organism needs sleep, food, or water balancing the priorities based on absolute needs

            if self.hunger > self.min_hunger or self.thirst > self.min_thirst:
                percent_food_remaining = 1 - (self.hunger / self.max_hunger)
                percent_water_remaining = 1 - (self.thirst / self.max_thirst)
                self.ready_to_mate = False
            

                if percent_food_remaining < percent_water_remaining:
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
            
            if self.needs_sleep:
                print("Needs sleep")
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
                print("Needs food")
                if self.is_current_target_dyanmic():
                    self.move_towards_dynamic_resource(self.current_target)
                    distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                    if distance < self.feeding_range:
                        self.eat_food()
                    else:
                        pass
                else:
                    if not self.Detect_Food():
                        self.move_towards_resource(random.choice(self.consumable_resources))
                        
                self.progress_left_on_decision = self.decision_duration
                return
            
            if self.needs_water:
                print("Needs water")

                water_id = 2

                if self.current_target:
                    self.move_towards_resource(self.current_target.resource_type_id)
                    distance = ((self.organism_position[0] - self.current_target.resource_position[0])**2 + (self.organism_position[1] - self.current_target.resource_position[1])**2)**0.5
                    distance -= self.current_target.resource_radius
                    if distance < self.feeding_range:
                        self.drink_water()
                    else:
                        pass
                else:
                    if not self.Detect_Water():
                        self.move_towards_resource(water_id)
                        
                self.progress_left_on_decision = self.decision_duration
                return
            
            # fourth layer of decision making: Check if the organism is ready to mate

            if self.procreate_cool_down < 0:
                self.ready_to_mate = True

            if self.ready_to_mate:
                print("Looking for mate")
                if self.current_target is None:
                    self.wander()
                    self.Detect_Mates()
    
                if self.current_target is not None:
                    self.move_towards_organism(self.current_target)
                    distance = ((self.organism_position[0] - self.current_target.organism_position[0])**2 + (self.organism_position[1] - self.current_target.organism_position[1])**2)**0.5
                    if distance < self.feeding_range:
                        self.procreate()
                
                self.progress_left_on_decision = self.decision_duration
                return
            
            # fifth layer of decision making: Wander around
            self.wander()
            self.progress_left_on_decision = self.decision_duration
            return
                
                
        
        else:
            self.progress_left_on_decision -= 1

        
    def Detect_Food(self) -> Any:
        for resource in self.all_known_dynamic_resources.values():
            resource_position = resource.resource_position
            distance = ((self.organism_position[0] - resource_position[0])**2 + (self.organism_position[1] - resource_position[1])**2)**0.5
            if distance < self.sight_range:
                self.current_target = resource
                return True
        return False
    
    def procreate(self) -> Any:
        pass

    