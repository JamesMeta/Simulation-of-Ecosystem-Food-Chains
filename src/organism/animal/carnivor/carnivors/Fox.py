from typing import List, Any
import sys
sys.path.append("src/organism/animal/carnivor")
from Carnivor import Carnivor

class Fox(Carnivor):
    
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

                self.name = "Fox"
                self.species_id = 1
                self.procreate_cool_down = 181440     #ticks
                self.max_hunger = 60480               #ticks
                self.max_thirst = 4320               #ticks
                self.max_exhaustion = 17280           #ticks
                self.min_hunger = 10080
                self.min_thirst = 4320
                self.speed = 1                       #pixels per tick
                self.mass = 3.8
                self.sight_range = 300              #pixels
                self.feeding_range = 5              #pixels
                self.sleep_duration = 2880           #ticks
                self.detection_multiplier = 1       #constant
                self.consumable_organisms = {7,9}   #species_id
                self.decision_duration = 100         #ticks

                self.debug_mode = True
                
                if self.debug_mode:
                        self.color = "orange"
                        self.radius = 10