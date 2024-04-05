from typing import List, Any
import random
import sys
sys.path.append("src/organism/animal/carnivor")
from Carnivor import Carnivor
from Carnivor import colors
from Carnivor import colorize

class Fox(Carnivor):
    
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
                # self.stalking = False
                # self.current_task = False

                self.name = "Fox"
                self.species_id = 1
                self.procreate_cool_down = 181440     #ticks
                self.max_hunger = 60480               #ticks
                self.max_thirst = 25920               #ticks
                self.max_exhaustion = 17280           #ticks
                self.min_hunger = 10080 
                self.min_thirst = 4320
                self.max_speed = 6.8                        # pixels per tick
                self.min_speed = 3.4                        # pixels per tick
                self.mass = 3.8
                self.sight_range = 300              #pixels
                self.feeding_range = 20              #pixels
                self.sleep_duration = 2880           #ticks
                self.detection_multiplier = 1       #constant
                self.consumable_organisms = [7,9]   #species_id
                self.potential_predators = [-1]        # species_id
                self.decision_duration = 50         #ticks
                self.metabolism_constant = 0.125
                
                if self.debug_mode:
                        self.color = "orange"
                        self.radius = 10

                if self.random_start:
                    self.hunger = random.randint(0, self.max_hunger)
                    self.thirst = random.randint(0, self.max_thirst)
                    self.exhaustion = random.randint(0, self.max_exhaustion)
                    self.procreate_cool_down = random.randint(0, self.procreate_cool_down)