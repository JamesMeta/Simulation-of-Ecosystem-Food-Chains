from typing import List, Any
import random
import sys
sys.path.append("src/organism/animal/carnivor")
from Carnivor import Carnivor

class Frog(Carnivor):
    
        def __init__(self, organism_position: List[float], animal_id: int):
                super().__init__(organism_position, animal_id)

                # inherited variables
                
                # self.organism_position = organism_position
                # self.animal_id = animal_id
                # self.all_known_resources = []
                # self.all_known_organisms = []
                # self.alive_status = True
                # self.hunger = 0
                # self.thirst = 0
                # self.exhaustion = 0
                # self.warned = False
                # self.in_danger = False
                # self.needs_sleep = False
                # self.ready_to_mate = False
                # self.current_target = None
                # self.progress_left_on_decision = 0
                # self.stalking = False

                self.name = "Frog"
                self.species_id = 3
                self.procreate_cool_down = 72576     #ticks
                self.max_hunger = 86400               #ticks
                self.max_thirst = 4320               #ticks
                self.max_exhaustion = 8640           #ticks
                self.min_hunger = 14400
                self.min_thirst = 720
                self.speed = 1                       #pixels per tick
                self.mass = 0.02
                self.sight_range = 300              #pixels
                self.feeding_range = 5              #pixels
                self.sleep_duration = 360           #ticks
                self.detection_multiplier = 1       #constant
                self.consumable_organisms = {8}   #species_id
                self.decision_duration = 100         #ticks
                
                if self.debug_mode:
                        self.color = "green"
                        self.radius = 3
                
                if self.random_start:
                    self.hunger = random.randint(0, self.max_hunger)
                    self.thirst = random.randint(0, self.max_thirst)
                    self.exhaustion = random.randint(0, self.max_exhaustion)
                    self.procreate_cool_down = random.randint(0, self.procreate_cool_down)