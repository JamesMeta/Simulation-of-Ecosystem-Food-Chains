from typing import List, Any
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
                # self.ready_to_mate = False
                # self.current_target = None
                # self.progress_left_on_decision = 0
                # self.stalking = False

                self.name = "Frog"
                self.species_id = 3
                self.procreate_cool_down = 10000     #ticks
                self.max_hunger = 2000               #ticks
                self.max_thirst = 1000               #ticks
                self.max_exhaustion = 5000           #ticks
                self.speed = 1                       #pixels per tick
                self.mass = 1
                self.visibility_range = 50          #pixels
                self.detection_range = 50           #pixels
                self.feeding_range = 5              #pixels
                self.sleep_duration = 100           #ticks
                self.detection_multiplier = 1       #constant
                self.consumable_organisms = {8}   #species_id
                self.decision_duration = 10         #ticks

                self.debug_mode = True
                
                if self.debug_mode:
                        self.color = "green"
                        self.radius = 3