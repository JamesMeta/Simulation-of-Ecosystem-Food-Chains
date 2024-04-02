from typing import List, Any
import sys
import random
sys.path.append("src/organism/animal/carnivor")
from Carnivor import Carnivor

class Owl(Carnivor):
    
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
                # self.stalking = False
                # self.current_task = False

                self.name = "Owl"
                self.species_id = 2
                self.procreate_cool_down = 181440     #ticks
                self.max_hunger = 43200               #ticks
                self.max_thirst = 17280               #ticks
                self.max_exhaustion = 4320           #ticks
                self.min_hunger = 7200
                self.min_thirst = 2880
                self.max_speed = 2                        # pixels per tick
                self.min_speed = 1                        # pixels per tick
                self.mass = 1.8
                self.sight_range = 360              #pixels
                self.feeding_range = 5              #pixels
                self.sleep_duration = 720           #ticks
                self.detection_multiplier = 1       #constant
                self.consumable_organisms = {3,9}   #species_id
                self.potential_predators = {-1}        # species_id
                self.decision_duration = 100         #ticks
                
                if self.debug_mode:
                        self.color = "brown"
                        self.radius = 7

                if self.random_start:
                    self.hunger = random.randint(0, self.max_hunger)
                    self.thirst = random.randint(0, self.max_thirst)
                    self.exhaustion = random.randint(0, self.max_exhaustion)
                    self.procreate_cool_down = random.randint(0, self.procreate_cool_down)
